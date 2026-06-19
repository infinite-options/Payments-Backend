
import stripe
import json
import os
import requests
import datetime

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mail import Mail, Message
from email import message


def _obscure_key(key):
    if not key:
        return key
    if len(key) <= 8:
        return "****"
    return f"{key[:12]}****{key[-4:]}"


# STEP 1: Setup Stripe
# Get the correct Keys
class getCorrectKeys(Resource):
    def __call__(self):
        print("In Call")

    def get_keys(self, businessId):
        return self._load_keys(businessId)

    def post(self, businessId):
        keys = self._load_keys(businessId)
        return {
            "PUBLISHABLE_KEY": keys["PUBLISHABLE_KEY"],
            "SECRET_KEY": _obscure_key(keys["SECRET_KEY"]),
        }

    def _load_keys(self, businessId):
        # Business Code sent in as a parameter from frontend
        print("Step 1: Get Correct Keys")
        print("business: ", businessId)

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
        elif businessId == "EC":
            PUBLISHABLE_KEY = os.environ.get("PM_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("PM_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "ECTEST":
            PUBLISHABLE_KEY = os.environ.get("PM_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("PM_STRIPE_TEST_SECRET_KEY")
        elif businessId == "IOPAYMENT":
            PUBLISHABLE_KEY = os.environ.get("IOPAYMENTS_STRIPE_LIVE_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("IOPAYMENTS_STRIPE_LIVE_SECRET_KEY")
        elif businessId == "IOTEST":
            PUBLISHABLE_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_SECRET_KEY")
        elif businessId == "ACH":
            PUBLISHABLE_KEY = os.environ.get("ACH_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("ACH_STRIPE_TEST_SECRET_KEY")
        else:
            PUBLISHABLE_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_PUBLISHABLE_KEY")
            SECRET_KEY = os.environ.get("IOPAYMENTS_STRIPE_TEST_SECRET_KEY")


        # print("PUBLISHABLE_KEY: ", PUBLISHABLE_KEY)
        # print("SECRET_KEY: ", SECRET_KEY)
        stripe.api_key = SECRET_KEY
        stripe.api_version = None

        return {"PUBLISHABLE_KEY": PUBLISHABLE_KEY, "SECRET_KEY": SECRET_KEY}


class stripeKey(Resource):
    def get(self, businessId):
        keys = getCorrectKeys().get_keys(businessId)
        return {"publicKey": keys["PUBLISHABLE_KEY"]}