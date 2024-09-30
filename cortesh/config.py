import os
import toml

#load .cortesh/index.toml if exists, if not, initialitze default values for it

class Config():
    def __init__(self):
        #check file existence
        os.path.exists('.cortesh/config.toml')
        #if exists, load it
        if os.path.exists('.cortesh/config.toml'):
            self.load()
        else:
            print("which folders do you want to index? use asterisk for all, or comma separated values.")
            folders = input("> ")
            print("which extensions do you want to index? use asterisk for all, or comma separated values.")
            extensions = input("> ")

            #if not, initialize default values
            self.folders = folders.split(',')
            self.extensions = extensions.split(',')
            self.db_path = '.cortesh/index.db'
            self.save()
        

    def load(self):
        with open('.cortesh/config.toml') as f:
            data = toml.load(f)
            self.folders = data['folders']
            self.extensions = data['extensions']
            self.db_path = data['db_path']  if 'db_path' in data else '.cortesh/index.db'

    def save(self):
        with open('.cortesh/config.toml', 'w') as f:
            f.write(toml.dumps({'folders': self.folders, 'extensions': self.extensions}))

    def set_folders(self, folders):
        self.folders = folders
        self.save()

    def set_extensions(self, extensions):
        self.extensions = extensions
        self.save()

    def get_folders(self):
        return self.folders

    def get_extensions(self):
        return self.extensions
