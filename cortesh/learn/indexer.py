import os
import sqlite3
import time

class Indexer:
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
                    memoryAddress TEXT UNIQUE,
                    timestamp REAL,
                    indexed BOOLEAN,
                    summary TEXT
                )
            ''')

    def index_files(self):
        for root in self.root_folders:
            # sum current user execution folder
            self.index_folder(root)

    def index_folder(self, path):
        if not path.endswith('/'):
            path = path + '/'
        realpath = os.path.join(os.getcwd(), path)
        # for folders, call index folder recursively, for files call update_index
        for root, dirs, files in os.walk(realpath):
            for file in files:
                 _, extension = os.path.splitext(file)
                 extension = extension[1:]
                 if extension in self.extensions:
                    self.update_index(os.path.join(path, file))
            for dir in dirs:
                if not dir.startswith('.'):
                    self.index_folder(os.path.join(path, dir))
            dirs[:] = []



    def update_index(self, filepath, indexed=False):
        print('Updating index for', filepath)
        real_filepath = os.path.join(os.getcwd(), filepath)
        timestamp = os.path.getmtime(real_filepath)
        summary = ''  # Assuming a method to generate summary
        with self.conn:
            self.conn.execute('''
                INSERT INTO files (filename, timestamp, indexed, summary)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(filename) DO UPDATE SET
                    timestamp=?,
                    indexed=?
            ''', (filepath, timestamp, indexed, summary, timestamp, indexed))

    def generate_summary(self, filepath):
        # Placeholder for summary generation logic
        return "Summary of " + filepath

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

    def get_one(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT filename, memoryAddress FROM files WHERE indexed = 0 LIMIT 1')
        #try catch
        res = cursor.fetchone()
        if res is None:
            print('No files to process')
            return
        print('---res', res)
        filename = res[0]
        memoryAddress = res[1]
        print('--- Found filename', filename)
        print('--- Found memoryAddress', memoryAddress)
        return filename, memoryAddress

    def save_summary(self, filename, summary):
        print('++++Saving summary for', filename)
        with self.conn:
            self.conn.execute('''
                INSERT INTO files (filename, summary)
                VALUES (?, ?)
                ON CONFLICT(filename) DO UPDATE SET
                    summary=?
            ''', (filename, summary, summary))
            print('++++Summary saved for', filename)
    def save_memory_address(self, filename, memoryAddress):
        with self.conn:
            self.conn.execute('''
                INSERT INTO files (filename, memoryAddress)
                VALUES (?, ?)
                ON CONFLICT(filename) DO UPDATE SET
                    memoryAddress=excluded.memoryAddress
            ''', (filename, memoryAddress))

    def count_unindexed(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT filename FROM files WHERE indexed = 0')
        count = len(cursor.fetchall())
        return count