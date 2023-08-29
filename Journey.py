import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import psycopg2
import requests
token = "0"
profileid = "0"
vcode = ''
lines = ''

#UPDATE username and password and STATUS below to run script
@logTestName
def test_post_login_ACT():
    logger.info("POST /login - Positive Test")
    head = {
        'apollographql-client-name': 'ENCOURAGE'
    }

    mutation = """ mutation ($username: String!, $password: String!) 
        {
        userLogin(
            input: {
            username: $username,
            password: $password
            }
        ) 
    {
    __typename
    ...on
    UserLoginSuccess
        {
        profileId
        accessToken
        refreshToken
        }
    ...on
    InvalidPrivacyProgramTermsAndConditionVersionError
        {
        message,
        privacyProgramErrors
        }
    ...on
    PrivacyProgramTermsAndConditionsNotFoundError
        {
        message,
        privacyProgramErrors
        }
    ...on
    ProfileMissingOrInvalidAcceptedTermsAndConditionsError
        {
        message,
        privacyProgramErrors
        }
    ...on
    UserLoginError
        {
        message
        }
    ...on
    InvalidUserCredentialsError
        {
        message
        }
    ...on
    Error
        {
        message
        }
    }
}
    """


    variables = {
    "username": "nrccua.signup+202307194@gmail.com",
    "password": "Password1!"}

    response = requests.post(apollo_helpers.graphQL, headers=head, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print (json_response["data"]["userLogin"]["accessToken"])
    print (json_response["data"]["userLogin"]["profileId"])
    global token
    global profileid
    token = (json_response["data"]["userLogin"]["accessToken"])
    profileid = (json_response["data"]["userLogin"]["profileId"])
    assert response.status_code == 200
    assert (token != '')


##########Read from the Text file ####################
###Text file created from SELECT milestone_uid FROM journeys.journey_milestone###############
@logTestName
def test_updateLearnerMilestoneStatus():
    logger.info("POST /updateLearnerMilestoneStatus - Positive Test")
    global lines
    global count
    global line
    global milestoneUID
    global verificationcode
    global emailaddress

    # Using readlines()
    file = open('milestone_uid', 'r')
    #print(file)
    lines = file.readlines()
    print (lines)
    line = len(file.readlines())
    print(line)


    x = 0
    # Strips the newline character
    for x in lines:
        print (x)
        #x= x.strip()
        #print(line.strip(x))
        milestoneUID = x.strip()
        from more_itertools import strip
        #x.strip()


        head = {
            "Authorization": "bearer " + token
        }
        #COMPLETED, NOT_APPLICABLE, IN_PROGRESS, NOT_STARTED
        mutation = """ mutation updateLearnerMilestoneStatus ($input: UpdateLearnerMilestoneStatusInput!) 
            {updateLearnerMilestoneStatus (input: $input)
            }"""

        variables = {
                "input": {
                    "milestoneUid": milestoneUID,
                    "profileId": profileid,
                    "status": "COMPLETED"
                }
            }


        response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables}, headers=head)
        print(response.text)




