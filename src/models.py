from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId
from enum import Enum
from datetime import datetime

class SearchQuery(BaseModel):
    search_term:str =''
    search_criteria:str ='name'

class Item(BaseModel):
    id:int
    name:str
    qty:int
    price:float
    supplier:int

class Customer(BaseModel):
    id:int
    first_name:str
    last_name:str
    customer_type:str
    address:str
    postal: str
    phone:str

