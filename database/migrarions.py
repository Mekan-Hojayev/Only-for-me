import sqlite3

def init_database():
    with sqlite3.connect('servers.db') as conn:
        cursor = conn.cursor()
        
        # Create server_logs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT,
            created_at TIMESTAMP,
            avg_latency REAL
        )
        ''')
        
        # Create server_metrics table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_host TEXT,
            server_type TEXT,
            latency REAL,
            check_time TIMESTAMP
        )
        ''')
        
        conn.commit()

if __name__ == "__main__":
    init_database()
    