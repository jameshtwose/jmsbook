# Checking which end points function in python

#%%
import requests
from ast import literal_eval
import pandas as pd
import numpy as np
import json
# %%
# This functions
url = "http://127.0.0.1:8000/"
headers = {}
response = requests.request("GET", url, headers=headers)
welcome_df = pd.DataFrame(literal_eval(response.text), index=[0])
welcome_df
# %%
# This functions
url = "http://127.0.0.1:8000/login/"
headers = {}
response = requests.request("POST", 
                            url, 
                            headers=headers,
                            data={"username": "jms3@gmail.com", 
                                  "password": "pass12345"})
login_df = pd.DataFrame(literal_eval(response.text), index=[0])
login_df
# response.text

#%%
# This functions (make sure to update email and password)
url = "http://127.0.0.1:8000/users/"
headers = {}
response = requests.request("POST", 
                            url, 
                            headers=headers,
                            json={"email": "jms3@gmail.com", 
                                  "password": "pass12345"})
response.text

#%%
# This functions
users = list()
for id in range(20):
    url = f"http://127.0.0.1:8000/users/{id}"
    headers = {}
    response = requests.request("GET", 
                                url, 
                                headers=headers)
    if str(response) == "<Response [200]>":
        users.append(pd.DataFrame(literal_eval(response.text), index=[0]))
pd.concat(users)

#%%
# This functions
url = "http://127.0.0.1:8000/posts/"
headers = {'Authorization': f'Bearer {login_df["access_token"].iloc[0]}'}
response = requests.request("POST", 
                            url, 
                            headers=headers,
                            json={"title": "This is a super cool new post", 
                                  "content": f"Oh damn, look a random number: {round(np.random.random(), 2)}"})
response.text

#%%
# This functions
url = "http://127.0.0.1:8000/posts/"
headers = {'Authorization': f'Bearer {login_df["access_token"].iloc[0]}'}
response = requests.request("GET", 
                            url, 
                            headers=headers)

(pd.concat([pd.DataFrame(x) for x in json.loads(response.text)])
 .reset_index()
 .drop(["index", "owner"], axis=1)
 .drop_duplicates()
 )

# %%
# This functions
id = 18
url = f"http://127.0.0.1:8000/posts/{id}"
headers = {'Authorization': f'Bearer {login_df["access_token"].iloc[0]}'}
response = requests.request("GET", 
                            url, 
                            headers=headers)

json.loads(response.text)

#%%
# This functions
id = 18
url = f"http://127.0.0.1:8000/posts/{id}"
headers = {'Authorization': f'Bearer {login_df["access_token"].iloc[0]}'}
response = requests.request("DELETE", 
                            url, 
                            headers=headers)

response.text