import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import psycopg2
import requests
token = "0"
profileid = "0"
vcode = ''

#UPDATE username and password and STATUS below to run script
@logTestName
def test_post_login_ACT():
    logger.info("POST /login - Positive Test")

    mutation = """ mutation ($username: String!, $password: String!) 
    {
    login(input: {username:$username, password:$password})
        {
        token
        profileId
        }
    }
    """
    variables = {
    "username": "nrccua.signup@gmail.com",
    "password": "Password1!"}

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print (json_response["data"]["login"]["token"])
    print (json_response["data"]["login"]["profileId"])
    global token
    global profileid
    token = (json_response["data"]["login"]["token"])
    profileid = (json_response["data"]["login"]["profileId"])
    assert response.status_code == 200
    assert (token != '')


##########Query the milestone table and send variable to Journeys mutation####################
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

            head = {
                "Authorization": "bearer " + token
            }
            #COMPLETED, NOT_APPLICABLE, IN_PROGRESS, NOT_STARTED
            mutation = """ mutation ($profileId: ID!, $milestone: ID!)
                {
                  updateLearnerMilestoneStatus(input: {
                    status: NOT_APPLICABLE,
                    milestoneUid: $milestone,
                    profileId: $profileId
                  })
                }"""

            variables = {
                "updateLearnerMilestoneStatus": "null",
                "milestone": milestoneUID,
                "profileId": profileid
            }

            response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables}, headers=head)
            print(response.text)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
    #closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")