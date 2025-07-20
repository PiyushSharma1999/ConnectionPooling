from benchmark import benchmark_non_pool, benchmark_pool
import mysql.connector

if __name__ == "__main__":
    config = {
        "connector": mysql.connector.connect,
        "params": {
            "host": "localhost",
            "user": "root",
            "password": "Spoison@911",
            "database": "testDB"
        }
    }

    benchmark_non_pool(config)
    benchmark_pool(config)