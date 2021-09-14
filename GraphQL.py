import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
import datetime
import requests
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuemailname = "nrccua.signup+" + TS + "@gmail.com"




# @pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
#@logTestName
#def test_post_login():
#    logger.info("POST /login - Positive Test")

#    mutation = """mutation
#    {
#        login(input:
#        {username:"nrccua.signup+202108042@gmail.com",password:"Password1!"})
#        {
#            token
#        }
#    }
#    """

#    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation})
#    print(response.text)
#    assert(response.status_code, 200)


# @pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
@logTestName
def test_post_register_ACT():
    logger.info("POST /register - Positive Test")

    mutation = """ mutation ($email: String!, $password: String!) 
    {
    registerUser(input:
        {
        email:$email
        firstName: "Test"
        lastName: "User"
        middleName:"D"
        password:$password
        dateOfBirth:"12/30/2001"
        communicationPreference:EMAIL
        addressCity:"Iowa City"
        addressState:"Iowa"
        addressStateCode:"IA"
        addressCountry:"United States"
        addressCountryCode: "US"
        addressPostalCode: "52240"
        addressStreet1: "111 2nd Street"
        phone:"+123456789"
        tncVersion: "2B51CDDB-9CD2-11E8-9D82-0A8F77C6E070"})
        {
        username
        userId
        profileId
        }
    }
    """

    variables = {
    "email": "nrccua.signup+202108045@gmail.com",
    "password": "Password1!}"
}
    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200

# @pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
@logTestName
def test_post_verifyuser_ACT():
    logger.info("POST /verifyuser - Positive Test")

    mutation = """ mutation ($username: String!, $verificationCode: String!) 
    {
    verifyUser(input:
        {
        username:$username,
        verificationCode:$verificationCode})
        {
        message
        }
    }
    """

    variables = {
    "username": "nrccua.signup+202108044@gmail.com",
    "verificationCode": "480078"
    }
    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200


# @pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
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
    "username": "nrccua.signup+202108042@gmail.com",
    "password": "Password1!"}

    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200



