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
    def find_by_uuid(db: Database, model_name, uuid: UUID) -> BaseModel:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
        record = CRUD.find(db, model_name, filter_params={"uuid": UUID(uuid)})
        if not record:
            raise Exception("Not Found")
        return record[0]

    @staticmethod
    def create(db: Database, model_name, data: dict) -> UUID:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
        record_id = uuid4()
        data.update(uuid=record_id)
        db[model_name].insert_one(data)
        return record_id

    @staticmethod
    def update(db: Database, model_name, uuid: UUID, data: dict) -> UUID:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
        assert uuid, "UUID not provided"
        db[model_name].update({"uuid": UUID(uuid)}, {"$set": data})
        return CRUD.find_by_uuid(db, model_name, uuid)

    @staticmethod
    def delete(db: Database, model_name, uuid: UUID) -> None:
        assert db, "DB not provided"
        assert model_name, "ModelName not provided"
        assert uuid, "UUID not provided"
        db[model_name].remove({"uuid": UUID(uuid)})
