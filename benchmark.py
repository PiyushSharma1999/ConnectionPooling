import time
import threading
from concurrent.futures import ThreadPoolExecutor
from connection_pool import ConnectionPool

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
            self.counter -= 1
            if self.counter == 0:
                self.done.set()

    def wait(self):
        self.done.wait()

def new_conn(config):
    return config['connector'](**config['params'])

def task_without_pool(wg, config):
    try:
        db = new_conn(config)
        cursor = db.cursor()
        cursor.execute("SELECT SLEEP(0.01);")
        cursor.fetchall()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error' {e}")
    finally:
        wg.done_task()

def task_with_pool(wg, pool):
    try:
        conn = pool.get()
        cursor = conn.conn.cursor()
        cursor.execute("SELECT SLEEP(0.01);")
        cursor.fetchall()
        cursor.close()
        pool.put(conn)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        wg.done_task()

def benchmark_non_pool(config):
    wg = WaitGroup()
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=300) as executor:
        for _ in range(300):
            wg.add()
            executor.submit(task_without_pool, wg, config)
    wg.wait()
    print(f"Benchmark (No Pool): {time.time() - start_time:.2f} sec")

def benchmark_pool(config):
    wg = WaitGroup()
    pool = ConnectionPool(20, config["params"])
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=300) as executor:
        for _ in range(300):
            wg.add()
            executor.submit(task_with_pool, wg, pool)
    wg.wait()
    pool.close_all()
    print(f"Benchmark (With Pool): {time.time() - start_time:.2f} sec")
