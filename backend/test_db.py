import psycopg2
import time

def test_connection():
    try:
        conn = psycopg2.connect(
            host="db",
            database="siva",
            user="admin",
            password="Database@siva",
            port=5432,
            connect_timeout=5
        )
        print("✅ Successfully connected to database!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    for i in range(5):
        if test_connection():
            break
        print(f"Retry {i+1}/5...")
        time.sleep(2)
