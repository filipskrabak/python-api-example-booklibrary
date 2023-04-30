from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v3/aircrafts/{aircraft_code}/seats/{seat_choice}")
async def handler(aircraft_code: str, seat_choice: int):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT seat_no, COUNT(seat_no) FROM (
    SELECT *, dense_rank() over(partition by flights.flight_id order by book_date asc) as rnk FROM flights
    JOIN boarding_passes ON flights.flight_id = boarding_passes.flight_id
    JOIN tickets ON tickets.ticket_no = boarding_passes.ticket_no
    JOIN bookings ON bookings.book_ref = tickets.book_ref
    WHERE aircraft_code = '{aircraft_code}') AS t
    WHERE t.rnk = {seat_choice}
    GROUP BY seat_no
    ORDER BY count DESC
    LIMIT 1; """)

    output = {}
    output["result"] = {}
    
    rows = cursor.fetchall()

    for row in rows: 
        output["result"]["seat"] = row[0]
        output["result"]["count"] = row[1]

    cursor.close()
    db_instance.close()

    return output
