# File from https://stripe.com/docs/payments/accept-a-payment?ui=elements
# Accept a Payment > Custom Payment Flow
# Copied from View Full Sample in Step 2
# #! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

import stripe
import json
import os
import requests

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv


# static_dir = str(os.path.abspath(os.path.join(__file__, "..", os.getenv("STATIC_DIR"))))
# app = Flask(
#     __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
# )
app = Flask(__name__)
# cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
CORS(app)

# API
api = Api(app)


# STEP 1: Setup Stripe
# Get the correct Keys
class getCorrectKeys(Resource):
    def __call__(self):
        print("In Call")

    def post(self, businessId):
        # Business Code sent in as a parameter from frontend
        print("Step 1: Get Correct Keys")
        businessID = businessId
        print("business: ", businessId)

        # FOR LOCAL TESTING
        # print("In Try Block")
        # if businessId == "M4ME":
        #     PUBLISHABLE_KEY = "M4ME_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "M4ME_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "M4METEST":
        #     PUBLISHABLE_KEY = "M4ME_STRIPE_TEST_PUBLISHABLE_KEY"
        #     SECRET_KEY = "M4ME_STRIPE_TEST_SECRET_KEY"
        # elif businessId == "SF":
        #     PUBLISHABLE_KEY = "SN_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "SN_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "SFTEST":
        #     PUBLISHABLE_KEY = "SN_STRIPE_TEST_PUBLISHABLE_KEY"
        #     SECRET_KEY = "SN_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "IOPAYMENT":
        #     PUBLISHABLE_KEY = "IOPAYMENTS_STRIPE_LIVE_PUBLISHABLE_KEY"
        #     SECRET_KEY = "IOPAYMENTS_STRIPE_LIVE_SECRET_KEY"
        # elif businessId == "IOTEST":
        #     PUBLISHABLE_KEY = "IOPAYMENTS_STRIPE_TEST_PUBLISHABLE_KEY"
        #     SECRET_KEY = "IOPAYMENTS_STRIPE_TEST_SECRET_KEY"
        # else:
        #     PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
        #     SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"

        # FOR LIVE TESTING
        print("In Try Block")
        if businessId == "M4ME":
            PUBLISHABLE_KEY = os.environ.get("M4ME_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("M4ME_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "M4METEST":
            PUBLISHABLE_KEY = os.environ.get("M4ME_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("M4ME_STRIPE_TEST_SECRET_KEY")
        elif businessId == "SF":
            PUBLISHABLE_KEY = os.environ.get("SN_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("SN_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "SFTEST":
            PUBLISHABLE_KEY = os.environ.get("SN_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("SN_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "IOPAYMENT":
            PUBLISHABLE_KEY = os.environ.get("IOPAYMENTS_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("IOPAYMENTS_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "IOTEST":
            PUBLISHABLE_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_SECRET_KEY")
        else:
            PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
            SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"

        print("PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
        print("SECRET_KEY: ", SECRET_KEY)
        stripe.api_key = SECRET_KEY
        stripe.api_version = None

        return {"PUBLISHABLE_KEY": PUBLISHABLE_KEY, "SECRET_KEY": SECRET_KEY}


# STEP 2: Create a Customer
# class createCustomerOnly(Resource):
#     def __call__(self):
#         print("In Call")

#     def get(self):

#         # Create Payment Intent
#         # Create customer.  Need this step to save CC info
#         # Returns a Customer ID Created by Stripe
#         print("Step 2")
#         print("stripe PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
#         customer = stripe.Customer.create()
#         print("customer: ", customer)
#         customerId = customer.id
#         print("customer ID: ", customerId)

#         return customerId


class createNewCustomer(Resource):
    def __call__(self):
        print("In Call")

    def post(self, customer_uid):
        # Customer UID sent in from frontend
        print("Step 2")

        # data = request.get_json(force=True)
        # print("data: ", data)
        # customerUid = data["customer_uid"]
        print("customer: ", customer_uid)

        # Check if Stripe does NOT already have the Customer UID
        try:
            # IF Stripe has the UID then it cannot create another customer with same UID THEN try will fail
            # IF it does NOT have the UID then it will create the customer
            customer = stripe.Customer.create(id=customer_uid)
            print("New Customer ID created!")
            newCustomer = True
        except:
            # IF Stripe has the UID, it will retrieve the info and print it
            print("Found Customer ID!")
            stripe.Customer.retrieve(customer_uid)
            # stripe.Customer.retrieve("cus_JKUnLFjlbjW2PG")
            print("Customer Info: ", stripe.Customer.retrieve(customer_uid))
            newCustomer = False

        return newCustomer


# STEP 3: Create a Payment Intent
class createPaymentIntentOnly(Resource):
    def __call__(self):
        print("In Call")

    def get(self):

        # Create Payment Intent
        print("Step 3")
        intent = stripe.PaymentIntent.create(
            amount=1099,
            currency="usd",
            # Verify your integration in this guide by including this parameter
            # metadata={'integration_check': 'accept_a_payment'},
            customer="100-000009",
        )
        print("intent: ", intent)
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return client_secret

    def post(self, customer_uid, charge_amount):

        # Create Payment Intent with Customer ID
        print("Step 3")
        print("stripe sk: ", stripe.api_key)
        # data = request.get_json(force=True)
        # print("data: ", data)
        intent = stripe.PaymentIntent.create(
            amount=charge_amount,
            currency="usd",
            # Verify your integration in this guide by including this parameter
            # metadata={'integration_check': 'accept_a_payment'},
            # customer="cus_JKUnLFjlbjW2PG",
            customer=customer_uid,
            # customer='{{CUSTOMER_ID}}',
            # payment_method="pm_1IhpoELMju5RPMEvq6B92VsG",
            # payment_method='{{PAYMENT_METHOD_ID}}',
            # off_session=True,
            # confirm=True,
        )
        print("intent: ", intent)
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return client_secret


class createPaymentIntent(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("data: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        print("customer: ", customer_uid)
        print("business: ", businessId)
        print("amount: ", charge_amount)

        print("In Step 1")
        keys = getCorrectKeys.post(self, businessId)
        print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])

        print("In Step 2")
        newCustomer = createNewCustomer.post(self, customer_uid)
        print(newCustomer)

        print("In Step 3")
        paymentIntent = createPaymentIntentOnly.post(self, customer_uid, charge_amount)
        print(paymentIntent)

        return {
            "PK": keys["PUBLISHABLE_KEY"],
            "NewCustomer": newCustomer,
            "pi": paymentIntent,
        }


# Define API routes
# NEW BASE URL:  https://huo8rhh76i.execute-api.us-west-1.amazonaws.com/dev/
api.add_resource(getCorrectKeys, "/api/v2/getCorrectKeys/<string:businessId>")
api.add_resource(createNewCustomer, "/api/v2/createNewCustomer/<string:customer_uid>")
# api.add_resource(createCustomerOnly, "/api/v2/createCustomerOnly<string:customer_uid>")
api.add_resource(createPaymentIntent, "/api/v2/createPaymentIntent")


if __name__ == "__main__":
    # app.run()
    app.run(host="127.0.0.1", port=2000)