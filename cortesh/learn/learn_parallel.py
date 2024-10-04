from cortesh.learn.indexer import Indexer
from cortesh.learn.reader.git import GitReader
from cortesh.process.memory.memory import Memory
from cortesh.learn.explore import Explorer
import concurrent.futures

class LearnParallel():
    def __init__(self, llm, logger, config):
        self.llm = llm
        self.logger = logger
        self.config = config
        self.indexer = Indexer(config.db_path, config.folders, config.extensions)
        self.reader = GitReader(llm)
        self.memory = Memory('git')

    def index(self):
        self.indexer.index_files()
        self.process()

    def verify_index(self):
        self.indexer.verify_indexed_files()

    def process(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            while True:
                filename, memoryAddress = self.indexer.get_one_random()
                if not filename:
                    break
                futures.append(executor.submit(self.process_file, filename, memoryAddress))
            concurrent.futures.wait(futures)

    def process_file(self, filename, memoryAddress):
        print('Processing file:', filename)
        embeddingText = self.reader.read(filename)
        print('embeddingText')
        print(embeddingText)
        self.indexer.save_summary(filename, embeddingText)
        if not memoryAddress:
            memoryAddress = self.memory.add(filename, embeddingText)
        else:
            memoryAddress = self.memory.update(memoryAddress, filename, embeddingText)
        self.indexer.save_memory_address(filename, memoryAddress)
        self.indexer.update_index(filename, True)
        self.updateProgress()

    def updateProgress(self):
        self.logger.log('Remaining: ' + str(self.indexer.count_unindexed()) + ' files to process')

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