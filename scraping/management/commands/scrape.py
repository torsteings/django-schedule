from django.core.management.base import BaseCommand

from jobs.settings import EMAIL_HOST_PASSWORD
from jobs.settings import EMAIL_HOST_USER

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import numpy as np
import pandas as pd

import requests

class Command(BaseCommand):
    # define logic of command
    def handle(self, *args, **options):
        yahooAdress = "https://query1.finance.yahoo.com/v8/finance/chart/"
        tickerSymbol = "EQNR" #ticker
        symbol = ".OL?symbol="
        rest = ".OL&period1=1533914279&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit"
        url = yahooAdress + tickerSymbol + symbol + tickerSymbol + rest
        #url = "https://query1.finance.yahoo.com/v8/finance/chart/EQNR.OL?symbol=EQNR.OL&period1=1533914279&period2=9999999999&interval=1d&includePrePost=true&events=div%2Csplit"
        r = requests.get(url)

        #Checks if there is contact with the server: Status code: 200 = OK!
        if r.status_code == 200:
            #print("Status code: 200.....Standard response for successful HTTP requests")
            data = r.json()
            result = r.json()['chart']['result']

            # Iterate through the list ['meta']. List does not contain {timestamp} dictionary.
            # Append all items to metaList.
            # {timestamp} is on the same level as ['meta'] and can be accessed through the for loop.
            metaList = []
            for item in result:
                metaList.append(item['indicators']['quote'])
            open = metaList[0][0]['open']
            close = metaList[0][0]['close']
            high = metaList[0][0]['high']
            low = metaList[0][0]['low']
            volume = metaList[0][0]['volume']

            #open.reverse()
            #close.reverse()
            #high.reverse()
            #low.reverse()
            #volume.reverse()

            dataMatrix = []
            dataMatrix.append(open)
            dataMatrix.append(close)
            dataMatrix.append(high)
            dataMatrix.append(low)
            dataMatrix.append(volume)
            #print(dataMatrix)

            data = np.array(dataMatrix).T.tolist()
            df = pd.DataFrame(data, index=range(0, len(open)), columns=['open_price', 'close_price', 'high_price', 'low_price', 'volume'])
            close_price = df['close_price'].tail(1)
            # return df['volume']
            # return df

        # Set email header information.
        sender = "CTbirds AS"
        username = EMAIL_HOST_USER
        password = EMAIL_HOST_PASSWORD
        host = "smtp.gmail.com"
        port = 587 #transport level security

        recipient = "torstein.skarsgard@gmail.com"

        body = "var3" + str(close_price)

        # Assemble the message.
        msg = MIMEMultipart()
        msg.add_header("From", sender)
        msg.add_header("To", recipient)
        msg.add_header("Subject", "Dagens aksje")
        msg.attach(MIMEText(body, "plain"))

        # Send the message.
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()

        self.stdout.write( 'job complete' )
        # Include a return statement at the end of each
        # logical flow of the handle() function so
        # Heroku Scheduler knows when it can shut down.

        return
