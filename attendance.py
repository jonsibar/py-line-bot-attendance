#!/usr/bin/env python
# coding: utf-8

# In[40]:


import requests
from bs4 import BeautifulSoup
import json

# In[41]:


login = 'https://sso.universitaspertamina.ac.id/login'
siup = 'https://siup.universitaspertamina.ac.id/student/home'
attendance = 'https://siup.universitaspertamina.ac.id/student/attendance'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.6.1546.4'
}
login_data = {
    'username':'***REMOVED***',
    'password' : '***REMOVED***'
}


# In[42]:


s = requests.session()
r = s.get(login, headers = headers)
soup = BeautifulSoup(r.content, 'lxml')
login_data['_token']=soup.find('input', attrs={'name':'_token'})['value']
r = s.post(login, headers = headers, data = login_data)
r = s.get(siup, headers = headers)


# In[43]:


r = s.get(attendance, headers = headers)
soup = BeautifulSoup(r.content, 'lxml')
soup = soup.findAll('tr', class_ =['even', 'odd'])


# In[45]:


subject_list = []
for subject in soup:
    subjects = subject.findAll('td')[1].text
    subject_list.append(subjects)


# In[46]:


percent_list = []
for percent in soup:
    percents = percent.findAll('td')[2].text
    percent_list.append(percents)


# In[ ]:
attendance = dict(zip(subject_list, percent_list))
attendance = json.dumps(attendance)
attendance = attendance.replace('{','')
attendance = attendance.replace('}','')
attendance = attendance.replace(',','\n')
attendance = attendance.replace('"','')
attendance = attendance.replace('\\u00a0', "-")
