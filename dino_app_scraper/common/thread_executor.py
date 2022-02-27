import concurrent.futures

def getExecutor(numberOfThreads):
    print(f'Creating Executor with {numberOfThreads} threads.')
    return concurrent.futures.ThreadPoolExecutor(max_workers=numberOfThreads)