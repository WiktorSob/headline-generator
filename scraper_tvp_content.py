from utils import get_website, get_content
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import time
import pickle
import argparse
from time import sleep
from random import random, randint, choices


def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '▮' * int(percent) + '-' * (100 - int(percent))
    print(f'|{bar}| {percent:.2f}%')
    
    
def batch(batch_size):
    """
    calls function for obtaining content from given link.
    """
    
    # open links and ids to keep data related after multiprocessing
    with open('articles_metadata/articles_links_clean.pkl', 'rb') as f:
        links = pickle.load(f)

    # with open('articles_metadata/articles_ids_clean.pkl', 'rb') as f:
    #     ids = pickle.load(f)
    
    with open('articles_metadata/articles_headlines_clean.pkl', 'rb') as f:
        headlines = pickle.load(f)
        
    with open('articles_metadata/articles_titles_clean.pkl', 'rb') as f:
        titles = pickle.load(f)
    
    # open log file with checkpoint - last obtaineg link
    with open('obtain_content/log.pkl', 'rb') as f:
        log = pickle.load(f)

    #open file with already obtained content for appending new pages
    with open('obtain_content/full_content.pkl', 'rb') as f:
        full_content = pickle.load(f)
        
    print(f'current len of content: {len(full_content)}')
    
    checkpoint = log['checkpoint']
    
    print(f'starting from page: {checkpoint}')
    start = time()

    # launch function
    with ProcessPoolExecutor() as executor:
        res = list(executor.map(get_content,
                                links[checkpoint : checkpoint + batch_size],
                                titles[checkpoint : checkpoint + batch_size],
                                headlines[checkpoint : checkpoint + batch_size]))
        
    full_content.extend(res)    
    
    end = time()
    
    print(f'last obtained page: {checkpoint + batch_size}')
    
    # save last obtained page id to logs as a starting point for another call
    log['checkpoint'] = checkpoint + batch_size
    
    with open('obtain_content/log.pkl', 'wb') as f:
        pickle.dump(log, f)    
    
    with open('obtain_content/full_content.pkl', 'wb') as f:
        pickle.dump(full_content, f)
    
    
    print(f'exec time: {end-start:.3f}s')

def main():
 
    parser = argparse.ArgumentParser(description="Argument parser")
    parser.add_argument("--batch_size", type = int, default = 50, help = 'number of pages to download in one batch')
    parser.add_argument("--n_batches", type = int, default = 5, help = 'number of batches')
    args = parser.parse_args()   

    batch_size = args.batch_size
    n_batches = args.n_batches
    
    for progress, i in enumerate(range(1, n_batches+1)):
        batch(batch_size = batch_size)
        progress_bar(progress + 1, n_batches)
        print(f'finished batch: {i}')
        
        if i < n_batches: 
            sleep_time = randint(1,30) * random() + choices(population = [0, 300, 600], weights = [0.96, 0.035, 0.005])[0]
            print(f'Cooldown time: {sleep_time:.3f}s')
            sleep(sleep_time)
        
if __name__ == '__main__':
    main()