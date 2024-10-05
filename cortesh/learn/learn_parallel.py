from cortesh.learn.indexer import Indexer
from cortesh.learn.reader.git import GitReader
from cortesh.process.memory.memory import Memory
from cortesh.learn.explore import Explorer
import concurrent.futures
from tqdm import tqdm


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
        total_files = self.indexer.count_unindexed()
        with tqdm(total=total_files, desc='Indexing Files', unit='file') as pbar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                embedding_texts = {}
                unindexed_files = self.indexer.get_unindexed()
                memory_addresses = {}
                for filename, memoryAddress in unindexed_files:
                    if not filename:
                        break
                    memory_addresses[filename] = memoryAddress
                    futures.append(executor.submit(self.process_file, filename, memoryAddress, pbar, embedding_texts))
                for future in concurrent.futures.as_completed(futures):
                    filename, embeddingText = future.result()
                    memoryAddress = memory_addresses[filename]
                    if not memoryAddress:
                        memoryAddress = self.memory.add(filename, embeddingText)
                    else:
                        memoryAddress = self.memory.update(memoryAddress, filename, embeddingText)
                    if memoryAddress:
                        self.indexer.save_memory_address(filename, memoryAddress)
                        self.indexer.save_summary(filename, embeddingText)
                    pbar.update(1)

    def process_file(self, filename, memoryAddress, pbar, embedding_texts):
        embeddingText = self.reader.read(filename)
        return filename, embeddingText
        

    def updateProgress(self, pbar):
        pbar.update(1)
        print('Remaining: ' + str(self.indexer.count_unindexed()) + ' files to process')

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