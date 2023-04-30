from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v1/flights/late-departure/{delay}")
async def status(delay: int):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT flight_id, flight_no, (EXTRACT(EPOCH FROM actual_departure-scheduled_departure)/60)::int AS delay FROM flights 
    WHERE (EXTRACT(EPOCH FROM actual_departure-scheduled_departure)/60)::int > {delay} 
    ORDER BY delay DESC; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        output_row = {}
        output_row["flight_id"] = row[0]
        output_row["flight_no"] = row[1]
        output_row["delay"] = row[2]

        output["results"].append(output_row)

    cursor.close()
    db_instance.close()

    return output
