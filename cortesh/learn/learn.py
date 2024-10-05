from cortesh.learn.indexer import Indexer
from cortesh.learn.reader.git import GitReader
from cortesh.process.memory.memory import Memory
from cortesh.learn.explore import Explorer
from tqdm import tqdm

class Learn():
    def __init__(self, llm, logger, config):
        self.llm = llm
        self.logger = logger
        self.config = config
        self.indexer = Indexer(config.db_path, config.folders, config.extensions)
        self.reader = GitReader(llm)
        self.memory = Memory('git')

    def index(self):
        total_files = self.indexer.count_unindexed()
        with tqdm(total=total_files, desc='Indexing Files', unit='file') as pbar:
            self.indexer.index_files(pbar)
        self.process()

    def verify_index(self):
        self.indexer.verify_indexed_files()

    def process(self):
        filename, memoryAddress = self.indexer.get_one()
        print('filename', filename)
        if not filename:
            return
        embeddingText = self.reader.read(filename)
        self.indexer.save_summary(filename, embeddingText)
        if not memoryAddress:
            memoryAddress = self.memory.add(filename, embeddingText)
        else:
            memoryAddress = self.memory.update(memoryAddress, filename, embeddingText)
        self.indexer.save_memory_address(filename, memoryAddress)
        self.indexer.update_index(filename, True)
        self.updateProgress()
        self.process()

    def updateProgress(self):
        remaining_files = self.indexer.count_unindexed()
        self.logger.log('Remaining: ' + str(remaining_files) + ' files to process')

    def explore(self):
        explorer = Explorer()
        while True:
            action = input("Choose an action: load, display, clear, exit: ")
            if action == "load":
                explorer.load_data()
                print("Data loaded.")
            elif action == "display":
                explorer.display_data()
            elif action == "clear":
                explorer.clear_data()
                print("Data cleared.")
            elif action == "exit":
                break
            else:
                print("Invalid action. Please choose again.")