from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v1/top-airlines")
async def status(limit: int):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT flights.flight_no, COUNT(flights.flight_no) AS count FROM flights 
    JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id 
    JOIN tickets ON ticket_flights.ticket_no = tickets.ticket_no 
    WHERE flights.status = 'Arrived' 
    GROUP BY flights.flight_no 
    ORDER BY count DESC, flights.flight_no ASC 
    LIMIT {limit}; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        output_row = {}
        output_row["flight_no"] = row[0]
        output_row["count"] = row[1]

        output["results"].append(output_row)

    cursor.close()
    db_instance.close()

    return output
