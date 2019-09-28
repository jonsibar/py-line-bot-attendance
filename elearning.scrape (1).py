#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

# In[3]:


s=requests.Session()
r=s.get(login, headers = headers)
soup = BeautifulSoup(r.content, 'html5lib')
login_data['_token']=soup.find('input', attrs={'name':'_token'})['value']
r=s.post(login, headers = headers, data = login_data)
r=s.get(elearning, headers = headers)
soup = BeautifulSoup(r.content, 'html5lib')
courses = soup.findAll('h2', class_='title')


# In[4]:


for course in courses:
    title = course.a['title']
    path = "D:\Jonathan\Documents\Python\Prototype\{}".format(title)
    try:
        mkdir(path)
    except FileExistsError:
        pass
    url = course.a['href']
    r=s.get(url, headers = headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    soup = soup.findAll('div', class_='activityinstance')
    print(title)
    for file in soup:
        file_name = file.span.text
        file_url = file.a['href']
        if 'File' in file_name and 'resource' in file_url:
            r=s.get(file_url, headers = headers, stream = True)
            file_name = file_name.replace(' File','')
            dest = path + '/' + str(file_name)+ '.pdf'
            chunk_size = 1024
            total_size = int(r.headers['content-length'])
            with open(dest,'wb') as f:
                for data in tqdm(iterable = r.iter_content(chunk_size = chunk_size), desc = str(file_name) + '.pdf', total = total_size/chunk_size, unit = 'KB'):
                    f.write(data)
                f.close()
            


# In[ ]:





# In[ ]:




