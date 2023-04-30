from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v1/bookings/{booking_id}")
async def status(booking_id: str):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT bookings.book_ref, bookings.book_date, tickets.ticket_no, tickets.passenger_id, tickets.passenger_name, boarding_passes.boarding_no, flights.flight_no, boarding_passes.seat_no, flights.aircraft_code, flights.arrival_airport, flights.departure_airport, flights.scheduled_arrival, flights.scheduled_departure FROM bookings 
    JOIN tickets ON bookings.book_ref = tickets.book_ref 
    JOIN ticket_flights ON tickets.ticket_no = ticket_flights.ticket_no 
    JOIN flights ON ticket_flights.flight_id = flights.flight_id 
    JOIN boarding_passes ON ticket_flights.ticket_no = boarding_passes.ticket_no AND ticket_flights.flight_id = boarding_passes.flight_id 
    WHERE bookings.book_ref = '{booking_id}' 
    GROUP BY bookings.book_ref, tickets.ticket_no, ticket_flights.ticket_no, ticket_flights.flight_id, flights.flight_id, boarding_passes.ticket_no, boarding_passes.flight_id 
    ORDER BY tickets.ticket_no, boarding_passes.boarding_no; """)

    output = {}
    output["result"] = {}
    
    rows = cursor.fetchall()

    for row in rows: 
        if("id" not in output["result"] and "book_date" not in output["result"]):
            output["result"]["id"] = row[0]
            output["result"]["book_date"] = row[1]
            output["result"]["boarding_passes"] = []

        output_row = {}
        output_row["id"] = row[2]
        output_row["passenger_id"] = row[3]
        output_row["passenger_name"] = row[4]
        output_row["boarding_no"] = row[5]
        output_row["flight_no"] = row[6]
        output_row["seat"] = row[7]
        output_row["aircraft_code"] = row[8]
        output_row["arrival_airport"] = row[9]
        output_row["departure_airport"] = row[10]
        output_row["scheduled_arrival"] = row[11]
        output_row["scheduled_departure"] = row[12]

        output["result"]["boarding_passes"].append(output_row)

    cursor.close()
    db_instance.close()

    return output
