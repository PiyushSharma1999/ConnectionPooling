
import threading
import mysql.connector
from concurrent.futures import ThreadPoolExecutor

class WaitGroup:
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()
        self.done = threading.Event()
    
    def add(self, n = 1):
        with self.lock:
            self.counter += n
            self.done.clear()
    
    def done_task(self):
        with self.lock:
            self.counter -=1
            if self.counter == 0:
                self.done.set()
    
    def wait(self):
        self.done.wait()

def new_conn():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "******",

    )