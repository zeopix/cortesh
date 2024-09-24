from cortesh.learn import FileIndexer
from cortesh.learn.reader.git import GitReader


class Learn():
    def __init__(self, llm, logger, config):
        self.llm = llm
        self.logger = logger
        self.config = config
        self.indexer = FileIndexer(config['db_path'], config['root_folders'], config['extensions'])
        self.reader = GitReader(llm)

    def index(self):
        self.indexer.index_files()

    def verify_index(self):
        self.indexer.verify_indexed_files()

    def process(self):
        #get one file from indexer
        filename = self.indexer.get_one()
        embeddingText = self.reader.read(filename)



