from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By 
import time
from bs4 import BeautifulSoup
import os
import glob
import requests
import os.path
import csv
import pandas as pd
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
try:
    os.mkdir("download")
except:
    pass
cwd = os.getcwd()
#PATH = "/app/.chromedriver/bin/chromedriver/chromedriver.exe"
chromeOptions= webdriver.ChromeOptions()
chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chromeOptions.add_argument('--headless')
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--no-sandbox")
prefs = {"download.default_directory" : cwd+"\\download"}
chromeOptions.add_experimental_option("prefs",prefs)

def start_driver():
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chromeOptions)
    return driver

def start_page(source):
    source.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")
#     time.sleep(3)
    source.page_source
    soup = BeautifulSoup(source.page_source)
    source.maximize_window()
    state_id = soup.findAll('div',{"class":"ui-selectonemenu ui-widget ui-state-default ui-corner-all"})[1]["id"]
    refresh_id = soup.findAll('button',{'class':'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-left button'})[0]['id']
    down_excel = soup.findAll('img',{'alt':''})[2]['id']
    return state_id,refresh_id,down_excel,source

def select_state(source,state_no,state_id,refresh_id):
#def select_state(source,state_no,state_id):
    #print(str(state_no))
    source.find_element_by_id(state_id+"_label").click()
    source.find_element_by_id(state_id+"_"+str(state_no)).click()
    time.sleep(2)
    refresh(source,refresh_id)
    time.sleep(5)
    source.page_source
    time.sleep(3)
    soup = BeautifulSoup(source.page_source)
    rtos = soup.findAll("select",{"id":"selectedRto_input"})
    #print(rtos,'inside func')
    rtolist = [i.text for i in rtos[0].findAll('option')[1:]]
    #print(rtolist,'list')
    if len(rtolist)==1:
        rtocounter = list(range(1,len(rtolist)+1))
        rto_dict = dict(zip(rtocounter,rtolist))
    else:
        rtocounter = list(range(1,len(rtolist)))
        rto_dict = dict(zip(rtocounter,rtolist))

    return source,rto_dict


def select_rto(source,rto_no):
    source.find_element_by_id("selectedRto_label").click()
    text = source.find_element_by_id("selectedRto_"+str(rto_no)).text.split('(')
    source.find_element_by_id("selectedRto_"+str(rto_no)).click()
    source.find_element_by_id(refresh_id).click()
    return source
    

def refresh(source,refresh_id):
    source.find_element_by_id(refresh_id).click()
    time.sleep(2)
    source.find_element_by_id(refresh_id).click()
    return source



def select_y_axis(source,y_no,refresh_id):
    source.find_element_by_id("yaxisVar_label").click()
    time.sleep(0.2)
    source.find_element_by_id("yaxisVar_"+y_no).click()
    return source

def select_x_axis(source,x_no,refresh_id):
    source.find_element_by_id("xaxisVar_label").click()
    time.sleep(0.2)
    source.find_element_by_id("xaxisVar_"+x_no).click()
    time.sleep(0.2)
    source.find_element_by_id(refresh_id).click()
    return source

def select_year_type(source):
    source.find_element_by_id("selectedYearType_label").click()
    time.sleep(0.2)
    source.find_element_by_id("selectedYearType_2").click()
#     time.sleep(0.2)
#     source.find_element_by_id(refresh_id).click()
    return source

def select_year(source,year_no):
    source.find_element_by_id("selectedYear_label").click()
    time.sleep(1)
    source.find_element_by_id("selectedYear_"+year_no).click()
#     time.sleep(0.2)
    source.find_element_by_id(refresh_id).click()
    return source


def select_month(source,month_no):
    source.find_element_by_id("groupingTable:selectMonth_label").click()
    time.sleep(1)
    source.find_element_by_id("groupingTable:selectMonth_"+month_no).click()
    return source

def select_vcgroup(source,gruop_no):
    source.find_element_by_id("vchgroupTable:selectCatgGrp_label").click()
    time.sleep(0.2)
    source.find_element_by_id("vchgroupTable:selectCatgGrp_"+gruop_no).click()
    return source

def download(source):
    time.sleep(0.5)
    source.find_element_by_id("groupingTable:xls").click()
    return source


def file_rename(rto,y_axis,x_axis,year,month):
    file_type = '/*xlsx'
    files = glob.glob('./download' + file_type)
    max_file = max(files, key=os.path.getmtime)
    try:
        time.sleep(0.5)
        #rename_file
        os.rename(max_file,cwd+'/download/'+rto+'_'+y_axis+'_'+x_axis+'_'+year+'_'+month+'.xlsx')
    except:
        print('rename error1')
        os.remove(max_file)

def send_files_to_drive(name,path):
    headers = {"Authorization": "Bearer ya29.a0ARrdaM_B11gXPI5ctK4TMcehQXq7l7QPrPzgJXfouVy_dDJv3wnRVWGfz4BhKeetjWpUfJXMdv5MCXjxm0IjDHzdJo00CjWhPgrEmZZ8cWFixakBto0H_-Lrd1OLltDwW0K5gB4YPAE2fdYqrWYS-iiSfAm4"}
    para = {
        "name": name,
        "parents":["14JH-iI0UJWMfwuwLFKlu1IYiQWko_baN"]
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open(path, "rb")
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files)
    return r.status_code

def logfileupdatewrite(s,rto,y_axis,x_axis,year,month):
    f = open('download/logfile.txt',"w")
    f.write(str(s)+","+str(rto)+","+str(y_axis)+","+str(x_axis)+","+str(year)+","+str(month))
    f.close()
    
def logfilebasewrite(s,rto,y_axis,x_axis,year,month):
    f = open('download/baselogfile.txt',"w")
    f.write(str(s)+","+str(rto)+","+str(y_axis)+","+str(x_axis)+","+str(year)+","+str(month))
    f.close()


def logfileread():
    f = open('download/logfile.txt',"r")
    d = f.read().split(",")
    f.close()
    return d

def basefilefileread():
    f = open('download/baselogfile.txt',"r")
    d = f.read().split(",")
    f.close()
    return d

maker = {"0":"Vehicle Category","1":"Norms","2":"Fuel"}

Fuel = {"0":"Vehicle Category","1":"Norms"}

Norms = {"0":"Vehicle Category","1":"Fuel"}

vehicleClass = {"0":"Vehicle Category","1":"Norms","2":"Fuel"}

vehicleCategory = {"0":"Norms","1":"Fuel"}

yAxis = {"0":"vehicleCategory","1":"VehicleClass","2":"Norms","3":"Fuel","4":"Maker"}

years = {"2":"2021","3":"2020","4":"2019","5":"2018","6":"2017","7":"2016","8":"2015","9":"2014","10":"2013","11":"2012"}

month = {"1":"JAN","2":"FEB","3":"MAR","4":"APR","5":"MAY","6":"JUN","7":"JUL","8":"AUG","9":"SEP","10":"OCT","11":"NOV","12":"DEC"}

xyaxis = {"vehicleCategory":vehicleCategory,"VehicleClass":vehicleClass,"Norms":Norms,"Fuel":Fuel,"Maker":maker}

f = open('State_RTO_LIST.json',"r")
data1 = f.read()
data1 = json.loads(data1)
f.close()

f1 = open('State_LIST.json',"r")
state_dict = f1.read()
state_dict = json.loads(state_dict)
f1.close()

drive = start_driver()
logfilebasewrite('1', '1', '0', '0', '2', '1')

state_id,refresh_id,down_excel,source = start_page(drive)

while True:
    try:
        try:
            logdatas = logfileread()
            s_start,r_start,yx_start,xx_start,y_start,m_start  = logdatas
            #print(m_start,'m_start')
        except:
            print('except')
            logdatas = basefilefileread()
            s_start,r_start,yx_start,xx_start,y_start,m_start  = logdatas
            #print(m_start,'except')


        for s in range(int(s_start),len(list(state_dict.keys()))+1):
            source,rto_dict = select_state(source,str(s),state_id,refresh_id)
            #source,rto_dict = select_state(source,s,state_id)
    #             print(state_dict[s])
            time.sleep(1)
            #print(rto_dict,r_start,"rto")
            for r in range(int(r_start),len(list(rto_dict.keys()))+1):
                time.sleep(1)
                source = select_rto(source,r)
                name_rto = rto_dict[r]
                time.sleep(1)
                yaxisxsx = ["0","1","2","3","4"]

                for yx in range(int(yx_start),len(yaxisxsx)):
                    #print('yx',yx)
                    source = select_y_axis(source,str(yx),refresh_id)
                    name_yaxis = yAxis[str(yx)]
                    #print(name_yaxis)
                    time.sleep(3)
                    xaxisxsx = list(xyaxis[name_yaxis].keys())
    #                     print(xyaxis)
    #                     print(name_yaxis)
                    #print(xx_start,len(xaxisxsx))

                    for xx in range(int(xx_start),len(xaxisxsx)):
                        #print('xx_in',xx)
                        source = select_x_axis(source,str(xx),refresh_id)
                        print(xyaxis[name_yaxis])
                        name_xaxis = xyaxis[name_yaxis][str(xx)]
                        #print(name_xaxis,'x')
                        time.sleep(1)
                        source = select_year_type(source)
                        time.sleep(1)
                        yearsxsx = list(years.keys())
                        time.sleep(1)

                        for y in range(int(y_start),len(yearsxsx)+2):
                            #print('y_in',y)
                            time.sleep(1)
                            source = select_year(source,str(y))
                            source = refresh(source,refresh_id)
                            name_year = years[str(y)]
    #                             print(list(range(int(y_start),len(yearsxsx)+2)))
                            if name_year =="2021":
                                monthsxsx = list(month.keys())[:7]
                            else:
                                monthsxsx = list(month.keys())
                            time.sleep(2)

                            for m in range(int(m_start),len(monthsxsx)+1):
                                #print('m_in',m)
                                time.sleep(2)
                                source = select_month(source,str(m))
                                name_month = month[str(m)]
                                #print(name_month)
                                time.sleep(1)
                                download(source)
                                time.sleep(1)

                                logfileupdatewrite(str(s),r,str(yx),str(xx),str(y),str(m))
                                time.sleep(1.5)
                                file_rename(name_rto,name_yaxis,name_xaxis,name_year,name_month)
                                di = cwd+'/download/'+name_rto+'_'+name_yaxis+'_'+name_xaxis+'_'+name_year+'_'+name_month+'.xlsx'
                                nam = name_rto+'_'+name_yaxis+'_'+name_xaxis+'_'+name_year+'_'+name_month+'.xlsx'
                                time.sleep(1)
                                send_files_to_drive(nam,di)
                                
                            m_start='1'
                        y_start='2'
                    xx_start='0'
                yx_start='0'
            r='1'


    except Exception as e:
        print(e)


 