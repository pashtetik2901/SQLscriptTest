from fastapi import FastAPI
from app.config import setting
from database.model import simply_db_conn
from database.model.script_db.script import add_product
from app.model_valid.response_model import MainResponse
from app.model_valid.request_model import NewOrder
import uvicorn

app = FastAPI()

@app.post("/add", response_model=MainResponse)
async def add_order_item(data: NewOrder):
    try:
        add_product(data)
        
        return MainResponse(status=True)
    except Exception as err:
        print(f'Error - {err}')
        return MainResponse(status=False)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)