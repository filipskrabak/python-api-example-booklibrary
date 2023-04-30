from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v1/passengers/{passenger_id}/companions")
async def status(passenger_id: str):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT tickets.passenger_id AS id, tickets.passenger_name AS name, COUNT(*) AS flights_count, ARRAY_AGG(flights.flight_id ORDER BY flights.flight_id ASC) AS flights FROM tickets 
    JOIN ticket_flights ON ticket_flights.ticket_no = tickets.ticket_no 
    JOIN flights ON flights.flight_id = ticket_flights.flight_id 
    WHERE flights.flight_id IN ( 
    SELECT flights.flight_id from tickets 
    JOIN ticket_flights ON tickets.ticket_no = ticket_flights.ticket_no 
    JOIN flights ON ticket_flights.flight_id = flights.flight_id 
    WHERE tickets.passenger_id = '{passenger_id}' 
    ORDER BY flights.flight_id ASC) AND tickets.passenger_id != '{passenger_id}' 
    GROUP BY tickets.passenger_id, tickets.passenger_name 
    ORDER BY flights_count DESC, tickets.passenger_id ASC; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        output_row = {}
        output_row["id"] = row[0]
        output_row["name"] = row[1]
        output_row["flights_count"] = row[2]
        output_row["flights"] = row[3]

        output["results"].append(output_row)

    cursor.close()
    db_instance.close()

    return output
