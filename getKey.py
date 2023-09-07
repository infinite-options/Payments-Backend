
import stripe
import json
import os
import requests
import datetime

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mail import Mail, Message
# from dotenv import load_dotenv, find_dotenv
from email import message


# STEP 1: Setup Stripe
# Get the correct Keys
class getCorrectKeys(Resource):
    def __call__(self):
        print("In Call")

    def post(self, businessId):
        # Business Code sent in as a parameter from frontend
        print("Step 1: Get Correct Keys")
        print("business: ", businessId)

        # FOR LOCAL TESTING
        # print("In Local Testing")    
        # if businessId == "M4ME":
        #     PUBLISHABLE_KEY = "M4ME_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "M4ME_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "M4METEST":
        #     PUBLISHABLE_KEY = "pk_test_51HyqrgLMju5RPMEvtVH4G5lX2XoAjV9dTn0gE9dJ31UW4oy2joF7qjo3lP1Z90pADoMwIS9YY8UTyYfjxwdN1BrV007QZEgxtf"
        #     SECRET_KEY = "sk_test_51HyqrgLMju5RPMEvwirVtSGoCPyU1IaorHsOI1Pr1ABkR8dEpk2MAWBAIT9ZHPtbWHhjvEFwP11jLVC4h7TZhdu000mBRlnir9"
        # elif businessId == "NITYA":
        #     PUBLISHABLE_KEY = "NITYA_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "NITYA_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "NITYATEST":
        #     PUBLISHABLE_KEY = "pk_test_51J0UzOLGBFAvIBPFJbfSOn5SboZ4sX5TOrklg3o45EQywUNwxTameQVrEF9BZfmcU6WtkUFVQ2xvASNLC6tVLhdK00E1kJtmzH"
        #     SECRET_KEY = "sk_test_51J0UzOLGBFAvIBPFAm7Y5XGQ5APRxzzUeVJ1G1VdV010gW0bGzbDZsdM7fNeFDRs0WTenXV4Q9ANpztS7Y7ghtwb007quqRPZ3"
        # elif businessId == "SF":
        #     PUBLISHABLE_KEY = "SN_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "SN_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "SFTEST":
        #     PUBLISHABLE_KEY = "pk_test_6RSoSd9tJgB2fN2hGkEDHCXp00MQdrK3Tw",
        #     SECRET_KEY = "sk_test_fe99fW2owhFEGTACgW3qaykd006gHUwj1j",
        # elif businessId == "PM":
        #     PUBLISHABLE_KEY = "PM_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "PM_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "PMTEST":
        #     PUBLISHABLE_KEY = "pk_test_51LiLgbAdqquNNobLdqsqIFwoOeEHHPIreP9mTR96BxYlpNvEwKGqTgUoRvifGpr3xvk0UhQqYgW1Y5MPcyDl1xNh00aEzp41ro"
        #     SECRET_KEY = "sk_test_51LiLgbAdqquNNobLU7BiHIWUqfuDLXgYiYph8LmAb387UevA28B2YGOMFmhSNekAbz3yvI1XwKq8OIVK0ef75klh00Z38zfhYx"
        # elif businessId == "IOPAYMENT":
        #     PUBLISHABLE_KEY = "IOPAYMENTS_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "IOPAYMENTS_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "IOTEST":
        #     PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
        #     SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"
        # else:
        #     PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
        #     SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"

        # FOR LIVE TESTING
        print("In Live Mode")
        if businessId == "M4ME":
            PUBLISHABLE_KEY = os.environ.get("M4ME_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("M4ME_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "M4METEST":
            PUBLISHABLE_KEY = os.environ.get("M4ME_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("M4ME_STRIPE_TEST_SECRET_KEY")
        elif businessId == "NITYA":
            PUBLISHABLE_KEY = os.environ.get("NITYA_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("NITYA_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "NITYATEST":
            PUBLISHABLE_KEY = os.environ.get("NITYA_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("NITYA_STRIPE_TEST_SECRET_KEY")
        elif businessId == "SF":
            PUBLISHABLE_KEY = os.environ.get("SN_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("SN_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "SFTEST":
            PUBLISHABLE_KEY = os.environ.get("SN_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("SN_STRIPE_TEST_SECRET_KEY")
        elif businessId == "PM":
            PUBLISHABLE_KEY = os.environ.get("PM_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("PM_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "PMTEST":
            PUBLISHABLE_KEY = os.environ.get("PM_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("PM_STRIPE_TEST_SECRET_KEY")
        elif businessId == "IOPAYMENT":
            PUBLISHABLE_KEY = os.environ.get("IOPAYMENTS_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("IOPAYMENTS_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "IOTEST":
            PUBLISHABLE_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_SECRET_KEY")
        elif businessId == "ACH":
            PUBLISHABLE_KEY = "pk_test_51NkKHkFXblfqA49hJnh8bdxgRzvhtaACstCkJQIO4Sq4szBeomcdKTCh4tsMbuc8SiATjA8IPqcwkvnLENclDZJX00TsjxpFYU"
            SECRET_KEY = "sk_test_51NkKHkFXblfqA49hU9dmIuuuGAzNxnFusrLHWxwrQRxXLSJP0p0RGmL4SIhSltKqLOcRf81sV6z54HRIRQi8tO7r006CE4Tevp"
        else:
            PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
            SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"


        # print("PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
        # print("SECRET_KEY: ", SECRET_KEY)
        stripe.api_key = SECRET_KEY
        stripe.api_version = None

        return {"PUBLISHABLE_KEY": PUBLISHABLE_KEY, "SECRET_KEY": SECRET_KEY}