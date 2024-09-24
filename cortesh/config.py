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
            #if not, initialize default values
            self.folders = []
            self.extensions = []
            self.save()

    def load(self):
        with open('.cortesh/config.toml') as f:
            data = toml.load(f)
            self.folders = data['folders']
            self.extensions = data['extensions']

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
