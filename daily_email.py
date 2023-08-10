import os
import gspread
from random import randint
from httplib2 import Http
import smtplib
from dotenv import load_dotenv

load_dotenv()

def lambda_handler(event, context):
    gc = gspread.service_account(filename='daily-email-bot-783f84e4558c.json')
    wks = gc.open_by_key('12y3I1U7ArX-qOUcRLMNn0Ww4j5ShwhXVUJyvyKVf9Gg')
    sheet = wks.get_worksheet(0)

    x = len(sheet.col_values(1))
    randomRow = randint(0,x)

    title = sheet.cell(randomRow, 2).value
    quote = sheet.cell(randomRow, 3).value
    #print(quote)

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()

    gmail_username = os.getenv('GMAIL_USERNAME')
    gmail_password = os.getenv('GMAIL_PASSWORD')

    smtpObj.login(gmail_username, gmail_password)

    sent_from = 'laurenbaldino1@gmail.com'
    to = ['laurenbaldino1@gmail.com']
    body = 'Subject: Daily Quote\n\n %s\n %s\n' % (title, quote)

    sendmailStatus = smtpObj.sendmail(sent_from, to, body.encode('utf-8'))
    if sendmailStatus != {}:
        print('Error')
    smtpObj.quit()

