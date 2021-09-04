import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_BASE_URL = 'https://graph.facebook.com/v11.0'      # APIのバージョンを指定
BUSINESS_ACCOUNT_ID = os.getenv('BUSINESS_ACCOUNT_ID') # ビジネスアカウントID
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')               # アクセストークン

class InstagramGraphApi:
    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.business_account_id = BUSINESS_ACCOUNT_ID
        self.access_token = ACCESS_TOKEN
    
    # ユーザーを取得
    def get_user(self, username, fields):
        return requests.get('{api_base_url}/{business_account_id}?fields=business_discovery.username({username}){{{fields}}}&access_token={access_token}'
                   .format(
                       api_base_url = self.api_base_url,
                       business_account_id = self.business_account_id,
                       username = username,
                       fields = fields,
                       access_token = self.access_token
                   )).json()['business_discovery']

    # メディアを取得
    def get_media(self, username, fields):
        ret_data = []
        
        res = requests.get('{api_base_url}/{business_account_id}?fields=business_discovery.username({username}){{media{{{fields}}}}}&access_token={access_token}'
                  .format(
                      api_base_url = self.api_base_url,
                      business_account_id = self.business_account_id,
                      username = username,
                      fields = fields,
                      access_token = self.access_token
                  )).json()['business_discovery']
        
        for i in range(len(res['media']['data'])):
            ret_data.append(res['media']['data'][i])

        # Instagram Graph APIの仕様上、一度のリクエストで取得できるのは25件までなので、それ以上取得したい場合は複数回リクエストを送る        
        if 'after' in res['media']['paging']['cursors'].keys():
            after = res['media']['paging']['cursors']['after']
            
            while after is not None:
                res = requests.get('{api_base_url}/{business_account_id}?fields=business_discovery.username({username}){{media.after({after}){{{fields}}}}}&access_token={access_token}'
                          .format(
                              api_base_url = self.api_base_url,
                              business_account_id = self.business_account_id,
                              username = username,
                              after = after,
                              fields = fields,
                              access_token = self.access_token
                          )).json()['business_discovery']

                for i in range(len(res['media']['data'])):
                    ret_data.append(res['media']['data'][i])
                
                if 'after' in res['media']['paging']['cursors'].keys():
                    after = res['media']['paging']['cursors']['after']
                else:
                    after = None

        return ret_data
    
    # インサイト（ユーザー）を取得
    def get_user_insight(self, metric, period):
        return requests.get('{api_base_url}/{business_account_id}/insights?metric={metric}&period={period}&access_token={access_token}'
		           .format(
					   api_base_url = self.api_base_url,
					   business_account_id = self.business_account_id,
					   metric = metric,
                       period = period,
					   access_token = self.access_token
		           )).json()['data']
    
    # インサイト（メディア）を取得
    def get_media_insight(self, media_id, metric):
        return requests.get('{api_base_url}/{media_id}/insights?metric={metric}&access_token={access_token}'
		           .format(
					   api_base_url = self.api_base_url,
					   media_id = media_id,
					   metric = metric,
					   access_token = self.access_token
				   )).json()['data']
