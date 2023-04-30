from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v1/airlines/{flight_no}/load-week")
async def status(flight_no: str):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT s.day_str, ROUND(AVG(load_percentage), 2) FROM ( 
    
    SELECT flights.flight_id, ((t.load::float/COUNT(flights.flight_id)::float)*100)::numeric AS load_percentage, TO_CHAR(scheduled_departure, 'ID') AS day, TO_CHAR(scheduled_departure, 'Day') AS day_str, flights.flight_no FROM flights 
    JOIN aircrafts_data ON flights.aircraft_code = aircrafts_data.aircraft_code 
    JOIN seats ON seats.aircraft_code = aircrafts_data.aircraft_code 
    JOIN ( 
        
    SELECT DISTINCT flights.flight_id, COUNT(ticket_flights.ticket_no) AS load, flights.flight_no FROM flights 
    JOIN ticket_flights ON ticket_flights.flight_id = flights.flight_id 
    WHERE flights.flight_no = '{flight_no}' 
    GROUP BY flights.flight_id 
    ORDER BY flights.flight_id ASC 
        
    ) AS t ON t.flight_id = flights.flight_id 
    WHERE flights.flight_no = '{flight_no}' 
    GROUP BY flights.flight_id, t.load 
    ORDER BY flights.flight_id ASC 
        
    ) AS s 
    GROUP BY day, s.day_str 
    ORDER BY day ASC; """)

    output = {}
    output["result"] = {}
    
    rows = cursor.fetchall()

    output["result"]["flight_no"] = flight_no
    output["result"]["monday"] = rows[0][1]
    output["result"]["tuesday"] = rows[1][1]
    output["result"]["wednesday"] = rows[2][1]
    output["result"]["thursday"] = rows[3][1]
    output["result"]["friday"] = rows[4][1]
    output["result"]["saturday"] = rows[5][1]
    output["result"]["sunday"] = rows[6][1]
    
    cursor.close()
    db_instance.close()

    return output
