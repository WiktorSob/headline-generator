import requests
import html
from bs4 import BeautifulSoup
import unicodedata
from unidecode import unidecode
import argparse
import json
import re
import pickle
from random import random, randrange
from time import sleep
import os

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import Popularity
  

class ObtaingDataError(Exception):
    pass

    

def get_website(page_link, random_user_agent = False):
    if random_user_agent:
        user_agent_rotator = UserAgent(popularity = [Popularity.COMMON.value,
                                                Popularity.POPULAR.value],
                                limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        headers = {'User-Agent' : user_agent}
    else:
        headers = None
    response = requests.get(page_link, headers=headers)
    content = response.content.decode('utf-8')
    content = html.unescape(content)
    content = unicodedata.normalize("NFKD", content)
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def find_metadata_json(soup):
    script = soup.find('script', string=re.compile('window.__directoryData'))
    json_text = re.search(r'^\s*window.__directoryData\s*=\s*({.*?})\s*;\s*$',
                        script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    
    return data['items']

def obtain_info(page_link, domain, page):
    page_link = page_link.format(domain = domain, page = page)
    
    print(f'stealing from: {page_link}')
    
    soup = get_website(page_link=page_link)
    json_metadata = find_metadata_json(soup=soup)
    
    page_links = ['https://www.tvp.info' + x['url'] for x in json_metadata]
    page_leads = [ x['lead'] for x in json_metadata]
    page_titles = [ x['title'] for x in json_metadata]
    
    return page_links, page_leads, page_titles

def job(page_link, start_page, end_page, domain):
    result_links, result_leads, result_titles = [], [], []
    failed_counter = 0
    for page in range(int(start_page), int(end_page)+1):
        try:
            page_links, page_leads, page_titles = obtain_info(page_link,
                                                              domain = domain,
                                                              page = page)
            result_links.extend(page_links)
            result_leads.extend(page_leads)
            result_titles.extend(page_titles)
        except:
            if failed_counter == 5:
                print('Failed 5 times. Breaking loop')
                print(f'Last page obtained: {page}')
                break
            else:
                print(f'Failed obtaining page: {page} from domain: {domain}')
                failed_counter += 1
                pass
        # After obtaining data from one page wait for a while between 1-3 sec    
        sleep(random()*randrange(1,3))
    
    res = (result_links, result_leads, result_titles)
    
    with open(f'results/results_{domain}_{start_page}-{end_page}.pkl', 'wb') as f:
        pickle.dump(res, f)
    
    print('-' * 89)
    print('Output file saved in /results')
    
    return result_leads, result_links, result_titles



def main():
    
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
  
if __name__ == '__main__':
    main()