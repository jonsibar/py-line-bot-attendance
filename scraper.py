#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import json


# In[2]:

def scrape(login_data):

    login = 'https://sso.universitaspertamina.ac.id/login'
    siup = 'https://siup.universitaspertamina.ac.id/student/home'
    presensi = 'https://siup.universitaspertamina.ac.id/student/attendance'
    elearning = 'https://elearning.universitaspertamina.ac.id/my/'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.6.1546.4'
    }
    
    # In[3]:
    
    
    s = requests.session()
    r = s.get(login, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    login_data['_token']=soup.find('input', attrs={'name':'_token'})['value']
    r = s.post(login, headers = headers, data = login_data)
    r = s.get(siup, headers = headers)
    
    
    # In[4]:
    
    
    r = s.get(presensi, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    soup = soup.findAll('tr', class_ =['even', 'odd'])
    
    
    # In[5]:
    
    
    subject_list = []
    for subject in soup:
        subjects = subject.findAll('td')[1].text
        subject_list.append(subjects)
    
    
    # In[6]:
    
    
    percent_list = []
    for percent in soup:
        percents = percent.findAll('td')[2].text
        percent_list.append(percents)
    
    
    # In[7]:
    
    
    attendance = dict(zip(subject_list, percent_list))
    
    
    # In[8]:
    
    
    attendance = json.dumps(attendance)
    attendance = attendance.replace('{','')
    attendance = attendance.replace('}','')
    attendance = attendance.replace(', ','\n')
    attendance = attendance.replace('"','')
    attendance = attendance.replace('\\u00a0', "-")
    
    
    
    #E-LEARNING:
    r=s.get(elearning, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    courses = soup.findAll('h2', class_='title')
    
    elearning_list = []
    
    for course in courses:
        title = course.a['title']
        elearning_list.append(title+ ', , ') 
        url = course.a['href']
        r=s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, 'lxml')
        soup = soup.findAll('div', class_='activityinstance')
        for file in soup:
            file_name = file.span.text
            file_url = file.a['href']
            if 'File' in file_name and 'resource' in file_url:
                file_name = file_name.replace(' File','')
                elearning_list.append(file_name)
                elearning_list.append(file_url)
        elearning_list.append(', ')

    

    elearning_list = json.dumps(elearning_list)
    elearning_list = elearning_list.replace('[','')
    elearning_list = elearning_list.replace(']','')
    elearning_list = elearning_list.replace(', ','\n')
    elearning_list = elearning_list.replace('"','')






if __name__ == '__main__':
    scrape()