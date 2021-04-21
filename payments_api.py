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

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv


# Setup Stripe python client library
load_dotenv(find_dotenv())
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = os.getenv("STRIPE_API_VERSION")

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
# use below for local testing

# IO Keys
# PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
# SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"
# stripe.api_key = SECRET_KEY
# stripe.api_version = None

# static_dir = str(os.path.abspath(os.path.join(__file__, "..", os.getenv("STATIC_DIR"))))
# app = Flask(
#     __name__, static_folder=static_dir, static_url_path="", template_folder=static_dir
# )
app = Flask(__name__)
# cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
CORS(app)

# API
api = Api(app)

# STRATEGY: Create an Endpoint that bring is the business code and returns the proper keys
# USE a try block to try from website but if not use the default test keys

# STEP 1: Setup Stripe
# Get the correct Keys


class getCorrectKeys(Resource):
    def post(self):
        # Customer UID sent in from frontend
        print("Step 1: Get Correct Keys")
        data = request.get_json(force=True)
        print("data: ", data)
        businessId = data["business_code"]
        print("business: ", businessId)

        print("In Try Block")
        if businessId == "M4ME":
            PUBLISHABLE_KEY = "M4ME_STRIPE_LIVE_PUBLISHABLE_KEY"
            SECRET_KEY = "M4ME_STRIPE_LIVE_SECRET_KEY"
        elif businessId == "M4METEST":
            PUBLISHABLE_KEY = "M4ME_STRIPE_TEST_PUBLISHABLE_KEY"
            SECRET_KEY = "M4ME_STRIPE_TEST_SECRET_KEY"
        elif businessId == "SF":
            PUBLISHABLE_KEY = "SN_STRIPE_LIVE_PUBLISHABLE_KEY"
            SECRET_KEY = "SN_STRIPE_LIVE_SECRET_KEY"
        elif businessId == "SFTEST":
            PUBLISHABLE_KEY = "SN_STRIPE_TEST_PUBLISHABLE_KEY"
            SECRET_KEY = "SN_STRIPE_LIVE_SECRET_KEY"
        elif businessId == "IOPAYMENT":
            PUBLISHABLE_KEY = "IOPAYMENTS_STRIPE_LIVE_PUBLISHABLE_KEY"
            SECRET_KEY = "IOPAYMENTS_STRIPE_LIVE_SECRET_KEY"
        elif businessId == "IOTEST":
            PUBLISHABLE_KEY = "IOPAYMENTS_STRIPE_TEST_PUBLISHABLE_KEY"
            SECRET_KEY = "IOPAYMENTS_STRIPE_TEST_SECRET_KEY"
        else:
            PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
            SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"

        print("PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
        print("SECRET_KEY: ", SECRET_KEY)
        stripe.api_key = SECRET_KEY
        stripe.api_version = None

        return PUBLISHABLE_KEY


# STEP 2: Create a Customer
class createCustomerOnly(Resource):
    def get(self):

        # Create Payment Intent
        # Create customer.  Need this step to save CC info
        customer = stripe.Customer.create()
        print("customer: ", customer)
        customerId = customer.id
        print("customer ID: ", customerId)

        return customerId


class createNewCustomer(Resource):
    def post(self):
        # Customer UID sent in from frontend
        print("Step 2")
        data = request.get_json(force=True)
        print("data: ", data)
        customerUid = data["customer_uid"]
        print("customer: ", customerUid)

        # Check if Stripe does NOT already have the Customer UID
        try:
            # IF Stripe has the UID then it cannot create another customer with same UID THEN try will fail
            # IF it does NOT have the UID then it will create the customer
            customer = stripe.Customer.create(id=data["customer_uid"])
            print("New Customer ID created!")
            newCustomer = True
        except:
            # IF Stripe has the UID, it will retrieve the info and print it
            print("Found Customer ID!")
            stripe.Customer.retrieve(data["customer_uid"])
            # stripe.Customer.retrieve("cus_JKUnLFjlbjW2PG")
            print("Customer Info: ", stripe.Customer.retrieve(data["customer_uid"]))
            newCustomer = False

        return newCustomer


# STEP 3: Create a Payment Intent
class createPaymentIntentOnly(Resource):
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

    def post(self):

        # Create Payment Intent with Customer ID
        print("Step 3")
        print("stripe sk: ", stripe.api_key)
        data = request.get_json(force=True)
        print("data: ", data)
        intent = stripe.PaymentIntent.create(
            amount=1099,
            currency="usd",
            # Verify your integration in this guide by including this parameter
            # metadata={'integration_check': 'accept_a_payment'},
            # customer="cus_JKUnLFjlbjW2PG",
            customer=data["customer_uid"],
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


# Step 1, 2 ,3 Combined
class createPaymentIntent(Resource):
    def post(self):
        # Step 1
        # Customer UID sent in from frontend
        print("Step 1: Get Correct Keys")
        data = request.get_json(force=True)
        print("data: ", data)
        businessId = data["business_code"]
        print("business: ", businessId)

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

        # return PUBLISHABLE_KEY

        # STEP 2
        # Customer UID sent in from frontend
        print("Step 2")
        # data = request.get_json(force=True)
        # print("data: ", data)
        customerUid = data["customer_uid"]
        print("customer: ", customerUid)

        # Check if Stripe does NOT already have the Customer UID
        try:
            # IF Stripe has the UID then it cannot create another customer with same UID THEN try will fail
            # IF it does NOT have the UID then it will create the customer
            customer = stripe.Customer.create(id=data["customer_uid"])
            print("New Customer ID created!")
            newCustomer = True
        except:
            # IF Stripe has the UID, it will retrieve the info and print it
            print("Found Customer ID!")
            stripe.Customer.retrieve(data["customer_uid"])
            # stripe.Customer.retrieve("cus_JKUnLFjlbjW2PG")
            print("Customer Info: ", stripe.Customer.retrieve(data["customer_uid"]))
            newCustomer = False

        # return newCustomer

        # Step 3
        # Create Payment Intent with Customer ID
        print("Step 3")
        print("stripe sk: ", stripe.api_key)

        paras = {
            "item_uid": "320-000050",
            "num_issues": "2",
            "customer_uid": "100-000125",
            "tip": "2",
            "ambassador": "",
        }
        params = {
            "item_uid": data["item_uid"],
            "num_issues": data["num_deliveries"],
            "customer_uid": data["customer_uid"],
            "tip": data["payment_summary"]["tip"],
            "ambassador": "",
        }
        response = requests.post(
            url="https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/order_amount_calculation",
            json=params,
        )
        print("total amount is: ", response.json())
        total_amount = float(response.json())

        # data = request.get_json(force=True)
        # print("data: ", data)
        intent = stripe.PaymentIntent.create(
            # amount=int(float(data["payment_summary"]["total"]) * 100),
            amount=int(total_amount * 100),
            # amount=1099,
            # currency="usd",
            currency=data["currency"],
            # Verify your integration in this guide by including this parameter
            # metadata={'integration_check': 'accept_a_payment'},
            # customer="cus_JKUnLFjlbjW2PG",
            customer=data["customer_uid"],
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


# Step 4: Payment method with card and billing details entirely on the Front End

# Step 5: Submit Payment to Stripe is handled entirely on the Front End


# Step 6: Submit Off Session payment to Strip
class createOffSessionPaymentIntent(Resource):
    def post(self):

        # Create Payment Intent with Customer ID
        print("stripe sk: ", stripe.api_key)
        data = request.get_json(force=True)
        print("data: ", data)
        intent = stripe.PaymentIntent.create(
            amount=1099,
            currency="usd",
            # Verify your integration in this guide by including this parameter
            # metadata={'integration_check': 'accept_a_payment'},
            # customer="cus_JKUnLFjlbjW2PG",
            customer=data["customer_uid"],
            # customer='{{CUSTOMER_ID}}',
            # payment_method=data["payment_method"],
            payment_method=stripe.PaymentMethod.list(
                customer=data["customer_uid"],
                type="card",
            )
            .data[0]
            .id,
            # payment_method='{{PAYMENT_METHOD_ID}}',
            off_session=True,
            confirm=True,
        )
        print("intent: ", intent)
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return client_secret


class customerPaymentMethodList(Resource):
    def post(self):

        # Create Payment Intent with Customer ID
        print("stripe sk: ", stripe.api_key)
        data = request.get_json(force=True)
        print("data: ", data)
        list = stripe.PaymentMethod.list(
            customer=data["customer_uid"],
            type="card",
        )
        # print("Payment Method List: ", list)
        print("Payment Method: ", list.data[0].id)
        return list.data[0].id


# class template_name(Resource):
#     def get(self, variables):

#         try:


#             response['message'] = "A temporary password has been sent"
#             return response, 200
#         except:
#             raise BadRequest('Request failed, please try again later.')
#         finally:
#             disconnect(conn)


# ------- ORIGINAL CODE --------
@app.route("/checkout", methods=["GET"])
def get_checkout_page():
    # Display checkout page
    return render_template("index.html")


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@app.route("/create-payment-intent", methods=["POST"])
def create_payment():
    data = json.loads(request.data)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(data["items"]), currency=data["currency"]
    )

    try:
        # Send publishable key and PaymentIntent details to client
        return jsonify(
            {
                "publishableKey": os.getenv("STRIPE_PUBLISHABLE_KEY"),
                "clientSecret": intent.client_secret,
            }
        )
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/webhook", methods=["POST"])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret
            )
            data = event["data"]
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event["type"]
    else:
        data = request_data["data"]
        event_type = request_data["type"]
    data_object = data["object"]

    if event_type == "payment_intent.succeeded":
        print("💰 Payment received!")
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == "payment_intent.payment_failed":
        print("❌ Payment failed.")
    return jsonify({"status": "success"})


# ------- END ORIGINAL CODE --------


# Define API routes
# NEW BASE URL:  https://huo8rhh76i.execute-api.us-west-1.amazonaws.com/dev/

api.add_resource(getCorrectKeys, "/api/v2/getCorrectKeys")
api.add_resource(createPaymentIntentOnly, "/api/v2/createPaymentIntentOnly")
api.add_resource(createPaymentIntent, "/api/v2/createPaymentIntent")
api.add_resource(createCustomerOnly, "/api/v2/createCustomerOnly")
api.add_resource(createNewCustomer, "/api/v2/createNewCustomer")
api.add_resource(createOffSessionPaymentIntent, "/api/v2/createOffSessionPaymentIntent")
api.add_resource(customerPaymentMethodList, "/api/v2/customerPaymentMethodList")

if __name__ == "__main__":
    # app.run()
    app.run(host="127.0.0.1", port=2000)
