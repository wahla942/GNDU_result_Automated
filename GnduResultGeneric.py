
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time



class ScrapeResult:
    def __init__(self,  year , month , c_type , course , sem , r_n ,  ):
        self.year = year
        self.month = month
        self.c_type  = c_type
        self.sem = sem
        self.course = course
        self.r_n = r_n
        self.names = []
        self.cgps = []
        self.r_n_to_str()
    def r_n_to_str(self):
        for i in range(len(self.r_n)):
            self.r_n[i] = str(self.r_n[i])
    def extract_result(self):
        driver.get(url)
        time.sleep(2)
        driver.find_element_by_name('DrpDwnYear').send_keys(self.year)
        time.sleep(1)
        driver.find_element_by_name('DrpDwnMonth').send_keys(self.month)
        time.sleep(1)
        driver.find_element_by_name('DropDownCourseType').send_keys(self.c_type)
        time.sleep(1)
        driver.find_element_by_name('DrpDwnCMaster').send_keys(self.course)
        time.sleep(1)
        driver.find_element_by_name('DrpDwnCdetail').send_keys(self.sem)
        
        for rn in self.r_n:
            gps = []
            name = []
            time.sleep(2)
            driver.find_element_by_name('textboxRno').clear()
            driver.find_element_by_name('textboxRno').send_keys(rn)
            driver.find_element_by_name('buttonShowResult').click()

            soup = BeautifulSoup(driver.page_source , 'html5lib')
            all_tr = soup.find_all('tr')
            for tr in all_tr:
                all_td = tr.find_all('td')
                for td in all_td:
                    try :
                        gps.append(td.centre.text)
                    except:
                        continue
            for tr in all_tr:
                all_td = tr.find_all('td')
                for td in all_td:
                    try:
                        name.append(td.text)
                    except:
                        continue

            try:
                self.names.append(name[5].split()[2])
                if name[5].split()[2] == ':':
                    self.names.append(name[4].split()[2])
            except : 
                self.names.append('Data_retreive_error')

            try:
                self.cgps.append(float(gps[4]))

            except:  
                self.cgps.append(-1.0)

            driver.back()
    def display_result(self):
        for x,y,z in zip(self.r_n , self.names , self.cgps):
            print(x,y,z)
    def write_to_csv(self):
        result = { 'Roll_Num' : self.r_n  , 'Name' : self.names , 'CGPA' : np.array(self.cgps) }
        df = pd.DataFrame( result )
        df.set_index('Roll_Num').to_csv('2019_may.csv')


year = '2019'
month = 'May.'
c_type = 'CBES (New)'
course = 'B.Tech. (Computer Science & Engg.)'
sem = 'B.Tech. (Computer Science & Engg.)-2nd Semester'


r_n = []
for i in range(1 , 221):
    r_n.append(17031874200 + i)


sr = ScrapeResult(year , month , c_type , course , sem , r_n)


driver = webdriver.Chrome(r'C:\Users\wahla saab\Pictures\drivers\chromedriver')
url = 'http://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'
sr.extract_result()
sr.write_to_csv()

driver.close()

