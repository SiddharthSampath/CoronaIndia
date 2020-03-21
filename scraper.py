from selenium import webdriver
from shutil import which
from selenium.webdriver.chrome.options import Options
import sqlite3
import os
import time

chrome_path = which("chromedriver")
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
driver.get("https://www.mohfw.gov.in/")
dbExist = 0
if os.path.isfile("./corona.db"):
    dbExist = 1
conn = sqlite3.connect("corona.db")
c = conn.cursor()
if not dbExist:
    c.execute('''
    CREATE TABLE CoronaV(STATE TEXT,
    INDIANS TEXT,
    FOREIGNERS TEXT,
    CURED TEXT,
    DEATHS TEXT)
    ''')

time.sleep(2)
rows = driver.find_elements_by_xpath("//tbody/tr")
count =  0
print(len(rows))
new_data = []
for row in rows:
    count += 1
    if count == len(rows):
        state = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[1]").text
        indian_cases = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[2]").text
        foreign_cases = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[3]").text
        cured = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[4]").text
        death = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[5]").text
        c.execute('SELECT * FROM CoronaV WHERE STATE=?',(state,))
        retrieved_data = c.fetchone()
        if retrieved_data == None:
            c.execute('''
            INSERT INTO CoronaV VALUES(?,?,?,?,?)
            ''',[state,indian_cases,foreign_cases,cured,death])
            conn.commit()
        else:
            if retrieved_data[1].strip() != indian_cases or retrieved_data[2].strip() != foreign_cases or retrieved_data[3].strip() != cured or retrieved_data[4].strip() != death:
                new_data.append(["EXISTING",state,indian_cases,foreign_cases,cured,death])
                values = [indian_cases,foreign_cases,cured,death,state]
                c.execute('''
                    UPDATE CoronaV set INDIANS = ?, FOREIGNERS = ?, CURED = ?,DEATHS = ? WHERE STATE = ?
                    ''',values)
                conn.commit()
           
        
        with open("test.txt","a") as fp:
            fp.write(f"{state} : Indian Nationals = {indian_cases}\t Foreign Nationals = {foreign_cases}\t Cured or Migrated = {cured}\t Death = {death} \n")
        print(f"{state} : Indian Nationals = {indian_cases}\t Foreign Nationals = {foreign_cases}\t Cured or Migrated = {cured}\t Death = {death} ")
        break
    else:
        state = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[2]").text
        indian_cases = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[3]").text
        foreign_cases = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[4]").text
        cured = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[5]").text
        death = driver.find_element_by_xpath(f"//tbody/tr[{count}]/td[6]").text
        c.execute('SELECT * FROM CoronaV WHERE STATE=?',(state,))
        retrieved_data = c.fetchone()
        if retrieved_data == None:
            new_data.append(["NEW_STATE",state,indian_cases,foreign_cases,cured,death])
            c.execute('''
                INSERT INTO CoronaV VALUES(?,?,?,?,?)
                ''',[state,indian_cases,foreign_cases,cured,death])
            conn.commit()
        else:
            if retrieved_data[1].strip() != indian_cases or retrieved_data[2].strip() != foreign_cases or retrieved_data[3].strip() != cured or retrieved_data[4].strip() != death:
                new_data.append(["EXISTING",state,indian_cases,foreign_cases,cured,death])
                values = [indian_cases,foreign_cases,cured,death,state]
                c.execute('''
                UPDATE CoronaV set INDIANS = ?, FOREIGNERS = ?, CURED = ?,DEATHS = ? WHERE STATE = ?
                ''',values)
                conn.commit()
       
        with open("test.txt","a") as fp:
            fp.write(f" State : {state}\t Indians affected : {indian_cases}\t foreigners affected : {foreign_cases}\t cured or migrated : {cured}\t deaths : {death}\n")
        
        print(f" State : {state}\t Indians affected : {indian_cases}\t foreigners affected : {foreign_cases}\t cured or migrated : {cured}\t deaths : {death}")
conn.close()
driver.close()