from utils import get_website, get_content
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import time
import pickle
import argparse

def main():

    parser = argparse.ArgumentParser(description="Argument parser")
    parser.add_argument("--pages", type = int, default = 100)
    args = parser.parse_args()
    
    with open('articles_metadata/articles_links_clean.pkl', 'rb') as f:
        links = pickle.load(f)

    with open('articles_metadata/articles_ids_clean.pkl', 'rb') as f:
        ids = pickle.load(f)
    
    with open('obtain_content/log.pkl', 'rb') as f:
        log = pickle.load(f)

    with open('obtain_content/full_content.pkl', 'rb') as f:
        full_content = pickle.load(f)
        
    print(f'current len of content: {len(full_content)}')
    
    checkpoint = log['checkpoint']
    
    print(f'starting from page: {checkpoint}')
    start = time()

    with ProcessPoolExecutor() as executor:
        res = list(executor.map(get_content,
                                links[checkpoint : checkpoint + args.pages],
                                ids[checkpoint : checkpoint + args.pages]))
        
    full_content.extend(res)    
    
    end = time()
    
    log['checkpoint'] = checkpoint + args.pages + 1
    
    print(f'last obtained page: {checkpoint + args.pages}')
    
    with open('obtain_content/log.pkl', 'wb') as f:
        pickle.dump(log, f)    
    
    with open('obtain_content/full_content.pkl', 'wb') as f:
        pickle.dump(full_content, f)
    
    
    print(f'exec time: {end-start:.3f}s')
    print()
if __name__ == '__main__':
    main()