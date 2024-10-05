import os
import sqlite3
import time
import random
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
    def get_one_random(self):
        unindexed_files = self.get_unindexed()
        if not unindexed_files:
            return None, None
        filename, memoryAddress = random.choice(unindexed_files)
        
        return filename, memoryAddress

    def index_files(self):
        updated_files = 0
        print('Indexing files...')
        for root in self.root_folders:
            # sum current user execution folder
            updated_files += self.index_folder(root)
        print('Updated ', updated_files, ' files')

    def index_folder(self, path, count=0):
        if not path.endswith('/'):
            path = path + '/'
        realpath = os.path.join(os.getcwd(), path)
        # for folders, call index folder recursively, for files call update_index
        for root, dirs, files in os.walk(realpath):
            for file in files:
                 _, extension = os.path.splitext(file)
                 extension = extension[1:]
                 if extension in self.extensions:
                    count += 0 if self.update_index(os.path.join(path, file)) else 1
            for dir in dirs:
                if not dir.startswith('.'):
                    count += self.index_folder(os.path.join(path, dir))
            dirs[:] = []
        return count



    def update_index(self, filepath, indexed=False):
        
        real_filepath = os.path.join(os.getcwd(), filepath)
        timestamp = os.path.getmtime(real_filepath)
        summary = ''  # Assuming a method to generate summary
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('SELECT timestamp, memoryAddress FROM files WHERE filename = ?', (filepath,))
            row = cursor.fetchone()
            if row:
                stored_timestamp, memoryAddress = row
                if timestamp <= stored_timestamp and memoryAddress is not None:
                    indexed = True
            self.conn.execute('''
                INSERT INTO files (filename, timestamp, indexed, summary)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(filename) DO UPDATE SET
                    timestamp=excluded.timestamp,
                    indexed=excluded.indexed
            ''', (filepath, timestamp, indexed, summary))
        return indexed

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
            return
        filename = res[0]
        memoryAddress = res[1]
        
        return filename, memoryAddress

    def save_summary(self, filename, summary):
        
        with self.conn:
            try:
                self.conn.execute('''
                    INSERT INTO files (filename, summary, indexed)
                    VALUES (?, ?, ?)
                    ON CONFLICT(filename) DO UPDATE SET
                        summary=?,
                                indexed=?
                ''', (filename, summary, True, summary, True))
            except sqlite3.IntegrityError:
                print('Error saving summary for', filename)
            except Exception as e:
                print('Error saving summary for', filename)
                print(e)
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

    def get_unindexed(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT filename, memoryAddress FROM files WHERE indexed = 0')
        count = cursor.fetchall()
        return count