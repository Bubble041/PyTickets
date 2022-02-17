from cgitb import text
from tkinter.tix import Select
from unicodedata import name
from pip import main
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from auth_data import username, password
import time
import json


browser = webdriver.Chrome(executable_path=r'chromedriver.exe')

tickets_info = []
works_info = []
coincidences = []
result = []

def login(username, password):

    browser.get('https://staff.timeweb.net/')
    time.sleep(2)

   
    login_input = browser.find_element_by_name('LoginForm[username]')
    login_input.clear()
    login_input.send_keys(username)
    time.sleep(2)

    password_input = browser.find_element_by_name('LoginForm[password]')
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(2)

    password_input.send_keys(Keys.ENTER)
    time.sleep(7)

def get_tickets_info():
    try:
        browser.get('https://staff.timeweb.net/oldstaff/load?module=mod_support')
        time.sleep(6)

        browser.switch_to.frame('oldstaff-index-frame')
        select = Select(browser.find_element_by_xpath('/html/body/table[1]/tbody/tr/td[3]/select'))
        select.select_by_value('all')
        time.sleep(2)
        try:
            table = browser.find_element_by_xpath('/html/body/table[3]/tbody')
            table = table.find_elements_by_tag_name('tr')
            tickets_id = []

            id_count = 0
            for item in table:
            
                if item.get_attribute('id'):
                    tickets_id.append(item.get_attribute('id'))
                    server_name = browser.find_element_by_xpath(f'//*[@id="{tickets_id[id_count]}"]/td[6]')
                    status = browser.find_element_by_xpath(f'//*[@id="{tickets_id[id_count]}"]/td[5]')
                    if status.text == "новый":
                        tickets_info.append(
                            {
                                "link": tickets_id[id_count].replace('tr_', 'https://staff.timeweb.net/tickets/'),
                                "server_name": server_name.text,
                                "status": status.text
                            }
                        )
                    id_count += 1
        except Exception as ex:
            print(ex)
            browser.quit()
            browser.close()
    except Exception as ex:
        print(ex)
        browser.quit()
        browser.close()
    print(tickets_info)

def get_works_info():
    browser.get('https://staff.timeweb.net/tech-works#list?type=null&status=null&serverName=null&degradationLevel=null&dateStart=null&dateEnd=null&limit=6&offset=0')
    time.sleep(4)

    for item in range(1, 5):
        work_type = browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[2]')
        if work_type.text[0:3] != 'ППР' or work_type.text[0:4] == 'DDoS':
            #if browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[3]/span').text == "Открыта":
            try:
                works_info.append(
                {
                    "type": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[2]').text[0:4].strip(),
                    "number": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[2]').text.strip(),
                    "status": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[3]/span').text,
                    "start_time": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[4]/span').text,
                    "influence": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[8]/span').text,
                    "servers": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[9]/ul/li/span').get_attribute('data-title')
                }
            )
            except:
                works_info.append(
                {
                    "type": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[2]').text[0:4].strip(),
                    "number": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[2]').text.strip(),
                    "status": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[3]/span').text,
                    "start_time": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[4]/span').text,
                    "influence": browser.find_element_by_xpath(f'//*[@id="techWorksLayout"]/div/div/div[4]/div/div[2]/ol/li[{item}]/div[8]/span').text,
                    "servers": 'none'
                }
            )
            
    print(works_info)
    

def looking_match():
    for server in works_info:
        for ticket in tickets_info:
            if ticket['server_name'] in server['servers']:
                result.append(
                    {
                        "link": ticket["link"],
                        "work_number": server["number"].split("#")[-1].strip(),
                        "start_time": server["start_time"],
                        "influence": server["influence"]
                    }
                )
    with open("result.json", "w") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

def main():
    login(username, password)
    get_tickets_info()
    time.sleep(2)
    get_works_info()
    time.sleep(2)
    looking_match()

if __name__ == '__main__':
    main()