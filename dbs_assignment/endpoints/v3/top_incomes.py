from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

from decimal import *

router = APIRouter()


@router.get("/v3/aircrafts/{aircraft_code}/top-incomes")
async def handler(aircraft_code: str):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT max as total_amount, year || '-' || month as month, day::text FROM (
SELECT *, MAX(t.sum) OVER (partition by t.year, t.month) as max
FROM (
SELECT EXTRACT('Month' FROM f.actual_departure) as month, EXTRACT('Year' FROM f.actual_departure) as year, EXTRACT('Day' FROM f.actual_departure) as day, SUM(amount) FROM flights as f
JOIN ticket_flights AS tf ON f.flight_id = tf.flight_id
WHERE f.aircraft_code = '{aircraft_code}' AND f.actual_departure IS NOT NULL
GROUP BY year, month, day) AS t) AS s
WHERE s.sum = s.max
ORDER BY total_amount DESC, s.month ASC; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        single_record = {}
        
        single_record["total_amount"] = Decimal(row[0]).normalize()
        single_record["month"] = row[1]
        single_record["day"] = row[2]

        output["results"].append(single_record)


    cursor.close()
    db_instance.close()

    return output
