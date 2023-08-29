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

        cursor.execute("""SELECT milestone_uid FROM journeys.journey_milestone""")
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
                    status: COMPLETED,
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