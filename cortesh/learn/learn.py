class Learn():
    def __init__(self, llm, logger, config):
        self.llm = llm
        self.logger = logger
        self.config = config
        self.indexer = FileIndexer(config['db_path'], config['root_folders'], config['extensions'])

    def index(self):
        self.indexer.index_files()

    def verify_index(self):
        self.indexer.verify_indexed_files()