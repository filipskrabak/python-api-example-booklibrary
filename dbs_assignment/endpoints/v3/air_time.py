from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v3/air-time/{book_ref}")
async def handler(book_ref: str):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT t.ticket_no, t.passenger_name, ARRAY_AGG(array[t.departure_airport::text, t.arrival_airport::text, TO_CHAR(t.flight_time, 'fmhh24:mi:ss'), TO_CHAR(t.total_time, 'fmhh24:mi:ss')] ORDER by t.actual_departure ASC) as flights FROM (
    SELECT tickets.ticket_no, passenger_name, departure_airport, arrival_airport, actual_arrival-actual_departure as flight_time, SUM(actual_arrival-actual_departure) over(partition by tickets.ticket_no order by actual_departure asc) as total_time, actual_departure from flights
    JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id
    JOIN tickets ON ticket_flights.ticket_no = tickets.ticket_no
    WHERE tickets.book_ref = '{book_ref}') AS t
    GROUP BY t.ticket_no, t.passenger_name; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        single_passenger = {}
        
        single_passenger["ticket_no"] = row[0]
        single_passenger["passenger_name"] = row[1]
        single_passenger["flights"] = [] # arr

        for flight in row[2]:
            single_flight = {}
            single_flight["departure_airport"] = flight[0]
            single_flight["arrival_airport"] = flight[1]
            single_flight["flight_time"] = flight[2]
            single_flight["total_time"] = flight[3]

            single_passenger["flights"].append(single_flight)

        output["results"].append(single_passenger)


    cursor.close()
    db_instance.close()

    return output
