import fastapi
import uvicorn
from fastapi import FastAPI, Path, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Query
import pprint

# import os
# import sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

from .database import InventoryOperator, CustomerOperator
from .models import *


api = fastapi.FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get('/search/item')
def get_search_items(
    search_term: str = Query(..., title='String to search'),
    search_criteria: str = Query(..., title='Criteria to search'),
):
    search_object = SearchQuery(search_term=search_term, search_criteria=search_criteria)
    operator = InventoryOperator()
    cursor = operator.get_search_result(search_object)
    return {'results':list(cursor)}

@api.get('/search/customer')
def get_search_customer(
    search_term: str = Query(..., title='String to search'),
    search_criteria: str = Query(..., title='Criteria to search'),
):
    search_object =SearchQuery(search_term=search_term, search_criteria=search_criteria)
    operator = CustomerOperator()
    cursor = operator.get_search_result(search_object)
    return {'results':list(cursor)}


@api.post('/delete/item')
def delete_item(
    id: str = Query(..., title='id of the item to be deleted'),
):
    operator = InventoryOperator()
    result = operator.delete_item(id)
    return result

@api.post('/delete/customer')
def delete_item(
    id: str = Query(..., title='id of the customer to be deleted'),
):
    operator = CustomerOperator()
    result = operator.delete_customer(id)
    return result

@api.post('/add/item')
def add_item(
    item: Item = Body(...)
):
    operator = InventoryOperator()
    result = operator.add_item(item)
    return result

@api.post('/add/customer')
def add_customer(
    customer: Customer = Body(...)
):
    operator = CustomerOperator()
    result = operator.add_customer(customer)
    return result


@api.get('/supplier')
def get_all_suppliers():
    operator = InventoryOperator()
    result = operator.get_all_suppliers()
    return {'results':list(result)}

@api.get('/detail/item')
def get_item_details(
    id: str = Query(..., title='id of the item to be fetched'),
):
    operator = InventoryOperator()
    result = operator.get_item_details(id)
    return result

@api.get('/detail/customer')
def get_customer_details(
    id: str = Query(..., title='id of the item to be fetched'),
):
    operator = CustomerOperator()
    result = operator.get_customer_details(id)
    return result

@api.post('/edit/item')
def edit_item(
    item: Item = Body(...)
):
    print(item)
    operator = InventoryOperator()
    result = operator.edit_item(item)
    return result

@api.post('/edit/customer')
def edit_customer(
    customer: Customer = Body(...)
):
    operator = CustomerOperator()
    result = operator.edit_customer(customer)
    return result








if __name__ == "__main__":
    uvicorn.run(api)