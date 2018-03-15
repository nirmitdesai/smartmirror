# Copyright (c) 2016 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Initializes an UberRidesClient with OAuth 2.0 Credentials.

This example demonstrates how to get an access token through the
OAuth 2.0 Authorization Code Grant and use credentials to create
an UberRidesClient.

To run this example:

    (1) Set your app credentials in config.yaml
    (2) Run `python authorization_code_grant.py`
    (3) A success message will print, 'Hello {YOUR_NAME}'
    (4) User OAuth 2.0 credentials are recorded in
        'oauth2_session_store.yaml'
"""



from builtins import input

import json

from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.client import UberRidesClient
from uber_rides.errors import ClientError
from uber_rides.errors import ServerError
from uber_rides.errors import UberIllegalState
from uber_rides.client import UberRidesClient
from uber_rides.session import OAuth2Credential
from uber_rides.session import Session

def authorization_code_grant_flow(credentials, storage_filename):
    """Get an access token through Authorization Code Grant.

    Parameters
        credentials (dict)
            All your app credentials and information
            imported from the configuration file.
        storage_filename (str)
            Filename to store OAuth 2.0 Credentials.

    Returns
        (UberRidesClient)
            An UberRidesClient with OAuth 2.0 Credentials.
    """
    print credentials.get('scopes')
    auth_flow = AuthorizationCodeGrant(
        credentials.get('client_id'),
        credentials.get('scopes'),
        credentials.get('client_secret'),
        credentials.get('redirect_url'),
    )

    auth_url = auth_flow.get_authorization_url()
    login_message = 'Login and grant access by going to:\n{}\n'
    login_message = login_message.format(auth_url)
    print(login_message)

    redirect_url = 'Copy the URL you are redirected to and paste here: \n'
    result = input(redirect_url).strip()

    try:
        session = auth_flow.get_session(result)

    except (ClientError, UberIllegalState) as error:
        print "failed........"
        print(error)
        return

    credential = session.oauth2credential

    credential_data = {
        'client_id': credential.client_id,
        'redirect_url': credential.redirect_url,
        'access_token': credential.access_token,
        'expires_in_seconds': credential.expires_in_seconds,
        'scopes': list(credential.scopes),
        'grant_type': credential.grant_type,
        'client_secret': credential.client_secret,
        'refresh_token': credential.refresh_token,
    }

    with open(storage_filename, 'w') as fp:
        print "dumped to file!"
        json.dump(credential_data,fp)

    return UberRidesClient(session, sandbox_mode=True)


def hello_user(api_client):
    """Use an authorized client to fetch and print profile information.

    Parameters
        api_client (UberRidesClient)
            An UberRidesClient with OAuth 2.0 credentials.
    """

    try:
        response = api_client.get_user_profile()

    except (ClientError, ServerError) as error:
        fail_print(error)
        return

    else:
        profile = response.json
        first_name = profile.get('first_name')
        last_name = profile.get('last_name')
        email = profile.get('email')
        message = 'Hello, {} {}. Successfully granted access token to {}.'
        message = message.format(first_name, last_name, email)
        print(message)

        response = api_client.get_products(37.402635, -121.950597)
        products = response.json.get('products')
        for p in products:
            if 'POOL' in p.get('display_name'):
                product_id = p.get('product_id')
                break

        print "/"*50
        print p.get('display_name')
        # Get upfront fare for product with start/end location
        estimate = api_client.estimate_ride(
            start_latitude=37.402635,
            start_longitude=-121.950597,
            end_latitude=37.397604,
            end_longitude=-122.139623,
            seat_count=1,
            product_id = product_id
        )
        fare = estimate.json.get('fare')
        print(fare)

        response = api_client.request_ride(
        product_id=product_id,
        start_latitude=37.402635,
            start_longitude=-121.950597,
            end_latitude=37.397604,
            end_longitude=-122.139623,
            seat_count=1,
        fare_id=fare['fare_id']
    )

        request = response.json
        request_id = request.get('request_id')

        # Request ride details from request_id
        response = api_client.get_ride_details(request_id)
        ride = response.json

        # Cancel a ride
        response = api_client.cancel_ride(request_id)
        ride = response.json
        print "*"*50

def getUberClient(credentials):
    oauth2credential = OAuth2Credential(
        client_id=credentials.get('client_id'),
        access_token=credentials.get('access_token'),
        expires_in_seconds=credentials.get('expires_in_seconds'),
        scopes=credentials.get('scopes'),
        grant_type=credentials.get('grant_type'),
        redirect_url=credentials.get('redirect_url'),
        client_secret=credentials.get('client_secret'),
        refresh_token=credentials.get('refresh_token'),
    )
    session = Session(oauth2credential=oauth2credential)
    return UberRidesClient(session)

if __name__ == '__main__':
    """Run the example.

    Get an access token through the OAuth 2.0 Authorization Code Grant
    and use credentials to create an UberRidesClient.
    """
    credentials = {
        'client_id': '',
        "access_token": ".",
        'grant_type' : 'client_credentials',
        'client_secret': '__',
        'redirect_url': 'https://.ngrok.io',
        "refresh_token": "",
        "scopes": "places profile request",
        "token_type": "Bearer",
        "expires_in_seconds": 2592000,
        "last_authenticated": 0

    }

    # api_client = authorization_code_grant_flow(
    #     credentials,
    #     'uberInfo.json',
    # )

    api_client = getUberClient(credentials)
    hello_user(api_client)
