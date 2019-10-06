#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import json
import urllib3
from datetime import datetime, timedelta
urllib3.disable_warnings()

# In[2]:

def presensi(login_data):

    login = 'https://sso.universitaspertamina.ac.id/login'
    siup = 'https://siup.universitaspertamina.ac.id/student/home'
    presensi = 'https://siup.universitaspertamina.ac.id/student/attendance'
    elearning = 'https://elearning.universitaspertamina.ac.id/my/'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.6.1546.4'
    }
    
    # In[3]:
    global attendance
    
    
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
    
    
    
def mats(login_data):

    login = 'https://sso.universitaspertamina.ac.id/login'
    siup = 'https://siup.universitaspertamina.ac.id/student/home'
    presensi = 'https://siup.universitaspertamina.ac.id/student/attendance'
    elearning = 'https://elearning.universitaspertamina.ac.id/my/'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.6.1546.4'
    }
    

    global elearning_list
    
    
    s = requests.session()
    r = s.get(login, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    login_data['_token']=soup.find('input', attrs={'name':'_token'})['value']
    r = s.post(login, headers = headers, data = login_data)
    

    r = s.get(elearning, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    courses = soup.findAll('h2', class_='title')
    
    elearning_list = []
    
    
    for course in courses:
        files = []
        title = course.a['title']
        files.append(title) 
        url = course.a['href']
        r=s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, 'lxml')
        soup = soup.findAll('div', class_='activityinstance')
        for file in soup:
            file_name = file.span.text
            file_url = file.a['href']
            if 'File' in file_name and 'resource' in file_url:
                file_name = file_name.replace(' File','')
                files.append(file_name)
                files.append(file_url)
        output = str(files)
        output = output.replace(', ','\n')
        output = output.replace('"','')
        output = output.replace("'",'')
        output = output.replace('[','')
        output = output.replace(']','')
        elearning_list.append(output)


def ujian(login_data):
    global jadwal

    login = 'https://sso.universitaspertamina.ac.id/login'
    siup = 'https://siup.universitaspertamina.ac.id/student/home'
    kalender = 'https://siup.universitaspertamina.ac.id/calendar/viewCalendar'
    
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.6.1546.4'
    }
    s = requests.session()
    r = s.get(login, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    login_data['_token']=soup.find('input', attrs={'name':'_token'})['value']
    r = s.post(login, headers = headers, data = login_data)
    r = s.get(siup, headers = headers)
    r = s.get(kalender, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    soup = soup.findAll('tbody')[2]
    jadwal = soup.get_text(strip=True, separator='</td><td>').replace('</td><td>','\n')



def bolos(login_data):
    global absen_list
    
    login = 'https://sso.universitaspertamina.ac.id/login'
    siup = 'https://siup.universitaspertamina.ac.id/student/home'
    presensi = 'https://siup.universitaspertamina.ac.id/student/attendance'
    elearning = 'https://elearning.universitaspertamina.ac.id/my/'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.6.1546.4'
    }
    
    
    
    s = requests.session()
    r = s.get(login, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    login_data['_token']=soup.find('input', attrs={'name':'_token'})['value']
    r = s.post(login, headers = headers, data = login_data)
    r = s.get(siup, headers = headers)
    
    
    
    r = s.get(presensi, headers = headers)
    soup = BeautifulSoup(r.content, 'lxml')
    soup = soup.findAll('tr', class_ =['even', 'odd'])
    
    
    subject_list = []
    for subject in soup:
        subjects = subject.findAll('td')[1].text
        subject_list.append(subjects)
    
    
    ra=soup[0].find('input', {'name':'ra'})['value']
    k=[]
    for value in soup:
        k.append(value.find('input', {'name':'k'})['value'])
    subject_dict=dict(zip(k, subject_list))
    
    
    absen_list=[]
    
    for i in k:
        dates=[]
        kh=[]
        url = 'https://siup.universitaspertamina.ac.id/student/attendanceDetail?ra='+ra+'&k='+i
        r=s.get(url, headers = headers)
        soup = BeautifulSoup(r.content, 'lxml')
        soup = soup.findAll('tr', class_ =['even', 'odd'])
        for tr in soup:
            det=tr.td
            det=det.get_text(strip=True)
            det=datetime.strptime(det, '%Y-%m-%d').date()
            dates.append(det)
            if tr.findAll('li', class_='next'):
                soup=tr.findAll('li', class_='next')
                url = soup2.a['href']
                r = s.get(url, headers = headers)
                soup = BeautifulSoup(r.content, 'lxml')
                soup = soup.findAll('tr', class_ =['even', 'odd'])
                for tr in soup:
                    det=tr.td
                    det=det.get_text(strip=True)
                    det=datetime.strptime(det, '%Y-%m-%d').date()
                    dates.append(det)
        dates=sorted(dates)
        if abs(dates[1] - dates[0]) < timedelta(days=7) or abs(dates[2] - dates[1] < timedelta(days=7) or abs(dates[3] - dates[2] < timedelta(days=7):
            cpw=2
            alimit=6
        else:
            cpw=1
            alimit=3
        a=0
        p=0
        for td in soup:
            ad=td.findAll('td')[4].get_text(strip=True)
            if ad == 'Alpa':
                a=a+1
            else:
                p=p+1
            kh.append(ad)
    
            if td.findAll('li', class_='next'):
                soup=tr.findAll('li', class_='next')
                url = soup2.a['href']
                r = s.get(url, headers = headers)
                soup = BeautifulSoup(r.content, 'lxml')
                soup = soup.findAll('tr', class_ =['even', 'odd'])
                for td in soup:
                    if ad == 'Alpa':
                        a=a+1
                    else:
                        p=p+1
                    kh.append(ad)
        alpstr=subject_dict[i]+'\nHadir = '+str(p)+'\nAlpa = '+str(a)+'\nJatah bolos = '+str(alimit-a)
        absen_list.append(alpstr)

    absen_list=json.dumps(absen_list)
    absen_list=absen_list.replace('"','')
    absen_list=absen_list.replace(', ','\n\n')
    absen_list=absen_list.replace('\\n','\n')
    absen_list=absen_list.replace('[','')
    absen_list=absen_list.replace(']','')