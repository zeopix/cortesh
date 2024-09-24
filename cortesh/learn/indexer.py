import os
import sqlite3
import time

class FileIndexer:
    def __init__(self, db_path, root_folders, extensions):
        self.db_path = db_path
        self.root_folders = root_folders
        self.extensions = extensions
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY,
                    filename TEXT UNIQUE,
                    timestamp REAL,
                    indexed BOOLEAN
                )
            ''')

    def index_files(self):
        for root in self.root_folders:
            for dirpath, _, filenames in os.walk(root):
                for filename in filenames:
                    if filename.endswith(self.extensions):
                        self.update_index(os.path.join(dirpath, filename))

    def update_index(self, filepath):
        timestamp = os.path.getmtime(filepath)
        with self.conn:
            self.conn.execute('''
                INSERT INTO files (filename, timestamp, indexed)
                VALUES (?, ?, ?)
                ON CONFLICT(filename) DO UPDATE SET
                    timestamp=excluded.timestamp,
                    indexed=1
            ''', (filepath, timestamp, True))

    def verify_indexed_files(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT filename, timestamp FROM files WHERE indexed = 1')
        indexed_files = cursor.fetchall()
        for filepath, timestamp in indexed_files:
            if not os.path.exists(filepath) or os.path.getmtime(filepath) != timestamp:
                self.conn.execute('UPDATE files SET indexed = 0 WHERE filename = ?', (filepath,))
        self.conn.commit()

    def close(self):
        self.conn.close()