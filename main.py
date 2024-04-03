import requests
import json
import time

class JobFinder():
    def __init__(self) -> None:
        api_key = 'jS0JuslcnshA8bs3kvdIYw'
        self.headers = {'Authorization': 'Bearer ' + api_key}
        self.api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'
        self.host = 'https://nubela.co/proxycurl'

    def job_scrape(self, search_id:str, job_type:str='anything', experience_level:str='anything', when:str='anytime',flexibility:str='anything',geo_id:str="92000000", keyword:str=None)->list:
        jobs_list=list()
        for i in range(5):
            self.params = {
                'job_type': job_type,
                'experience_level': experience_level,
                'when': when,
                'flexibility': flexibility,
                'geo_id': geo_id,
                'keyword': keyword,
                'search_id': search_id,
                'page':i
            }
            retries = 1
            success = False
            while not success:
                response=requests.get(url=self.api_endpoint,
                                    params=self.params,
                                    headers=self.headers)
                print(response.content)
                if response.status_code==200:
                    dict_data = json.loads(response.content)['job']
                    jobs_list = jobs_list+dict_data
                    success=True
                else:
                    wait = retries * 30
                    print(f'Error! Waiting {wait} secs and re-trying...')
                    time.sleep(wait)
                    retries += 1
            data_dict = json.loads(response.content)
            if data_dict['next_page_no']==None:
                break
        return jobs_list

    def fetch_search_id(self, company_url: str) -> int:
        response = requests.get(
            f'{self.host}/api/linkedin/company', 
            params={'url': company_url},
            headers=self.headers
        )
        return response.json()['search_id']

    def call(self,company_url:str) -> list:
        self.search_id = self.fetch_search_id(url=company_url)
        self.jobs_data = self.job_scrape(str(self.search_id))
        return self.jobs_data