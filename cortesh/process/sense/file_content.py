from cortesh.process.sense.sense import Sense


class FileContent(Sense):
    def instruction(self):
        return '=== REQUEST_FILE_CONTENT:<filename> ==='

    def test(self, response):
        if '=== REQUEST_FILE_CONTENT:' in response:
            return True
        pass

    def read(self, response):
        requested_folder_structures = []
        for line in response.split('\n'):
            if '=== REQUEST_FILE_CONTENT:' in line:
                path = line.split('=== REQUEST_FILE_CONTENT:')[1].strip().split(' ')[0]
                import os

                requested_folder_structures.append( self.read_file(path) )

        return '\n'.join(requested_folder_structures)

    def read_file(self, path):
        import os
        content = ''
        print('- READING FILE: ' + path)
        full_path = os.path.join(os.getcwd(), path)
        try:
            with open(full_path, 'r') as f:
                content = f.read()
        except:
            content = 'File not found'
        # return all in text format

        return 'File: ' + path + '\n\n' + content