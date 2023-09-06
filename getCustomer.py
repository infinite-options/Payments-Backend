
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
        last4 = "No Key"

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