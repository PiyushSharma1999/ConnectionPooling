import threading
from queue import Queue, Empty
import mysql.connector

class Connection:
    def __init__(self, id, config):
        self.id = id
        self.config = config
        self.conn = self.create()
    
    def create(self):
        return mysql.connector.connect(**self.config)
    
    def close(self):
        if self.conn.is_connected():
            self.conn.close()

class ConnectionPool:
    def __init__(self, max_conn, config):
        self.max_conn = max_conn
        self.pool = Queue(max_conn)
        for i in range(max_conn):
            self.pool.put(Connection(i, config))
    
    def get(self, timeout=None):
        try:
            return self.pool.get(timeout=timeout)
        except Empty:
            raise TimeoutError("No connection available within timeout.")
    
    def put(self, connection):
        self.pool.put(connection)
    
    def close_all(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            conn.close()