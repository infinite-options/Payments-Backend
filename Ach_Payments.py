import stripe
import json
import os
import requests

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS

class createACHPaymentIntent(Resource):
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
        elif businessId == "ACH":
            PUBLISHABLE_KEY = "pk_test_51NkKHkFXblfqA49hJnh8bdxgRzvhtaACstCkJQIO4Sq4szBeomcdKTCh4tsMbuc8SiATjA8IPqcwkvnLENclDZJX00TsjxpFYU"
            SECRET_KEY = "sk_test_51NkKHkFXblfqA49hU9dmIuuuGAzNxnFusrLHWxwrQRxXLSJP0p0RGmL4SIhSltKqLOcRf81sV6z54HRIRQi8tO7r006CE4Tevp"
        else:
            print("In Else Statment")
            PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
            SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"

        if PUBLISHABLE_KEY == None:
            print("PUBLISHABLE_KEY == None")
            PUBLISHABLE_KEY = "pk_test_51IhynWGQZnKn7zmSUdovQOXLCxhKlTh2HvcosWHC9DRXYMMGHZTa510D16bXziGlgWsjY8jF5vKUn5W5s78kSoOu00wa0SR2JG"
            SECRET_KEY = "sk_test_51IhynWGQZnKn7zmSUZDTXIaOoxawY7QO0FeLhOdSxFs5wCi1wjzS09u2vD20Yl5TiZ4rqQulzvbJGsw1lRtvoxG600NxkSdgGx"

        print("PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
        # print("SECRET_KEY: ", SECRET_KEY)
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
        # print("stripe sk: ", stripe.api_key)

        # paras = {
        #     "item_uid": "320-000050",
        #     "num_issues": "2",
        #     "customer_uid": "100-000125",
        #     "tip": "2",
        #     "ambassador": "",
        # }
        # params = {
        #     "item_uid": data["item_uid"],
        #     "num_issues": data["num_deliveries"],
        #     "customer_uid": data["customer_uid"],
        #     "tip": data["payment_summary"]["tip"],
        #     "ambassador": "",
        # }
        # print("params: ", params)
        # print(params["item_uid"])
        # print(params.json())
        # print(params.item_uid)

        print("In IF Block")
        print(businessId)
        if businessId == "M4ME" or businessId == "M4METEST":
            response = requests.post(
                url="https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/order_amount_calculation",
                #json=params,
            )
            print("total amount is: ", response.json())
            total_amount = float(response.json())
        elif businessId == "SF" or businessId == "SFTEST":
            response = requests.post(
                url="https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/order_amount_calculation",
                #json=params,
            )
            print("total amount is: ", response.json())
            total_amount = float(response.json())
        elif businessId == "IOPAYMENT" or businessId == "IOTEST":
            response = "1017"
            print("total amount is: ", response)
            total_amount = float(response)

        else:
            response = "1023"
            print("total amount is: ", response)
            total_amount = float(response)

        # response = "2100"
        # response = 2100
        # response = {"": "2100"}

        # response = requests.post(
        #     url="https://ht56vci4v9.execute-api.us-west-1.amazonaws.com/dev/api/v2/order_amount_calculation",
        #     json=params,
        # )
        # print("total amount is: ", response.json())
        # total_amount = float(response.json())

        # data = request.get_json(force=True)
        # print("data: ", data)
        # intent = stripe.PaymentIntent.create(
        #     # amount=int(float(data["payment_summary"]["total"]) * 100),
        #     amount=int(total_amount * 100),
        #     # amount=1099,
        #     # currency="usd",
        #     currency=data["currency"],
        #     # Verify your integration in this guide by including this parameter
        #     # metadata={'integration_check': 'accept_a_payment'},
        #     # customer="cus_JKUnLFjlbjW2PG",
        #     customer=data["customer_uid"],
        #     # customer='{{CUSTOMER_ID}}',
        #     # payment_method="pm_1IhpoELMju5RPMEvq6B92VsG",
        #     # payment_method='{{PAYMENT_METHOD_ID}}',
        #     # off_session=True,
        #     # confirm=True,
        # )
        # print("intent: ", intent)
        intent = stripe.PaymentIntent.create(
            amount=1099,
            currency="usd",
            setup_future_usage="off_session",
            customer= customerUid,
            payment_method_types=["us_bank_account"],
            payment_method_options={
                "us_bank_account": {
                    "financial_connections": {"permissions": ["payment_method", "balances"]},
                },
            },
        )
        client_secret = intent.client_secret
        # return {"secret": client_secret}
        return client_secret


