from utils import get_website, get_content
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import time
import pickle

with open('articles_metadata/articles_links.pkl', 'rb') as f:
    links = pickle.load(f)



if __name__ == '__main__':
    start = time()

    with ProcessPoolExecutor(1) as executor:
        res = list(executor.map(get_content, links[:20]))

    end = time()
    print(f'exec time: {end-start:.3f}s')

