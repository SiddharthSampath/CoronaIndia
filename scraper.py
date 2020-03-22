from selenium import webdriver
from shutil import which
from selenium.webdriver.chrome.options import Options
import sqlite3
import os
import time
import smtplib
from email.message import EmailMessage
from prettytable import PrettyTable
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

def data_retrieval(retrieved_data, scraped_data, final_row):


    state = scraped_data[0]
    indian_cases = scraped_data[1]
    foreign_cases = scraped_data[2]
    cured = scraped_data[3]
    death = scraped_data[4]
    if retrieved_data == None:
        
        new_data.append(["NEW_STATE",state,indian_cases,foreign_cases,cured,death])
        c.execute('''
                INSERT INTO CoronaV VALUES(?,?,?,?,?)
                ''',scraped_data)
        conn.commit()
    else:
        if retrieved_data[1].strip() != indian_cases or retrieved_data[2].strip() != foreign_cases or retrieved_data[3].strip() != cured or retrieved_data[4].strip() != death:
            if not final_row:
                new_data.append(["EXISTING",state,indian_cases,foreign_cases,cured,death,retrieved_data])
            else:
                new_data.append(["TOTAL",state,indian_cases,foreign_cases,cured,death,retrieved_data])
            values = [indian_cases,foreign_cases,cured,death,state]
            c.execute('''
                    UPDATE CoronaV set INDIANS = ?, FOREIGNERS = ?, CURED = ?,DEATHS = ? WHERE STATE = ?
                    ''',values)
            conn.commit()
    return

def send_email_notification():

    with open("test1.txt","w") as fp:
       fp.write(tab.get_string())
    

    email_content = "Hello,\n\n"
    if new_data:
        for item in new_data:
            if item[0] == "NEW_STATE":
                email_content += f"New State - {item[1]} affected\n"
                print(f"New State - {item[1]} affected")
            elif item[0] == "EXISTING":
                email_content += f"Change in stats in {item[1]}\n"
                email_content += f"Old Stats in {item[1]} \n Indians affected : {item[6][1]}\t foreigners affected : {item[6][2]}\t cured or migrated : {item[6][3]}\t deaths : {item[6][4]}\n"
                email_content += f"New Stats in {item[1]}\n"
                print(f"Change in stats in {item[1]}")
                print(f"Old Stats in {item[1]} \n Indians affected : {item[6][1]}\t foreigners affected : {item[6][2]}\t cured or migrated : {item[6][3]}\t deaths : {item[6][4]}")
                print(f"New Stats in {item[1]}")
            elif item[0] == "TOTAL":
                email_content += f"Old Stats in Total Cases \n Indians affected : {item[6][1]}\t foreigners affected : {item[6][2]}\t cured or migrated : {item[6][3]}\t deaths : {item[6][4]}\n"
                email_content += "The new total of the number of cases"
                print(f"Old Stats in Total Cases \n Indians affected : {item[6][1]}\t foreigners affected : {item[6][2]}\t cured or migrated : {item[6][3]}\t deaths : {item[6][4]}")
                print("The new total of the number of cases")

            email_content += f"Indians affected : {item[2]}\t foreigners affected : {item[3]}\t cured or migrated : {item[4]}\t deaths : {item[5]}\n"
            print(f"Indians affected : {item[2]}\t foreigners affected : {item[3]}\t cured or migrated : {item[4]}\t deaths : {item[5]}")
    else:
        email_content += "No change in the numbers"
        print("No change in the numbers")
    email_content += "\n\nYours Truly,\nThe Mysterious WebScraper"
    fromaddr = "themysteriouswebscraper@gmail.com"
    toaddr = "siddharthsampath98@gmail.com"
    
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    
    # storing the senders email address   
    msg['From'] = fromaddr 
    
    # storing the receivers email address  
    msg['To'] = toaddr 
    
    # storing the subject  
    msg['Subject'] = "Coronavirus updates in India"
    
    # attach the body with the msg instance 
    msg.attach(MIMEText(email_content, 'plain')) 
    
    # open the file to be sent  
    filename = "data.txt"
    attachment = open("test1.txt", "rb") 
    
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
    
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
    
    # encode into base64 
    encoders.encode_base64(p) 
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
    
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login(fromaddr, "Webscraping983!") 
    
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    s.sendmail(fromaddr, 'radhasampath8@gmail.com', text)
    # terminating the session 
    s.quit()
    
    return


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
tab = PrettyTable()
tab.field_names = ["State", "Indian_Affected","Foreigners Affected","Cured or Migrated","Deaths"]
button = driver.find_element_by_xpath("//button[@class='collapsible']")
button.click()
rows = driver.find_elements_by_xpath("(//div[@class='table-responsive'])[2]/table/tbody/tr")
count =  0
new_data = []
for row in rows:
    count += 1
    if count == len(rows):
        state = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[1]").text
        indian_cases = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[2]").text
        foreign_cases = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[3]").text
        cured = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[4]").text
        death = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[5]").text
        c.execute('SELECT * FROM CoronaV WHERE STATE=?',(state,))
        retrieved_data = c.fetchone()
        scraped_data = [state,indian_cases,foreign_cases,cured,death]
        data_retrieval(retrieved_data, scraped_data, True)
        # if retrieved_data == None:
        #     c.execute('''
        #     INSERT INTO CoronaV VALUES(?,?,?,?,?)
        #     ''',scraped_data)
        #     conn.commit()
        # else:
        #     if retrieved_data[1].strip() != indian_cases or retrieved_data[2].strip() != foreign_cases or retrieved_data[3].strip() != cured or retrieved_data[4].strip() != death:
        #         new_data.append(["EXISTING",state,indian_cases,foreign_cases,cured,death])
        #         values = [indian_cases,foreign_cases,cured,death,state]
        #         c.execute('''
        #             UPDATE CoronaV set INDIANS = ?, FOREIGNERS = ?, CURED = ?,DEATHS = ? WHERE STATE = ?
        #             ''',values)
        #         conn.commit()
        tab.add_row(scraped_data)
        print(f"{state} : Indian Nationals = {indian_cases}\t Foreign Nationals = {foreign_cases}\t Cured or Migrated = {cured}\t Death = {death} ")
        break
    else:
        state = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[2]").text
        indian_cases = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[3]").text
        foreign_cases = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[4]").text
        cured = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[5]").text
        death = driver.find_element_by_xpath(f"(//div[@class='table-responsive'])[2]/table/tbody/tr[{count}]/td[6]").text
        scraped_data = [state,indian_cases,foreign_cases,cured,death]
        c.execute('SELECT * FROM CoronaV WHERE STATE=?',(state,))
        retrieved_data = c.fetchone()
        data_retrieval(retrieved_data, scraped_data, False)
        # if retrieved_data == None:
        #     new_data.append(["NEW_STATE",state,indian_cases,foreign_cases,cured,death])
        #     c.execute('''
        #         INSERT INTO CoronaV VALUES(?,?,?,?,?)
        #         ''',[state,indian_cases,foreign_cases,cured,death])
        #     conn.commit()
        # else:
        #     if retrieved_data[1].strip() != indian_cases or retrieved_data[2].strip() != foreign_cases or retrieved_data[3].strip() != cured or retrieved_data[4].strip() != death:
        #         new_data.append(["EXISTING",state,indian_cases,foreign_cases,cured,death])
        #         values = [indian_cases,foreign_cases,cured,death,state]
        #         c.execute('''
        #         UPDATE CoronaV set INDIANS = ?, FOREIGNERS = ?, CURED = ?,DEATHS = ? WHERE STATE = ?
        #         ''',values)
        #         conn.commit()
        tab.add_row(scraped_data)
        print(f" State : {state}\t Indians affected : {indian_cases}\t foreigners affected : {foreign_cases}\t cured or migrated : {cured}\t deaths : {death}")
conn.close()
driver.close()

send_email_notification()

    
       