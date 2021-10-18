import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import psycopg2
import tkinter as tk
from tkinter import simpledialog
import datetime
import requests
import imaplib
import smtplib
import email
import time
import json
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuemailname = "nrccua.signup+" + TS + "@gmail.com"
vc = "123456"
token = "0"
profileid = "0"
vcode = ''



##########Activates the user based on the Verification Code found in the DB query####################
@logTestName
def test_encourage_post_queryMilestoneTable():
    logger.info("POST /queryMilestoneTable - Positive Test")
    global milestoneUID
    global verificationcode
    global emailaddress
    #time.sleep(10)
    try:
        connection = psycopg2.connect(user = apollo_helpers.pguser,
                                  password = apollo_helpers.pgpassword,
                                  host = apollo_helpers.pghost,
                                  port = apollo_helpers.pgport,
                                  database = apollo_helpers.pgdatabase)

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        cursor.execute("""SELECT uid FROM journeys.milestone""")
        query_results = cursor.fetchall()
        print(query_results)
        for x in query_results:
            print(x[0])
            milestoneUID = (x[0])

            mutation = """ mutation ($profileId: ID!, $milestone: ID!)
                {
                  updateLearnerMilestoneStatus(input: {
                    status: COMPLETED,
                    milestoneUid: $milestone,
                    profileId: $profileId
                  })
                }"""

            variables = {
                "updateLearnerMilestoneStatus": "null",
                "milestone": milestoneUID,
                "profileId": "616db9172000007f4df57a7e"
            }

            response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
            print(response.text)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
    #closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")