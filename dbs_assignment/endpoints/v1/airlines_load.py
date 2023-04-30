from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

from decimal import *

router = APIRouter()


@router.get("/v1/airlines/{flight_no}/load")
async def status(flight_no: str):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT flights.flight_id, COUNT(flights.flight_id) as aircraft_capacity, t.load, ROUND(((t.load::float/COUNT(flights.flight_id)::float)*100)::numeric, 2) AS load_percentage FROM flights 
        JOIN aircrafts_data ON flights.aircraft_code = aircrafts_data.aircraft_code 
        JOIN seats ON seats.aircraft_code = aircrafts_data.aircraft_code 
        JOIN ( 
        SELECT DISTINCT flights.flight_id, COUNT(ticket_flights.ticket_no) AS load FROM flights 
        JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id 
        WHERE flights.flight_no = '{flight_no}' 
        GROUP BY flights.flight_id 
        ORDER BY flights.flight_id ASC 
        ) as t ON t.flight_id = flights.flight_id 
        WHERE flights.flight_no = '{flight_no}' 
        GROUP BY flights.flight_id, t.load 
        ORDER BY flights.flight_id ASC; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        output_row = {}
        output_row["id"] = row[0]
        output_row["aircraft_capacity"] = row[1]
        output_row["load"] = row[2]
        output_row["percentage_load"] = Decimal(row[3]).normalize()

        output["results"].append(output_row)

    cursor.close()
    db_instance.close()

    return output
