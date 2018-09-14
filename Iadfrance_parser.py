from time import sleep
from random import randint
import os

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from user_agent import generate_user_agent


def random_sleep(start=1, end=3):
    sleep(randint(start, end))

dir = os.path.abspath(os.path.dirname(__file__))
url = "https://www.iadfrance.fr/agent/{}/modal"
out_file_name = 'iadfrance_agent.xlsx'
out_file_dir = os.path.join(dir, 'data', out_file_name)

# create out file sheet and headers
wb = Workbook()
ws = wb.create_sheet("iadfrance_agent_all")
ws.append(["First Name",
          "Last Name",
          "Email",
          "Phone",
          "Sector"])

print("Start...")
n = 0
for id in range(11000, 30000):
    try:
        random_sleep()
        headers = {'User-Agent': generate_user_agent()}
        response = requests.get(url.format(id), headers)
        if response.status_code != 404:
            print("Iteration --> {}".format(n))
            n += 1
            bs_obj = BeautifulSoup(response.text, features="html.parser")

            # get first and last name
            first_last_name = bs_obj.find("div", class_="modal-header-right").find("h4").text
            first_name = str(first_last_name).split(" ")[0]
            last_name = str(first_last_name).split(" ")[1]

            # get email and phone
            email_phone_obj = bs_obj.find("div", class_="clearfix")
            email = email_phone_obj.find_all("p")[0].text[8:]
            phone = email_phone_obj.find_all("p")[1].text[11:]

            # get sector
            sector = bs_obj.find("p", class_="sector").text
            ws.append([first_name,
                       last_name,
                       email,
                       phone,
                       sector
            ])
            wb.save(out_file_dir)

        else:
            continue
    except:
        continue
print("Save data to file {}".format(out_file_dir))





