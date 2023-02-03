from __future__ import print_function
import requests
from bs4 import BeautifulSoup

import os.path

from bs4 import BeautifulSoup
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import date, timedelta



yesterday = date.today() - timedelta(1)



def main():  # sourcery skip: avoid-builtin-shadow, low-code-quality
    new_func()
    checking = input("Do you want to check yesterday CPR(Y/N): ")
    if checking.lower() == "y":

    # input request

        date = yesterday.strftime("%Y-%m-%d")
    else:
        date = input("Enter the date need checking(yyyy-mm-dd): ")
    base = input("Enter the Campus need to check: ")
    groups = []
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']




    s = requests.Session()



    para = f'?GroupWithLessonSearch%5BnextLessonTime%5D={date}+-+{date}&GroupWithLessonSearch%5BnextLessonNumber%5D=&GroupWithLessonSearch%5BnextLessonTitle%5D=&GroupWithLessonSearch%5Bid%5D=&GroupWithLessonSearch%5Btitle%5D={base}&GroupWithLessonSearch%5Bvenue%5D=&GroupWithLessonSearch%5Bactive_student_count%5D=&GroupWithLessonSearch%5Bweekday%5D=&GroupWithLessonSearch%5BlessonTeacherName%5D=&GroupWithLessonSearch%5Bteacher%5D=&GroupWithLessonSearch%5Bcurator%5D=&GroupWithLessonSearch%5Btype%5D=&GroupWithLessonSearch%5Bstatus%5D=&GroupWithLessonSearch%5BlessonFormat%5D=&GroupWithLessonSearch%5Bis_online%5D=&export=true&name=default&exportType=html'
    header =  {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "_ga=GA1.2.1620969847.1664966279; _ym_uid=1664966280852805697; _ym_d=1664966280; intercom-device-id-ufjpx6k3=fd3080c1-5a63-4af6-bd1f-15268d549a7e; userId=30454; sidebar-state=collapsed; studentId=1700942; studentAccessToken=207b1708c507aa9b0229d32dc599bab81689c647731db71a33a81c1bda38882b; studentCreatedTimestamp=1673939693; _grid_page_size_schedule=35d0980fa38e2255112d0c62698773cab8aa12a81c6735caf172064b5eb6ea47a%3A2%3A%7Bi%3A0%3Bs%3A24%3A%22_grid_page_size_schedule%22%3Bi%3A1%3Bs%3A3%3A%22200%22%3B%7D; previousPage=%2F; _csrf=ddfeab8da656c219c7f8f37676b4c73b72e76a375e3c19fa13af59d898432ccba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22wKXr9u4XPDywrZA9Ubl94QnhWfeHhZ-e%22%3B%7D; createdTimestamp=1675163976; accessToken=10074a7a9ea56087dea1d0ec1edd8d558d2988fae737cfcc81475a6e87542fa0; SERVERID=b410; _backendMainSessionId=51483341885540d447037f89ca4a764d; _gid=GA1.2.1650049365.1675163974",
        "Referer": "https://lms.logika.asia/group/default/schedule?GroupWithLessonSearch%5BnextLessonTime%5D={date}%20-%20{date}&GroupWithLessonSearch%5BnextLessonNumber%5D=&GroupWithLessonSearch%5BnextLessonTitle%5D=&GroupWithLessonSearch%5Bid%5D=&GroupWithLessonSearch%5Btitle%5D={base}&GroupWithLessonSearch%5Bvenue%5D=&GroupWithLessonSearch%5Bactive_student_count%5D=&GroupWithLessonSearch%5Bweekday%5D=&GroupWithLessonSearch%5BlessonTeacherName%5D=&GroupWithLessonSearch%5Bteacher%5D=&GroupWithLessonSearch%5Bcurator%5D=&GroupWithLessonSearch%5Btype%5D=&GroupWithLessonSearch%5Bstatus%5D=&GroupWithLessonSearch%5BlessonFormat%5D=&GroupWithLessonSearch%5Bis_online%5D=",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }



    end_point = f'https://lms.logika.asia/group/default/schedule{para}'
    res = s.get(end_point, headers = header)
    output = str(res.content)
    start = output.find('<table>')
    end = output.find('</table>')
    all_classes = output[start:end+len('</table>')]
    soup = BeautifulSoup(all_classes, 'html.parser')






    # get data 
    all_tr = soup.find_all('tr')
    creds = None

    for tr in all_tr:
        all_td = tr.find_all('td')
        time_of_next_les = all_td[0]
        next_les = all_td[1]
        group_title = all_td[4].find('a')
        all_li = all_td[4].find('p')
        class_occurrences = all_td[6].find('span')

        if group_title is None:
            continue


        all_li = all_li.string
        group_details = ({
            'group' : group_title.string,
            'nextLesson': int(next_les.string),
            'Time of Next Lesson': time_of_next_les.string.replace('\xa0', ' '),
            "CPR Link": all_li[all_li.find("https"):],
            "Pecentage": str(class_occurrences.string)
            })
        groups.append(group_details)
    # get CPR 

    if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)



        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    for group in groups:
        lessons = []
        id = group["CPR Link"]
        start = id.find("d/")
        end = id.find("/edit")
        id = id[start+2:end]
        try:
            service = build('sheets', 'v4', credentials=creds)


            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=id,
                                        range='Report!AC2:AC34').execute()
            values = result.get('values', [])
            lessons.extend(j[0] for j in values)
            if not lessons:
                result = sheet.values().get(spreadsheetId=id,
                                        range='Report!AE2:AE34').execute()
                values = result.get('values', [])

                lessons.extend(j[0] for j in values)
    # Print result
            if lessons[group["nextLesson"]] != '#DIV/0!' and group['Pecentage'] != "0%":

                print(f"{group['group']} is at lesson {group['nextLesson']} and the CPR is FILL and the average score of {lessons[group['nextLesson']]}\n")

            elif lessons[group["nextLesson"]] == '#DIV/0!' and group['Pecentage'] == "0%":
                print(f"{group['group']} no student attend the lessons!\n")

            else:
                print(f"{group['group']} is at lesson {group['nextLesson']} and the CPR is NOT FILL\n---> Here is the CPR: {group['CPR Link']} \n")

        except HttpError as err:
            print(f"This {group['group']} don't have CPR!\n")

def new_func():
    global yesterday
    
main()


