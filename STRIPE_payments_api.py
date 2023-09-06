
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

from getKey import getCorrectKeys
from getCustomer import createCustomerOnly, createNewCustomer
from ACH_payments import createACHPaymentIntent
from ACH_payments import verifyACH, retrieve, status, webhook



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
        print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])


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


