from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v3/airlines/{flight_no}/top_seats")
async def handler(flight_no: str, limit: int):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT seat_no, array_length(array_agg(flight_id), 1) as flight_count, array_agg(flight_id) as flights FROM (
    SELECT t.flight_id, t.seat_no, SUM(t.grp_start) OVER (order by t.seat_no, t.flight_id) FROM (
    SELECT boarding_passes.flight_id, seat_no, 
        (CASE WHEN (flights.flight_id != LAG(flights.flight_id) OVER 
                    (partition by seat_no ORDER BY flights.flight_id) + 1) 
        OR (LAG(flights.flight_id) OVER 
            (partition by seat_no ORDER BY flights.flight_id) IS NULL) THEN 1 ELSE 0 END) 
        as grp_start
    FROM boarding_passes
    JOIN flights ON flights.flight_id = boarding_passes.flight_id
    WHERE flight_no = '{flight_no}'
    ORDER by seat_no, flight_id) AS t) as s
    GROUP BY sum, seat_no
    ORDER BY flight_count DESC, seat_no, flights
    LIMIT {limit}; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        single_record = {}
        
        single_record["seat"] = row[0]
        single_record["flights_count"] = row[1]
        single_record["flights"] = row[2]

        output["results"].append(single_record)


    cursor.close()
    db_instance.close()

    return output
