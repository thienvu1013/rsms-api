from abc import ABC, abstractclassmethod

class QueryBuilder(ABC):
    @abstractclassmethod
    def build_search_query(self, params):
        pass

class MongoQueryBuilder(QueryBuilder):
    def build_search_query(self, params):
        if params.search_criteria == 'id':
            try:
                number_search_term = int(params.search_term)
                query = {params.search_criteria:number_search_term}
            except Exception as e:
                return None
        else:
            query = {params.search_criteria:{"$regex" : f".*{params.search_term}.*",'$options': 'i'}}
        return query