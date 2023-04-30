from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v1/departures")
async def status(airport:str, day:int):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT flight_id, flight_no, scheduled_departure FROM airports_data 
    JOIN flights ON flights.departure_airport = airports_data.airport_code 
    WHERE flights.status = 'Scheduled' AND airports_data.airport_code = '{airport}' AND EXTRACT(ISODOW FROM scheduled_departure) = {day}
    ORDER BY scheduled_departure ASC, flight_id ASC; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        output_row = {}
        output_row["flight_id"] = row[0]
        output_row["flight_no"] = row[1]
        output_row["scheduled_departure"] = row[2]

        output["results"].append(output_row)

    cursor.close()
    db_instance.close()

    return output
