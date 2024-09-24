from cortesh.brain.sense.sense import Sense


class FolderStructure(Sense):
    def instruction(self):
        return '=== REQUEST_FOLDER_STRUCTURE:<foldername> === - Use a . to indicate the current folder, it will not display nested folders, make sure to make subsequent requests for nested folders before writing the response.'

    def test(self, response):
        if '=== REQUEST_FOLDER_STRUCTURE:' in response:
            return True
        pass

    def read(self, response):
        requested_folder_structures = []
        for line in response.split('\n'):
            if '=== REQUEST_FOLDER_STRUCTURE:' in line:
                path = line.split('=== REQUEST_FOLDER_STRUCTURE:')[1].strip().split(' ')[0]
                print('- READING FOLDER: ' + path)
                requested_folder_structures.append( self.read_folder(path) )

        return '\n'.join(requested_folder_structures)

    def read_folder(self, path):
        import os
        folders = []
        files = []
        #append current path
        full_folder_path = os.path.join(os.getcwd(), path)
        print('---PATH---', full_folder_path)
        try:
            for item in os.listdir(full_folder_path):
                full_path = os.path.join(path, item)
                print('---FULL PATH---', full_path)
                if os.path.isdir(full_path):
                    folders.append( ' - [Folder] - ' + full_path)
                elif os.path.isfile(full_path):
                    files.append( ' - [File] - ' + full_path)
            r = '=== REQUEST_FOLDER_STRUCTURE:' + path + ' ===\n' + '\n'.join(folders) + '\n' + '\n'.join(files)
        except:
            r = '=== REQUEST_FOLDER_STRUCTURE:' + path + ' ===\n' + 'Folder not found'
        # return all in text format
        return r