import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
import tkinter as tk
from tkinter import simpledialog
import datetime
import requests
import json
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuemailname = "nrccua.signup+" + TS + "@gmail.com"
vc = "123456"
token = "0"



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
    json_response = response.json()
    print (json_response["data"]["login"]["token"])
    token = (json_response["data"]["login"]["token"])
    assert response.status_code == 200



@logTestName
def test_post_profile_ACT():
    logger.info("POST /profile - Positive Test")
    head = {
        'Authorization': 'bearer ' + token
    }

    query = """ query 
    {
    myProfile 
        {
        profileId
        userAccount
            {
            userName
            isFederatedUser
            identityProvider
            actId
            personId
            }
        identity
            {
            firstName
            lastName
            dateOfBirth
            accountName
            }
        contact 
            {
            homeAddress
                {
                city
                state
                stateCode
                countryCode
                postalCode
                }
            email
            }
        }	
    }
    """

    response = requests.post('https://dev-aigr.act-et.org/graphql',
                             json={'query': query, 'headers': head})
    print(response.text)
    assert response.status_code == 200



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
    "email": newuemailname,
    "password": "Password1!}"
}
    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200
    print (newuemailname)

@logTestName
def test_verification_code():
    global vc
    vc = simpledialog.askstring(title="Verification Code",
                                      prompt="What's your Verification Code?:")
    # check it out
    print(vc)
    vc = str(vc)
ROOT = tk.Tk()

ROOT.withdraw()
    # the input dialog



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
    "username": newuemailname,
    "verificationCode": vc
    }
    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200


# @pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
@logTestName
def test_post_resendverification_ACT():
    logger.info("POST /resendverification - Positive Test")

    mutation = """ mutation ($username: String!) 
    {  
    resendUserAccountVerificationCode(input:
        {
        username:$username  
        })
        {
        message
        }
    }
    """

    variables = {
        "username": "nrccua.signup+202108044@gmail.com"
    }
    response = requests.post('https://dev-aigr.act-et.org/graphql',
                             json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200






# @pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
@logTestName
def test_post_forgotpassword_ACT():
    logger.info("POST /forgotpassword - Positive Test")

    mutation = """ mutation ($username: String!) 
    {
    forgotPassword(input: 
        {
        username:$username
        }) 
        {
        message
        }
    }
    """
    variables = {
    "username": newuemailname
    }

    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200


@logTestName
def test_verification_code2():
    global vc
    vc = simpledialog.askstring(title="Verification Code",
                                      prompt="What's your Verification Code?:")
    # check it out
    print(vc)
    vc = str(vc)
ROOT = tk.Tk()

ROOT.withdraw()
    # the input dialog



@logTestName
def test_post_completeforgotpassword_ACT():
    logger.info("POST /completeforgotpassword - Positive Test")

    mutation = """ mutation ($username: String!, $newPassword: String!, $verificationCode: String!) 
    {
    completeForgotPassword(input: 
        {
        verificationCode: $verificationCode,
        username: $username,
        newPassword: $newPassword,
        }) 
        {
        message
        }
    }
    """
    variables = {
    "username": newuemailname,
    "newPassword": "Password1!!",
    "verificationCode": vc
    }

    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    assert response.status_code == 200



@logTestName
def test_post_loginwithnewpassword_ACT():
    logger.info("POST /loginwithnewpassword - Positive Test")

    mutation = """ mutation ($username: String!, $password: String!) 
    {
    login(input: 
        {username:$username, password:$password})
        {
        token
        profileId
        }
    }
    """
    variables = {
    "username": newuemailname,
    "password": "Password1!!",
    }

    response = requests.post('https://dev-aigr.act-et.org/graphql', json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print(json_response["data"]["login"]["token"])
    assert response.status_code == 200



