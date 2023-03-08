from utils import job

from time import time
import argparse
import os

def main():
    
    start_time = time()
    parser = argparse.ArgumentParser(description="Argument parser")
    parser.add_argument("--domain", type = str, default = 'biznes')
    parser.add_argument("--start_page", type = int, default = 1)
    parser.add_argument("--end_page", type = int, default = 1)
    args = parser.parse_args()
    
    tvp_link = 'https://www.tvp.info/{domain}?page={page}'

    save_path = os.getcwd() + '/results'
    if os.path.exists(save_path) == False:
        os.makedirs(save_path)

    job(page_link = tvp_link,
        start_page=args.start_page,
        end_page=args.end_page,
        domain = args.domain)
    
    end_time = time()
    n_pages = args.end_page - args.start_page + 1
    exec_time = (end_time - start_time)/60
    print(f"Obtaining {n_pages} pages took:")
    print(f"{(exec_time):.3f} minutes")
    print(f"average time per page: {(exec_time/n_pages):.3f} min")
    
if __name__ == '__main__':
    main()