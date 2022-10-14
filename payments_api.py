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
from flask_mail import Mail, Message
# from dotenv import load_dotenv, find_dotenv
import datetime

from email import message



# static_dir = str(os.path.abspath(os.path.join(__file__, "..", os.getenv("STATIC_DIR"))))
# app = Flask(
#     __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
# )
app = Flask(__name__)
# cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
CORS(app)

# API
api = Api(app)

# --------------- Mail Variables ------------------
# Mail username and password loaded in .env file

# app.config['MAIL_USERNAME'] = "support@infiniteoptions.com"
# app.config['MAIL_PASSWORD'] = "Support***"
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# app.config['MAIL_USERNAME'] = os.getenv('SUPPORT_EMAIL')
# app.config['MAIL_PASSWORD'] = os.getenv('SUPPORT_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

app.config['MAIL_USERNAME'] = os.environ.get('SUPPORT_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('SUPPORT_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')


# Setting for mydomain.com
app.config["MAIL_SERVER"] = "smtp.mydomain.com"
app.config["MAIL_PORT"] = 465

# Setting for gmail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465


app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

# Set this to false when deploying to live application
# app.config["DEBUG"] = True
app.config["DEBUG"] = False

# app.config["STRIPE_SECRET_KEY"] = os.getenv("STRIPE_SECRET_KEY")

mail = Mail(app)


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
        else:
            PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
            SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"


        print("PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
        print("SECRET_KEY: ", SECRET_KEY)
        stripe.api_key = SECRET_KEY
        stripe.api_version = None

        return {"PUBLISHABLE_KEY": PUBLISHABLE_KEY, "SECRET_KEY": SECRET_KEY}


# STEP 2: Create a Customer
class createCustomerOnly(Resource):
    def __call__(self):
        print("In Call")

    def get(self):

        # Create Payment Intent
        # Create customer.  Need this step to save CC info
        # Returns a Customer ID Created by Stripe
        print("Step 2 createCustomerOnly")
        PUBLISHABLE_KEY = "pk_test_51J0UzOLGBFAvIBPFJbfSOn5SboZ4sX5TOrklg3o45EQywUNwxTameQVrEF9BZfmcU6WtkUFVQ2xvASNLC6tVLhdK00E1kJtmzH"
        print("stripe PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
        SECRET_KEY = "sk_test_51J0UzOLGBFAvIBPFAm7Y5XGQ5APRxzzUeVJ1G1VdV010gW0bGzbDZsdM7fNeFDRs0WTenXV4Q9ANpztS7Y7ghtwb007quqRPZ3"
        stripe.api_key = SECRET_KEY
        print("stripe sk: ", stripe.api_key)
        customer = stripe.Customer.create()
        print("customer: ", customer)
        customerId = customer.id
        print("customer ID: ", customerId)

        return customerId


class createNewCustomer(Resource):
    def __call__(self):
        print("In Call")

    def post(self, customer_uid):
        # Customer UID sent in from frontend
        print("Step 2 createNewCustomer")

        # data = request.get_json(force=True)
        # print("data: ", data)
        # customerUid = data["customer_uid"]
        print("customer: ", customer_uid)
        print("stripe sk: ", stripe.api_key)


        # Check if Stripe does NOT already have the Customer UID
        try:
            # IF Stripe has the UID then it cannot create another customer with same UID THEN try will fail
            # IF it does NOT have the UID then it will create the customer

            stripe.Customer.create(id=customer_uid)
            print("New Customer ID created!", customer_uid)
            newCustomer = True
            # Send Email here
            message = "New Customer created by Stripe!"
            SendEmail.get(self, message, customer_uid)
        except:
            # IF Stripe has the UID, it will retrieve the info and print it
            print("Found Customer ID!")
            stripe.Customer.retrieve(customer_uid)
            # stripe.Customer.retrieve("cus_JKUnLFjlbjW2PG")
            print("Customer Info: ", stripe.Customer.retrieve(customer_uid))
            newCustomer = False

        return newCustomer
        # return {"customer_uid": customer_uid, "newCustomer": newCustomer}


# STEP 3: Create a Payment Intent
class createPaymentIntentOnly(Resource):
    def __call__(self):
        print("In Call")

    def get(self):

        # Create Payment Intent
        print("Step 3 - Get Request.  Values are hard coded")
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
        # Comment out print("intent: ", intent) to avoid excess CloudWatch entries
        # print("intent: ", intent)
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return client_secret


# STEP 1,2,3 COMBINED: Create a Payment Intent
class createPaymentIntent(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("data: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        # print("customer: ", customer_uid)
        # print("business: ", businessId)
        # print("amount: ", charge_amount)

        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])


        print("\nIn Step 2")
        if customer_uid == "":
            # Send email here
            message = "No Customer ID sent"
            SendEmail.get(self, message, data)
            customer = stripe.Customer.create()
            customer_uid = customer.id
            print("Created New Customer ID: ", customer_uid)

        newCustomer = createNewCustomer.post(self, customer_uid)
        # print(newCustomer)
        print("customer_uid: ", customer_uid)


        print("\nIn Step 3")
        try: 
            paymentIntent = createPaymentIntentOnly.post(self, customer_uid, charge_amount)
            print(paymentIntent)
        except: 
            # Send email here
            message = "Payment Intent could not be created"
            SendEmail.get(self, message, data)
            print("Error Occurred")
            paymentIntent = "Notify customer that system is down"

        return paymentIntent


# Step 4: Payment method with card and billing details entirely on the Front End

# Step 5: Submit Payment to Stripe is handled entirely on the Front End


# Step 6: Submit Off Session payment to Strip
class createOffSessionPaymentIntent(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("\ndata: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        print("customer: ", customer_uid)
        print("business: ", businessId)
        print("amount: ", charge_amount)

        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        print("stripe api key: ", stripe.api_key)
        stripe.api_version = None

        print("\nIn Step 6")
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
            payment_method=stripe.PaymentMethod.list(
                customer=data["customer_uid"],
                type="card",
            )
            .data[0]
            .id,
            off_session=True,
            confirm=True,
        )

        print("\nPayment Intent: ", intent.id)
        print("Payment Intent with Secret: ", intent.client_secret)
        print("Charge ID: ", intent.charges.data[0].id)
        print("\nintent: ", intent)
        chargeId = intent.charges.data[0].id
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return chargeId


# Send Email
class SendEmail(Resource):
    def __call__(self):
        print("In SendEmail")

    # def get(self, message):
    def get(self, message, data):
        print("\nIn SendEmail")
        response = {}
        try:
            # conn = connect()
            # message = "test"
            # print("first email sent")
            print("Message to send: ", message)
            print("Data to send: ", data, type(data))
            # Send email to Host
            msg = Message(
                "Payment Error Occurred",
                sender="support@infiniteoptions.com",
                recipients=["pmarathay@gmail.com"],
            )
            print(msg)
            msg.body = (
                "Hi !\n\n"
                "You just got an email from your website! \n"
                "Here are the particulars:\n"
                # "Name:      " + name + "\n"
                # "Email:     " + email + "\n"
                # "Phone:     " + str(phone) + "\n"
                # "Subject:   " + subject + "\n"
                "Message:   " + message + "\n"
                "Data Sent: " + str(data) + "\n"
            )
            print(msg)
            # "Thx - Nitya Ayurveda\n\n"
            # print(msg)
            # print('msg-bd----', msg.body)
            mail.send(msg)
            print('\nafter mail send')

            # # Send email to Sender
            # msg2 = Message(
            #     "New Email from Nitya Ayurveda!",
            #     sender="support@infiniteoptions.com",
            #     recipients=[email],
            # )
            # msg2.body = (
            #     "Hi !\n\n"
            #     "Thanks for your email! \n"
            #     "Here are the particulars we sent:\n"
            #     "Name:      " + name + "\n"
            #     "Email:     " + email + "\n"
            #     "Phone:     " + str(phone) + "\n"
            #     "Subject:   " + subject + "\n"
            #     "Message:   " + message + "\n"
            # )
            # "Thx - Nitya Ayurveda\n\n"
            # # print('msg-bd----', msg.body)
            # mail.send(msg2)
            # print('after mail send')

            return 'Email Sent', 200

        except:
            print("Error Occurred - except")

# Retrieve Stripe Info - Utilities
class retrieveStripeCharge(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("\ndata: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        print("customer: ", customer_uid)
        print("business: ", businessId)
        print("amount: ", charge_amount)

        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        print("stripe api key: ", stripe.api_key)
        stripe.api_version = None

        # # Retrieve Charge ID (Typically from Mobile) - works
        # # Charge ID has a SUBSET of Payment Intent
        print("\nRetrieve Charge ID Info")
        retrieveInfo = stripe.Charge.retrieve("ch_1J32t7LMju5RPMEvMSe2q863")
        print("Last 4: ", retrieveInfo.payment_method_details.card.last4)
        print("Stripe Charge ID Info: ", retrieveInfo)

        # # Retrieve Payment Intent (Typically from Web or Postman) - -works
        # # Payment Intent has Everything
        # print("\nRetrieve Payment Intent Info")
        # # retrieveInfo = stripe.PaymentIntent.retrieve("pi_1IjEA3LMju5RPMEvKBUwxxhJ") - for M4ME
        # # retrieveInfo = stripe.PaymentIntent.retrieve("pi_1Ii1DOGQZnKn7zmSWXJHNS8F")
        # retrieveInfo = stripe.PaymentIntent.retrieve("pi_1IjIVyLMju5RPMEvXlz2JalH")
        # print("\nPayment Intent: ", retrieveInfo.id)
        # print("Payment Intent with Secret: ", retrieveInfo.client_secret)
        # print("Charge ID: ", retrieveInfo.charges.data[0].id)
        # print("\nStripe Payment Intent Info: ", retrieveInfo)

        # # Retrieve Payment Method - works
        # # Payment Method has customer ID, Name, Last 4 cc, Address
        # print("\nRetrieve Payment Method Info")
        # retrieveInfo = stripe.PaymentMethod.retrieve("pm_1Ii1DOGQZnKn7zmSer9GLvPi")
        # print("Stripe Payment Method Info: ", retrieveInfo)

        # # Retrieve All Customers - works
        # print("\nRetrieve All Customers per limit")
        # retrieveInfo = stripe.Customer.list(limit=30)
        # print("Stripe All Customers Info: ", retrieveInfo)

        return retrieveInfo


class retrieveLast4(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("\ndata: ", data)
        stripe_id = data["charge_id"]
        businessId = data["business_code"]
        print("charge_id: ", stripe_id)
        print("business: ", businessId)

        print("\nIn Step 1: Get Stripe Keys")
        keys = getCorrectKeys.post(self, businessId)
        print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        print("stripe api key: ", stripe.api_key)
        stripe.api_version = None

        if stripe_id[:2] == "pi":
            stripe_id = stripe.PaymentIntent.retrieve(stripe_id).get("charges").get("data")[0].get("id")
        
        # if 'ch_' in str(stripe_id):
        if stripe_id[:2] == "ch":
            print("\nRetrieve Charge ID Info")
            retrieveInfo = stripe.Charge.retrieve(stripe_id)
            print("Last 4: ", retrieveInfo.payment_method_details.card.last4)

            return retrieveInfo.payment_method_details.card.last4

        return("Enter a valid charge id")


# Process a Refund
class refund(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("\ndata: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        refund_amount = data["refund_amount"]
        charge_id = data["charge_id"]
        # charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        print("customer: ", customer_uid)
        print("business: ", businessId)
        # print("amount: ", charge_amount)

        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        print("stripe api key: ", stripe.api_key)
        stripe.api_version = None

        # Process a Refund
        print("\nProcess a Refund")
        retrieveInfo = stripe.Refund.create(
            charge=charge_id, amount=refund_amount
        )
        print("Stripe Refund Info: ", retrieveInfo)

        return retrieveInfo

# Find Created Customers
class customerList(Resource):
    def __call__(self):
        print("In Call")


    def get(self, businessId):
        # Customer UID sent in from frontend
        print("Find Customer List Attributes")

        print("In Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])

        # customers = stripe.Customer.list(limit=100, email='pmarathay@yahoo.com')
        # customers = stripe.Customer.list(limit=100, email='pmarathay@gmail.com')
        # customers = stripe.Customer.list(limit=100, starting_after='cus_JKScM1BhOQwEik')
        # customers = stripe.Customer.list(limit=100, email='j12345l54321@gmail.com', starting_after='100-000148')
        customers = stripe.Customer.list(limit=3)

        print(customers, type(customers))

        return(customers)


    def post(self, businessId):
    # def post(self):
        # Customer UID sent in from frontend
        print("Find Entire Customer List")

        print("In Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])

        # customers = stripe.Customer.list(limit=100, email='pmarathay@yahoo.com')
        # customers = stripe.Customer.list(limit=100, email='pmarathay@gmail.com')
        # customers = stripe.Customer.list(limit=100, starting_after='cus_JKScM1BhOQwEik')
        # customers = stripe.Customer.list(limit=100, email='j12345l54321@gmail.com', starting_after='100-000148')
        # customers = stripe.Customer.list(limit=100)

        # print(customers, type(customers))
        # print(customers["data"][0]["address"]["postal_code"])
        # print(customers["data"][0]["id"])
    
        # stripe.api_key = "sk_test_51HyqrgLMju5RPMEvow...JQ5TqpGkl299bo00yD1lTRNK"


        customers = stripe.Customer.list(limit=100)
        customer_list = []
        
        n = 1
        for items in customers["data"]:
            print(n, items["id"], items["email"], datetime.datetime.fromtimestamp(items["created"]))
            customer_list.append(str(items["id"]) + ",  " + str(items["email"]) + ", " + str(datetime.datetime.fromtimestamp(items["created"])))
            if n == 99:
                stripe_index = items["id"]
            n = n + 1
        print("Additional items: ",customers["has_more"])
        # print("Stripe Index: ", stripe_index)


        while customers["has_more"] == True:
            print("\ninside if statement")
            customers = stripe.Customer.list(limit=100, starting_after=stripe_index)
            m = n
            n = n + 1
            for items in customers["data"]:
                print(n, items["id"], items["email"], datetime.datetime.fromtimestamp(items["created"]))
                # print(stripe.Customer.retrieve(items["id"]))
                
                customer_list.append(str(items["id"]) + ",  " + str(items["email"]) + ", " + str(datetime.datetime.fromtimestamp(items["created"])))
                if n - m == 99:
                    stripe_index = items["id"]
                n = n + 1
            print("Additional items: ",customers["has_more"])
            # print("Stripe Index: ", stripe_index)
            continue

        # print(stripe.Customer.retrieve("100-000127"))
        print("Finished")

        return(customer_list)


# Define API routes
# NEW BASE URL:  https://huo8rhh76i.execute-api.us-west-1.amazonaws.com/dev/
api.add_resource(getCorrectKeys, "/api/v2/getCorrectKeys/<string:businessId>")
api.add_resource(createNewCustomer, "/api/v2/createNewCustomer/<string:customer_uid>")
api.add_resource(createCustomerOnly, "/api/v2/createCustomerOnly")
api.add_resource(createPaymentIntent, "/api/v2/createPaymentIntent")
api.add_resource(retrieveStripeCharge, "/api/v2/retrieveStripeCharge")
api.add_resource(retrieveLast4, "/api/v2/retrieveLast4")

api.add_resource(createOffSessionPaymentIntent, "/api/v2/createOffSessionPaymentIntent")
api.add_resource(refund, "/api/v2/refund")
api.add_resource(customerList, "/api/v2/customerList/<string:businessId>")

api.add_resource(SendEmail, "/api/v2/sendEmail/<string:message>")


if __name__ == "__main__":
    # app.run()
    app.run(host="127.0.0.1", port=2000)