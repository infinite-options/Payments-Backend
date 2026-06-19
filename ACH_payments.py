import stripe
import json
import os
import requests

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS

from getKey import getCorrectKeys


# NOT IN USE
class verifyACH(Resource):
    def post(self):
        data = request.get_json(force=True)
        stripe.api_key = os.environ.get("ACH_STRIPE_TEST_SECRET_KEY")
        customer_Uid = data["customer_uid"]
        pay_method = data["payment_method"]
        payment_intent_id = data["payment_intent_id"]
        stripe.api_version = None
        stripe.PaymentMethod.attach(
            pay_method,
            customer= customer_Uid,
        )
        stripe.PaymentIntent.confirm(payment_intent_id, payment_method = pay_method,setup_future_usage="off_session", mandate_data = "")


class retrieve(Resource):
        def post(self):

            data = request.get_json(force=True)
            print("data: ", data)
            customer_uid = data["customer_uid"]
            businessId = data["business_code"]
            payment_intent = data["payment_intent"]
            print("customer: ", customer_uid)
            print("business: ", businessId)
            print("payment intent: ", payment_intent)

            print("\nIn Step 1")
            keys = getCorrectKeys().get_keys(businessId)
            # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
            stripe.api_key = keys["SECRET_KEY"]
            stripe.api_version = None

            res = stripe.PaymentIntent.retrieve(payment_intent,)

            return res

class status(Resource):
    def post(self):

        data = request.get_json(force=True)
        print("data: ", data)
        customer_uid = data["customer_uid"]
        businessId = data["business_code"]
        payment_intent = data["payment_intent"]
        print("customer: ", customer_uid)
        print("business: ", businessId)
        print("payment intent: ", payment_intent)

        print("\nIn Step 1")
        keys = getCorrectKeys().get_keys(businessId)
        # print("stripe PUBLISHABLE_KEY: ", keys["PUBLISHABLE_KEY"])
        stripe.api_key = keys["SECRET_KEY"]
        stripe.api_version = None

        res = stripe.PaymentIntent.retrieve(payment_intent,)

        result = res["status"]

        return result

class webhook(Resource):
    def post(self):
        event = None
        stripe.api_key = os.environ.get("ACH_STRIPE_TEST_SECRET_KEY")
        endpoint_secret = os.environ.get("ACH_STRIPE_WEBHOOK_SECRET")
        data = request.data
        sig_header = request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                data, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid data
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        # Handle the event
        if event['type'] == 'payment_intent.created':
            payment_intent = event['data']['object']
        elif event['type'] == 'payment_intent.processing':
            payment_intent = event['data']['object']
        elif event['type'] == 'payment_intent.requires_action':
            payment_intent = event['data']['object']
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event['type']))

        return jsonify(success=True)

#Get Status of payment Endpoint