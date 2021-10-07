import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
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

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print (json_response["data"]["login"]["token"])
    global token
    token = (json_response["data"]["login"]["token"])
    assert response.status_code == 200
    assert (token != '')



@logTestName
def test_post_profile_ACT():
    logger.info("POST /profile - Positive Test")
    head = {
        "Authorization": "bearer " + token
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

    response = requests.post(apollo_helpers.graphQL, json={'query': query}, headers=head)
    print(response.text)
    json_response = response.json()
    profileid = (json_response["data"]["myProfile"]["profileId"])
    assert response.status_code == 200
    assert (profileid != '')


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
    print (json_response["data"]["userAccountExists"])
    global status
    status = (json_response["data"]["userAccountExists"])
    assert response.status_code == 200
    assert (status != 'true')

@logTestName
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
        "postalCode": "52240"}

    response = requests.post(apollo_helpers.graphQL, json={'query': query, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print(json_response["data"]["postalCodeInfo"]["stateCode"])
    global sc
    sc = (json_response["data"]["postalCodeInfo"]["stateCode"])
    assert response.status_code == 200
    assert (sc == 'IA')


@logTestName
def test_post_register_ACT():
    global vcode
    logger.info("POST /register - Positive Test")

    mutation = """ mutation ($email: String!, $password: String!) 
    {
    registerUser(input:
        {
        email:$email
        firstName: "Test"
        lastName: "User"
        middleName:""
        password:$password
        dateOfBirth:"12/30/2001"
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
    "password": "Password1!"
}
    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    profileID = (json_response["data"]["registerUser"]["profileId"])
    assert response.status_code == 200
    assert (profileID != '')
    print (newuemailname)


    # Give the email some time to arrive
    time.sleep(20)

    #semail = 'NRCCUA.SIGNUP+20211007160636@GMAIL.COM'
    #Retrieve the 6 digit verification code through email
    mail=imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login('nrccua.signup@gmail.com','Nrccua1!')
    mail.select('inbox')
    amt = len(mail.search(None, "ALL")[1][0].split())
    #print(amt)
    for i in range(amt, amt - 10, -1):
        try:
            data = mail.fetch(str(i), "(RFC822)")
            msg = email.message_from_string(str(data[1][0][1], "utf-8"))
            if (
                newuemailname.upper() in msg["to"]
                and "Activate ACT Account" in msg["subject"]
            ):
                body = msg.get_payload()[0].get_payload()
                print(body)
                vcode = body[body.find("verification code:") + 19:]
                for j in range(0, len(vcode)):
                    if vcode[j].isnumeric():
                        vcode = vcode[j: j + 6]
                        break
                print (vcode)
        except Exception:
            continue

    vcode = str(vcode)

#@logTestName
#def test_verification_code():
#    global vc
#    vc = simpledialog.askstring(title="Verification Code",
#                                      prompt="What's your Verification Code?:")
    # check it out
#    print(vc)
#    vc = str(vc)
#ROOT = tk.Tk()

#ROOT.withdraw()
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
    "verificationCode": vcode
    }
    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["data"]["verifyUser"]["message"])
    assert response.status_code == 200
    assert (message == 'Account verified successfully')


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
        "username": "nrccua.signup+202108062@gmail.com"
    }
    response = requests.post(apollo_helpers.graphQL,
                             json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["data"]["resendUserAccountVerificationCode"]["message"])
    assert response.status_code == 200
    assert (message == 'Verification code resent successfully.')






# @pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
@logTestName
def test_post_forgotpassword_ACT():
    logger.info("POST /forgotpassword - Positive Test")
    global vcode
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

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["data"]["forgotPassword"]["message"])
    assert response.status_code == 200
    assert (message == "A password reset notification has been sent to your EMAIL")

    # Give the email some time to arrive
    time.sleep(20)

    #Retrieve the 6 digit verification code through email
    mail=imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login('nrccua.signup@gmail.com','Nrccua1!')
    mail.select('inbox')
    amt = len(mail.search(None, "ALL")[1][0].split())
    #print(amt)
    for i in range(amt, amt - 10, -1):
        try:
            data = mail.fetch(str(i), "(RFC822)")
            msg = email.message_from_string(str(data[1][0][1], "utf-8"))
            if (
                newuemailname.upper() in msg["to"]
                and "Reset ACT Account Password" in msg["subject"]
            ):
                body = msg.get_payload()[0].get_payload()
                print(body)
                vcode = body[body.find("password code:") + 15:]
                for j in range(0, len(vcode)):
                    if vcode[j].isnumeric():
                        vcode = vcode[j: j + 6]
                        break
                print (vcode)
        except Exception:
            continue

    vcode = str(vcode)




#@logTestName
#def test_verification_code2():
#    global vc
#    vc = simpledialog.askstring(title="Verification Code",
#                                      prompt="What's your Verification Code?:")
#    # check it out
#    print(vc)
#    vc = str(vc)
#ROOT = tk.Tk()

#ROOT.withdraw()
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
    "verificationCode": vcode
    }

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    message = (json_response["data"]["completeForgotPassword"]["message"])
    assert response.status_code == 200
    assert (message == "Password changed successfully.")



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

    response = requests.post(apollo_helpers.graphQL, json={'query': mutation, 'variables': variables})
    print(response.text)
    json_response = response.json()
    print(json_response["data"]["login"]["token"])
    token = (json_response["data"]["login"]["token"])
    assert response.status_code == 200
    assert (token != '')


