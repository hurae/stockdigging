from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI
from datetime import datetime
from storage.business.server import json_handle
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Item(List):
    item_id: int
    item_text: str

class Data( BaseModel ):
    index_info_id: int
    trade_date: List[Item]
    # close: float
    # open: float
    # high: float
    # low: float


@app.post( "/store" )
def json_pull(data: Data):
    return data


uvicorn.run( app, host='127.0.0.1', port=8000 )
