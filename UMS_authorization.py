import apollo_helpers
from apollo_helpers import get, post, put, delete, responseTest, responseNegTest, logBody, logTestName
from loguru import logger
import pyodbc
import datetime
import tkinter as tk
from tkinter import simpledialog
import pytest
TS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
newuemailname = "nrccua.signup+" + TS + "@gmail.com"
vc = "123456"




############creation of a user for testing below################
#@pytest.mark.skipif(apollo_helpers.ENVNAME == 'prod', reason='data creation')
@logTestName
def test_post_register():
    logger.info("POST /register - Positive Test")

    payload = {
          "application": "apollo",
          "email": newuemailname,
          "password": "Password1!",
          "firstName": "SamTest",
          "lastName": "Smith",
          "dateOfBirth": "03/03/2003",
          "communicationPreference": "EMAIL",
          "addressCity": "Tampa",
          "addressState": "Florida",
          "addressStateCode": "FL",
          "addressCountry": "United States of America",
          "addressCountryCode": "US",
          "addressPostalCode": "90011",
          "addressStreet1": "1 Main Street",
          "phone": "+15555555555",
          "tncVersion": "2B51CDDB-9CD2-11E8-9D82-0A8F77C6E070",
          "acceptedTerms": True
    }

    response = post('/register', payload)
    print(response.body)
    responseTest(response.status, 201)

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



@logTestName
def test_post_verify_user():
    logger.info("POST /verify-user - Positive Test")

    payload = {
    "email": newuemailname,
    "verificationCode": vc,
    "application": "apollo"
    }

    response = post('/verify-user', payload)
    print(response.body)
    responseTest(response.status, 200)


@logTestName
def test_post_authenticatev2():
    logger.info("POST /authenticatev2 - Positive Test")

    payload = {
      "userName": newuemailname,
      "password": "Password1!",
       "expiresIn": "10m",
      "application": "apollo"
    }

    response = post('/authenticatev2', payload)
    print(response.body)
    responseTest(response.status, 200)


@logTestName
def test_post_request_password():
    logger.info("POST /request-password - Positive Test")

    payload = {
      "email": newuemailname,
      "application": "apollo"
    }

    response = post('/request-password', payload)
    print(response.body)
    responseTest(response.status, 200)


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
def test_post_confirm_password():
    logger.info("POST /confirm-password - Positive Test")

    payload = {
      "email": newuemailname,
      "verificationCode": vc,
      "newPassword": "New1password!",
      "application": "apollo"
    }

    response = post('/confirm-password', payload)
    print(response.body)
    responseTest(response.status, 200)



