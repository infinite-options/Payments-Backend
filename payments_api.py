# File from https://stripe.com/docs/payments/accept-a-payment?ui=elements
# Accept a Payment > Custom Payment Flow
# Copied from View Full Sample in Step 2
# #! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

import os

from dotenv import load_dotenv

load_dotenv()

import stripe
import json
import requests
import datetime

from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mail import Mail, Message
from email import message

from getKey import getCorrectKeys, stripeKey
from ACH_payments import verifyACH, retrieve, status, webhook


app = Flask(__name__)
# cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
CORS(app)

# API
api = Api(app)

# --------------- Mail Variables ------------------
# Mail username and password loaded in .env file

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


# --------------- Class Definitions ------------------

# Send Email
class SendEmail(Resource):
    def __call__(self):
        print("In SendEmail")

    @staticmethod
    def send_email(message, data):
        print("\nIn SendEmail send_email")
        try:
            # conn = connect()
            # message = "test"
            # print("first email sent")
            print("Message to send: ", message)
            print("Data to send: ", data, type(data))
            print("Mail config - Username:", app.config['MAIL_USERNAME'])
            print("Mail config - Server:", app.config["MAIL_SERVER"])
            print("Mail config - Port:", app.config["MAIL_PORT"])
            print("Mail config - SSL:", app.config["MAIL_USE_SSL"])
            print("Mail config - TLS:", app.config["MAIL_USE_TLS"])


            # Send email to Host            
            # Select appropriate Message Subject
            # if message[:31] == "New Customer created by Stripe!":
            if "New Customer created by Stripe!" in message:
                msg = Message(
                    "New Customer Created",
                    sender="support@infiniteoptions.com",
                    recipients=["Lmarathay@gmail.com",
                            "pmarathay@gmail.com"],
                )
            # elif message[:31] == "No Customer ID sent":
            elif "No Customer ID sent" in message:
                msg = Message(
                    "No Customer ID sent",
                    sender="support@infiniteoptions.com",
                    recipients=["Lmarathay@gmail.com",
                            "pmarathay@gmail.com"],
                )
            # elif message[:31] == "Suspicious Charge Amount":
            elif "Suspicious Charge Amount" in message:
                msg = Message(
                    "Suspicious Charge Amount",
                    sender="support@infiniteoptions.com",
                    recipients=["Lmarathay@gmail.com",
                            "pmarathay@gmail.com"],
                )
            else:
                msg = Message(
                    "Payment Error Occurred",
                    sender="support@infiniteoptions.com",
                    recipients=["Lmarathay@gmail.com",
                            "pmarathay@gmail.com"],
                )
            # print(msg)

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

            # "Thx - Nitya Ayurveda\n\n"
            print("About to send email...")
            print("Email subject:", msg.subject)
            print("Email recipients:", msg.recipients)
            print("Email body:", msg.body)
            mail.send(msg)
            print("Email sent successfully!")
            # print('\nafter mail send')

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

        except Exception as e:
            print(f"Error sending email: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return 'Email NOT Sent', 500

    def get(self, message, data):
        return self.send_email(message, data)


# STEP 1: Setup Stripe - Get the correct Keys


# STEP 2: Create a Customer
class createCustomerOnly(Resource):
    def __call__(self):
        print("In Call")

    def get(self):

        # Create Payment Intent
        # Create customer.  Need this step to save CC info
        # Returns a Customer ID Created by Stripe
        # print("Step 2 createCustomerOnly")
        PUBLISHABLE_KEY = os.environ.get("NITYA_STRIPE_TEST_PUBLISHABLE_KEY")
        SECRET_KEY = os.environ.get("NITYA_STRIPE_TEST_SECRET_KEY")
        stripe.api_key = SECRET_KEY
        # print("stripe sk: ", stripe.api_key)
        customer = stripe.Customer.create()
        # print("customer: ", customer)
        customerId = customer.id
        # print("customer ID: ", customerId)

        return customerId


class createNewCustomer(Resource):
    def __call__(self):
        print("In Call")

    def post(self, customer_uid):
        try:
            # Customer UID sent in from frontend
            print("Step 2 createNewCustomer")

            # data = request.get_json(force=True)
            # print("data: ", data)
            # customerUid = data["customer_uid"]
            # print("customer: ", customer_uid)
            # print("stripe sk: ", stripe.api_key)
            last4 = "No Key"

            if not stripe.api_key:
                return {"error": "Stripe API key is missing or None. Check your environment variables."}, 500

            if len(stripe.api_key)>4:
                last4 = stripe.api_key[-4:]


            # Check if Stripe does NOT already have the Customer UID
            try:
                # IF Stripe has the UID then it cannot create another customer with same UID THEN try will fail
                # IF it does NOT have the UID then it will create the customer
                stripe.Customer.create(id=customer_uid)
                print("New Customer ID created!", customer_uid)
                newCustomer = True
                # Send Email here
                message = "New Customer created by Stripe! " + last4
                SendEmail.send_email(message, customer_uid)
            except stripe.error.InvalidRequestError:
                # IF Stripe has the UID, it will retrieve the info and print it
                print("Found Customer ID!")
                stripe.Customer.retrieve(customer_uid)
                # stripe.Customer.retrieve("cus_JKUnLFjlbjW2PG")
                # print("Customer Info: ", stripe.Customer.retrieve(customer_uid))
                newCustomer = False
            except Exception as e:
                print(f"Unexpected error in customer creation/retrieval: {e}")
                newCustomer = False

            return newCustomer
            # return {"customer_uid": customer_uid, "newCustomer": newCustomer}
            
        except Exception as e:
            print(f"Error in createNewCustomer: {e}")
            return {"error": "Failed to create/retrieve customer"}, 500

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
        # print("stripe sk: ", stripe.api_key)
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

# STEP 1,2,3 COMBINED: Create a STRIPE Payment Intent
class createPaymentIntent(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)
            print("data: ", data)
            customer_uid = data["customer_uid"]
            businessId = data["business_code"]
            charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
            # print("customer: ", customer_uid)
            # print("business: ", businessId)
            print("amount: ", charge_amount)



            print("\nIn Step 1")
            # Check suspicious charge amount FIRST (before any early returns)
            if charge_amount <= 99 or charge_amount >= 1000000:
                message = "Suspicious Charge Amount"
                SendEmail.send_email(message, data)
                return {"error": f"Suspicious Charge Amount: ${charge_amount/100:.2f}"}, 400
            
            # Then check customer ID validation
            if "nitya" in businessId.lower():
                if not customer_uid.startswith("100"):
                    message = "No Customer ID sent"
                    SendEmail.send_email(message, data)
                    return {"error": "Invalid customer_uid"}, 400
            
            keys = getCorrectKeys.post(self, businessId)
            # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])


            print("\nIn Step 2")
            if customer_uid == "":
                # Send email here
                message = "No Customer ID sent"
                SendEmail.send_email(message, data)
                customer = stripe.Customer.create()
                customer_uid = customer.id
                print("Created New Customer ID: ", customer_uid)

            newCustomer = createNewCustomer.post(self, customer_uid)
            # print(newCustomer)
            print("customer_uid: ", customer_uid)


            print("\nIn Step 3")
            try: 
                paymentIntent = createPaymentIntentOnly.post(self, customer_uid, charge_amount)
                # print(paymentIntent)
            except Exception as e: 
                # Send email here
                message = "Payment Intent could not be created"
                SendEmail.send_email(message, data)
                print(f"Error creating payment intent: {e}")
                paymentIntent = "Notify customer that system is down"

            return paymentIntent
            
        except ValueError as e:
            # Handle ValueError specifically
            return {"error": str(e)}, 400
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error in createPaymentIntent: {e}")
            return {"error": "Internal server error"}, 500


# Step 4: Payment method with card and billing details entirely on the Front End


# Step 5: Submit Payment to Stripe is handled entirely on the Front End


# Step 6: Submit Off Session payment to Strip
class createOffSessionPaymentIntent(Resource):
    def post(self):

        data = request.get_json(force=True)
        # print("\ndata: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        # print("customer: ", customer_uid)
        # print("business: ", businessId)
        # print("amount: ", charge_amount)

        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        # print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        # print("stripe api key: ", stripe.api_key)
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

        # print("\nPayment Intent: ", intent.id)
        # print("Payment Intent with Secret: ", intent.client_secret)
        # print("Charge ID: ", intent.charges.data[0].id)
        # print("\nintent: ", intent)
        chargeId = intent.charges.data[0].id
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return chargeId

# STEP 1,2,3 COMBINED: Create a ACH Payment Intent
endpoint_secret = 'whsec_ABNMy16Qg0QPNJUOn0e1iwKsQiupT1KA'

class createACHPaymentIntent(Resource):
    def post(self):

        data = request.get_json(force=True)
        # print("data: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        # print("customer: ", customer_uid)
        # print("business: ", businessId)
        # print("amount: ", charge_amount)

        # Step 1
        # Customer UID sent in from frontend
        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        stripe.api_version = None
        

        # STEP 2
        # Customer UID sent in from frontend  
        print("\nIn Step 2")
        if customer_uid == "":
            # Send email here
            message = "No Customer ID sent"
            SendEmail.send_email(message, data)
            customer = stripe.Customer.create()
            customer_uid = customer.id
            print("Created New Customer ID: ", customer_uid)

        newCustomer = createNewCustomer.post(self, customer_uid)
        # print(newCustomer)
        # print("customer_uid: ", customer_uid)


        # Step 3
        # Create Payment Intent with Customer ID
        print("Step 3")
        intent = stripe.PaymentIntent.create(
            amount=charge_amount,
            currency="usd",
            setup_future_usage="off_session",
            customer= customer_uid,
            payment_method_types=["us_bank_account"],
            payment_method_options={
                "us_bank_account": {
                    "verification_method": "instant",
                    "preferred_settlement_speed": "fastest",
                    "financial_connections": {"permissions": ["payment_method", "balances"]},
                },
            },
        )
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return client_secret


class createEasyACHPaymentIntent(Resource):
    def put(self):
        print("In createEasyACHPaymentIntent PUT")

        data = request.get_json()
        print(data)
        print(data["session_id"])

        businessId =str(data["business_code"])
        print(businessId, type(businessId))

        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        stripe.api_version = None

        checkout_session = stripe.checkout.Session.retrieve(data["session_id"])  
        print(checkout_session)
        print(checkout_session.payment_intent)

        if(checkout_session.payment_intent not in {None, '', 'null'}):
            ACH_pi = stripe.PaymentIntent.retrieve(checkout_session.payment_intent)
            print("ACH_pi: ", ACH_pi)
            ACH_info = json.dumps({
                "id": checkout_session.id, 
                "status": ACH_pi.status, 
                "payment_method": ACH_pi.payment_method, 
                "client_secret": ACH_pi.client_secret,
                "failure_code": ACH_pi.charges.data[0].failure_code,
                "failure_message": ACH_pi.charges.data[0].failure_message
                })
            print("ACH INFO: ", ACH_info)

            # return Response(ACH_pi.status, status=200, mimetype="application/json")
            return Response(ACH_info, status=200, mimetype="application/json")
        
        else:
            return("No ACH Session Id")

    def post(self):
        print("in create checkout session")

        data = request.get_json(force=True)
        # print("\ndata: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        site = data["site"]
        if site == "LOCAL_PM":
            pay_success="http://localhost:3000/PaymentConfirmation"
            pay_fail="http://localhost:3000/tenantDashboard"
        elif site == "PM":
            pay_success="https://iopropertymanagement.netlify.app/PaymentConfirmation"
            pay_fail="https://iopropertymanagement.netlify.app/tenantDashboard"
        else:
            pay_success="https://iopropertymanagement.netlify.app/PaymentConfirmation"
            pay_fail="https://iopropertymanagement.netlify.app/tenantDashboard"
        # purchase_desc = data["description"]
        # print("customer: ", customer_uid)
        # print("business: ", businessId)
        # print("amount: ", charge_amount)

        # Step 1
        # Customer UID sent in from frontend
        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        stripe.api_version = None
        

        # STEP 2
        # Customer UID sent in from frontend  
        print("\nIn Step 2")
        if customer_uid == "":
            # Send email here
            message = "No Customer ID sent"
            SendEmail.send_email(message, data)
            customer = stripe.Customer.create()
            customer_uid = customer.id
            print("Created New Customer ID: ", customer_uid)

        newCustomer = createNewCustomer.post(self, customer_uid)
        # print(newCustomer)
        # print("customer_uid: ", customer_uid)


        # Step 3
        # Create Payment Intent with Customer ID
        print("Step 3")
        try:
            print("in try")
            checkout_session = stripe.checkout.Session.create(
                mode="payment",
                customer=customer_uid,
                # payment_method_types=["card", "us_bank_account"],
                payment_method_types=["us_bank_account"],
                payment_method_options={
                    "us_bank_account": {
                        "financial_connections": {"permissions": ["payment_method"]}
                    },
                },
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": charge_amount,
                            "product_data": {"name": "Property Rent and Fees"},
                        },
                        "quantity": 1,
                    },
                ],

                success_url = pay_success,
                cancel_url  = pay_fail,

            )

            print("checkout_session: ", checkout_session)
            print("checkout_session id: ", checkout_session.id)

            ACH_info = json.dumps({"id": checkout_session.id, "url": checkout_session.url})
            print("ACH INFO: ", ACH_info)

            # add entry to PAYMENTS table and Update PURCHASES table
            # Could MakePayment work?
        except Exception as e:
            return str(e)

        # return redirect(checkout_session.url, code=303)
        # return Response(checkout_session.url, status=201, mimetype="application/json")
        return Response(ACH_info, status=201, mimetype="application/json")
        # return jsonify({
        # "id": checkout_session.id,
        # "url": checkout_session.url
        # }), 201
    
        # return jsonify({"id": checkout_session.id, "url": checkout_session.url}), 201
        # return Response(jsonify({"id": checkout_session.id, "url": checkout_session.url}), status=201, mimetype="application/json")






# Retrieve Stripe Info - STRIPE Utilities
class retrieveStripeCharge(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("\ndata: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        # print("customer: ", customer_uid)
        # print("business: ", businessId)
        # print("amount: ", charge_amount)

        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        # print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
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
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        # print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
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
        refund_amount = data["refund_amount"] * 100      #refund amount must be multipled by 100 to convert it into cents
        charge_id = data["charge_id"]                    #charge ID comes from Stripe > Payments > select Successful Payment > scroll down to Connections
        # charge_amount = int(round(float(data["payment_summary"]["total"]) * 100))
        print("customer: ", customer_uid)
        print("business: ", businessId)
        # print("amount: ", charge_amount)

        print("\nIn Step 1")
        keys = getCorrectKeys.post(self, businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        # print("stripe SECRET_KEY: ", keys["SECRET_KEY"])
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
api.add_resource(stripeKey, "/api/v2/stripe_key/<string:businessId>")
api.add_resource(createNewCustomer, "/api/v2/createNewCustomer/<string:customer_uid>")
api.add_resource(createCustomerOnly, "/api/v2/createCustomerOnly")
api.add_resource(createPaymentIntent, "/api/v2/createPaymentIntent")
api.add_resource(retrieveStripeCharge, "/api/v2/retrieveStripeCharge")
api.add_resource(retrieveLast4, "/api/v2/retrieveLast4")

api.add_resource(createOffSessionPaymentIntent, "/api/v2/createOffSessionPaymentIntent")
api.add_resource(refund, "/api/v2/refund")
api.add_resource(customerList, "/api/v2/customerList/<string:businessId>")

# Removed SendEmail endpoint for security - now using static method internally
# api.add_resource(SendEmail, "/api/v2/sendEmail/<string:message>,<string:data>")

api.add_resource(createACHPaymentIntent, "/api/v2/createACHPaymentIntent")
api.add_resource(createEasyACHPaymentIntent, "/api/v2/createEasyACHPaymentIntent")

api.add_resource(retrieve, "/api/v2/retrieve")
api.add_resource(status, "/api/v2/status")
api.add_resource(webhook, "/api/v2/webhook")


if __name__ == "__main__":
    # app.run()
    app.run(host="127.0.0.1", port=2000)