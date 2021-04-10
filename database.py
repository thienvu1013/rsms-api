from abc import ABC, abstractclassmethod
from .query_builder import MongoQueryBuilder
import pymongo
import urllib.parse
import ssl
import os
# import os
# import sys
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

class DBConnector(ABC):
    @abstractclassmethod
    def connect(self):
        pass

class DBOperator(ABC):
    @abstractclassmethod
    def get_search_result(self, query):
        pass

class MongoConnector(DBConnector):
    def __init__(self):
        """Constructor to MongoConnector

        Args:
            connectionString (String): the connection string
            username (String): the username to the database 
            password (String): the password to the database
        """
        # self.connectionString = os.environ.get('CONNECTION_STRING_VIP_MONGODB')
        # self.username = os.environ.get('USERNAME_VIP_MONGODB')
        # self.password = os.environ.get('PASSWORD_VIP_MONGODB')

        self.connectionString = os.environ.get('RSMS_CONNECTION_STRING')
        self.username = os.environ.get('RSMS_USERNAME')
        self.password = os.environ.get('RSMS_PASSWORD')


    def connect(self):
        """create connection to the given connection string
        """

        try:
            username = urllib.parse.quote_plus(self.username)
            password = urllib.parse.quote_plus(self.password)
            self.client = pymongo.MongoClient(
                self.connectionString % (username, password))
        except Exception as e:
            msg = 'Connection error'
            try:
                self.client = pymongo.MongoClient(self.connectionString)
            except Exception as e:
                msg = 'Connection error'
                print(e)
                raise ConnectionError(msg)


    def getClient(self):
        """return the Client object from mongodb

        Returns:
            MongoClient: the client of the database
        """
        return self.client


    def close(self):
        self.client.close()


class InventoryOperator(DBOperator):
    def __init__(self):
        self.database = 'rsms'
        self.item_collection = 'items'
        self.supplier_collection = 'suppliers'
    
    def get_search_result(self, query):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.item_collection]

        query_builder = MongoQueryBuilder()
        query_expression = query_builder.build_search_query(query)

        try:
            cursor = collection.find(query_expression,{'_id': 0 })
        except Exception as e:
            raise RuntimeError('Search request failed')
        finally:
            connector.close()

        return cursor

    def delete_item(self, id):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.item_collection]

        try:
            result = collection.delete_one({'id': int(id)})
            return {"message":"item removed",'id':id}
        except Exception as e:
            raise RuntimeError('delete request failed')
        finally:
            connector.close()

    def get_all_suppliers(self):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.supplier_collection]
        try:
            result = collection.find({},{'_id': 0 })
            return result
        except Exception as e:
            raise RuntimeError('find supplier request failed')
        finally:
            connector.close()

    def add_item(self, item):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.item_collection]
        try:
            highestID = list(collection.find({}).sort('id',-1).limit(1))[0]['id']
            item.id = highestID+1
            result = collection.insert_one(item.dict())
            return {"message":"successfully added item"}
        except Exception as e:
            # raise RuntimeError('failed to add item')
            print(e)
            return {"message":"failed to added item"}
        finally:
            connector.close()

            # result = collection.

    def get_item_details(self,id):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.item_collection]
        try:
            result ={}
            item = collection.find({'id':int(id)},{'_id': 0 })
            result['item']=list(item)[0]
            supplier_id = int(result['item']['supplier'])
            collection = connector.getClient()[self.database][self.supplier_collection]
            supplier = collection.find({'id':supplier_id},{'_id': 0 })
            result['supplier']=list(supplier)[0]
            return result
        except Exception as e:
            raise RuntimeError('find supplier request failed')
        finally:
            connector.close()

    def edit_item(self, item):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.item_collection]
        try:
            result = collection.update_one({'id':item.id},{"$set":{'name':item.name, 'qty':item.qty, 'price':item.price}})
            print(result)
            return {"message":"successfully edited item"}
        except Exception as e:
            # raise RuntimeError('failed to add item')
            print(e)
            return {"message":"failed to added item"}
        finally:
            connector.close()


class CustomerOperator(DBOperator):
    def __init__(self):
        self.database = 'rsms'
        self.customer_collection = 'customers'

    def get_search_result(self, query):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.customer_collection]

        query_builder = MongoQueryBuilder()
        query_expression = query_builder.build_search_query(query)

        try:
            cursor = collection.find(query_expression,{'_id': 0 })
        except Exception as e:
            raise RuntimeError('Search request failed')
        finally:
            connector.close()

        return cursor
    
    def delete_customer(self, id):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.customer_collection]

        try:
            result = collection.delete_one({'id': int(id)})
            return {"message":"customer removed",'id':id}
        except Exception as e:
            raise RuntimeError('delete request failed')
        finally:
            connector.close()

    def add_customer(self, customer):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.customer_collection]
        try:
            highestID = list(collection.find({}).sort('id',-1).limit(1))[0]['id']
            customer.id = highestID+1
            result = collection.insert_one(customer.dict())
            return {"message":"successfully added item"}
        except Exception as e:
            # raise RuntimeError('failed to add item')
            print(e)
            return {"message":"failed to added item"}
        finally:
            connector.close()

    def get_customer_details(self, id):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.customer_collection]

        try:
            cursor = collection.find({'id':int(id)},{'_id': 0 })
        except Exception as e:
            raise RuntimeError('Search request failed')
        finally:
            connector.close()

        return {'customer':list(cursor)[0]}

    def edit_customer(self, customer):
        connector = MongoConnector()
        connector.connect()
        collection = connector.getClient()[self.database][self.customer_collection]
        try:
            result = collection.update_one({'id':customer.id},{"$set":{'first_name':customer.first_name, 'last_name':customer.last_name, 'address':customer.address, 'postal':customer.postal, 'phone': customer.phone, 'customer_type':customer.customer_type}})
            return {"message":"successfully edited customer"}
        except Exception as e:
            # raise RuntimeError('failed to add item')
            print(e)
            return {"message":"failed to added customer"}
        finally:
            connector.close()

    


if __name__=="__main__":
    i = InventoryOperator()
    i.add_item({})


