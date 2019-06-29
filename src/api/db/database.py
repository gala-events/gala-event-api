from enum import Enum


class ConnectionState(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Database:
    __status: ConnectionState
    @property
    def status(self):
        return self.__status.value

    def __init__(self, connection):
        self.connection = connection

    def close(self):
        self.connection.close()

    def __repr__(self):
        connection = "Database"
        return f"Connection to {connection}: {self.status}"
