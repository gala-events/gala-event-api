from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel
from .database import Database


class CRUD:

    @staticmethod
    def find(db: Database, model_name, skip: int = 0, limit: int = 25, filter_params: dict = None, sort: List[str] = None) -> List[BaseModel]:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
        if not filter_params:
            filter_params = dict()
        if not sort:
            sort = []

        sort_params = []
        for param in sort:
            direction = 1 if param and param[0] == "-" else -1
            sort_params.append((param, direction))

        cursor = db[model_name].find(filter_params).limit(limit)
        if sort_params:
            cursor = cursor.sort(sort_params)
        data = [record for record in cursor]
        return data

    @staticmethod
    def find_by_id(db: Database, model_name, id: UUID) -> BaseModel:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
        record = CRUD.find(db, model_name, filter_params={"uuid": id})
        if not record:
            raise Exception("Not Found")
        return record[0]

    @staticmethod
    def create(db: Database, model_name, data: dict) -> UUID:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
        record_id = uuid4()
        data.update(uuid=record_id)
        result = db[model_name].insert_one(data)
        print(result)
        return record_id

    @staticmethod
    def update(db: Database, model_name, id: UUID, data: dict) -> UUID:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"

    @staticmethod
    def delete(db: Database, model_name, id: UUID) -> None:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
