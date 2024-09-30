from cortesh.learn import FileIndexer
from cortesh.learn.reader.git import GitReader
from cortesh.process.memory.memory import Memory


class Learn():
    def __init__(self, llm, logger, config):
        self.llm = llm
        self.logger = logger
        self.config = config
        self.indexer = FileIndexer(config.db_path, config.folders, config.extensions)
        self.reader = GitReader(llm)
        self.memory = Memory('git')

    def index(self):
        self.indexer.index_files()
        self.process()

    def verify_index(self):
        self.indexer.verify_indexed_files()

    def process(self):
        filename, memoryAddress = self.indexer.get_one()
        print('filename', filename)
        if not filename:
            return
        embeddingText = self.reader.read(filename)
        print('embeddingText')
        print(embeddingText)
        self.indexer.save_summary( filename, embeddingText )
        if not memoryAddress:
            memoryAddress = self.memory.add(filename, embeddingText )
        else:
            memoryAddress = self.memory.update( memoryAddress, filename, embeddingText )
        self.indexer.save_memory_address( filename, memoryAddress )
        self.indexer.update_index( filename, True )
        self.updateProgress()
        self.process()

    def updateProgress(self):
    
        self.logger.log('Remaining: ' + str(self.indexer.count_unindexed()) + ' files to process')