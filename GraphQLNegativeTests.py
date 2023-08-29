import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
import tkinter as tk
from tkinter import simpledialog
import datetime
import requests
import json
import re
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuemailname = "nrccua.signup+" + TS + "@gmail.com"
vc = "123456"
token = "0"
profileid = "0"

#Invalid Login
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
    "username": "nrccua.signup+20210804265465152165@gmail.com",
    "password": "Password1!"}

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["errors"][0]["message"])
    print (message)
    assert response.status_code == 200
    assert (message == 'Incorrect username or password.')


#User under 13 years of age
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
        dateOfBirth:"12/30/2020"
        communicationPreference:EMAIL
        addressCity:""
        addressState:""
        addressStateCode:""
        addressCountry:""
        addressCountryCode: "US"
        addressPostalCode: "52240"
        addressStreet1: ""
        phone:""
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
    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["errors"][0]["message"])
    print(message)
    assert response.status_code == 200
    assert re.match("BadRequestException: You must be at least 13 years old to create an ACT account", message)
    print (newuemailname)

#Valid registration
@logTestName
def test_post_register2_ACT():
    logger.info("POST /register2 - Positive Test")

    mutation = """ mutation ($email: String!, $password: String!) 
    {
    registerUser(input:
        {
        email:$email
        firstName: "Test"
        lastName: "User"
        password:$password
        dateOfBirth:"12/30/2003"
        communicationPreference:EMAIL
        addressCountry:"United States"
        addressCountryCode: "US"
        addressPostalCode: "52240"
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
    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    profileID = (json_response["data"]["registerUser"]["profileId"])
    assert response.status_code == 200
    assert (profileID != '')
    print(newuemailname)

#Trying to login without account validation
@logTestName
def test_post_login2_ACT():
    logger.info("POST /login2 - Positive Test")

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
    "username": newuemailname,
    "password": "Password1!"}

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["errors"][0]["message"])
    print (message)
    assert response.status_code == 200
    assert (message == 'User is not confirmed.')

#user account exists
@logTestName
def test_post_useraccountexists_ACT():
    logger.info("POST /useraccountexists - Positive Test")

    query = """ query 
    userAccountExists($username: String!)
    {
    userAccountExists(username: $username)
    }
    """
    variables = {
        "username": newuemailname}

    response = requests.post(apollo_helpers.graphQL, json={'query': query, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print(json_response["data"]["userAccountExists"])
    global status
    status = (json_response["data"]["userAccountExists"])
    assert response.status_code == 200
    assert (status == True)

#Invalid Postal Code
def test_post_postalcodeinfo_ACT():
    logger.info("POST /postalcodeinfo - Positive Test")

    query = """ query 
    postalCodeInfoQuery($postalCode: String!) 
    {
    postalCodeInfo(postalCode:$postalCode)
        {
        city
        stateCode
        postalCode
        }
    }
    """
    variables = {
        "postalCode": "00000"}

    response = requests.post(apollo_helpers.graphQL, json={'query': query, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print(json_response["data"]["postalCodeInfo"])
    global sc
    pci = (json_response["data"]["postalCodeInfo"])
    assert response.status_code == 200
    assert (pci == None)


#Verify user - invalid verification code
@logTestName
def test_verify_user_invalid():
    logger.info("POST /verifyuserinvalid - Positive Test")

    mutation = """ mutation ($username: String!, $verificationCode: String!) {
    verifyUser(input:{
        username:$username,
        verificationCode:$verificationCode
        })
        {
        message
        }
    }
    """
    variables = {
    "username": newuemailname,
    "verificationCode": "111111"}

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["errors"][0]["message"])
    print (message)
    assert response.status_code == 200
    assert (message == 'Verification not successful. Invalid verification code provided, please try again.')


#Verify user - invalid user
@logTestName
def test_verify_user_invalid2():
    logger.info("POST /verifyuserinvalid2 - Positive Test")

    mutation = """ mutation ($username: String!, $verificationCode: String!) {
    verifyUser(input:{
        username:$username,
        verificationCode:$verificationCode
        })
        {
        message
        }
    }
    """
    variables = {
    "username": "x@x.com",
    "verificationCode": "111111"}

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["errors"][0]["message"])
    print (message)
    assert response.status_code == 200
    assert (message == 'Verification not successful. User does not exist.')

# Forgot Password - invalid user
#@logTestName
#def test_forgot_password_invalid():
#    logger.info("POST /forgotpasswordinvalid - Positive Test")

#    mutation = """ mutation ($username: String!) {
#      forgotPassword(input: {
#        username:$username
#       }) {
#
#         message
#       }
#     }
#     """
#     variables = {
#     "username": "x@x.x"}
#
#     response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
#     print(response.text)
#     json_response = response.json()
#     message = (json_response["data"]["forgotPassword"])
#     print(message)
#     assert response.status_code == 200
#     assert (message == 'Cannot reset password for the user as there is no registered/verified email or phone_number')
