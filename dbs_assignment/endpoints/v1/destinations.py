from fastapi import APIRouter

from dbs_assignment.config import settings

from dbs_assignment import database

router = APIRouter()


@router.get("/v1/airports/{airport}/destinations")
async def status(airport: str):
    db_instance = database.DBConn()
    cursor = db_instance.conn.cursor()
    cursor.execute(f"""SELECT DISTINCT arrival_airport FROM airports_data 
    JOIN flights ON departure_airport = airport_code  
    WHERE departure_airport = '{airport}' 
    ORDER BY arrival_airport ASC; """)

    output = {}
    output["results"] = []
    
    rows = cursor.fetchall()

    for row in rows: 
        output["results"].append(row[0])

    cursor.close()
    db_instance.close()

    return output
