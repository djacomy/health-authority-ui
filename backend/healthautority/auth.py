import json
from urllib.parse import urlencode

import os
import requests

from oic import rndstr
from oic.oauth2 import AuthorizationResponse
from oic.oic import Client
from oic.utils.authn.client import ClientSecretBasic, ClientSecretPost

from flask import *

import config


class AuthMachineClient(object):
    def __init__(self):
        self.client = self.get_client()
        if request.is_secure:
            proto = 'https://'
        else:
            proto = 'http://'
        self.host = proto + request.host
        print(self.host)

    def get_client(self):
        client = Client(client_authn_method={
            'client_secret_post': ClientSecretPost,
            'client_secret_basic': ClientSecretBasic
        })
        print(client.provider_config)
        client.provider_config(config.AUTHMACHINE_URL)
        client.client_id = config.AUTHMACHINE_CLIENT_ID
        client.client_secret = config.AUTHMACHINE_CLIENT_SECRET
        client.verify_ssl = True
        return client

    def get_authorization_url(self):
        nonce = rndstr()

        args = {
            'client_id': self.client.client_id,
            'response_type': 'code',
            'scope': config.AUTHMACHINE_SCOPE,
            'claims': json.dumps({}),
            'nonce': nonce,
            'redirect_uri': self.host + url_for('auth.auth_callback'),
            'state': 'some-state-which-will-be-returned-unmodified'
        }
        url = self.client.provider_info['authorization_endpoint'] + '?' + urlencode(args, True)
        return url

    def get_access_token(self, aresp):
        """Gets access token from AuthMachine.
        Args:
            aresp (AuthorizationResponse):
        """
        args = {
            'code': aresp['code'],
            'client_id': self.client.client_id,
            'client_secret': self.client.client_secret,
            'redirect_uri': self.host + url_for('auth.auth_callback')
        }

        return self.client.do_access_token_request(
            scope=config.AUTHMACHINE_SCOPE,
            state=aresp['state'],
            request_args=args,
            authn_method='client_secret_post')

    def get_userinfo(self, authorization_response):
        """Returns Open ID userinfo as dict.
        """

        self.get_access_token(authorization_response)
        user_info = self.client.do_user_info_request(
            state=authorization_response['state'],
            authn_method='client_secret_post')
        return user_info.to_dict()

    def get_authorization_response(self):
        authorization_response = self.client.parse_response(
            AuthorizationResponse,
            info=request.args,
            sformat='dict')
        return authorization_response

    def do_api_request(self, method, url, payload=None, query_params=None, **kwargs):
        assert config.AUTHMACHINE_API_TOKEN is not None, "Can't perform an API Request: API Token not specified"
        absolute_url = os.path.join(config.AUTHMACHINE_URL, url)

        if payload:
            kwargs['data'] = json.dumps(payload, sort_keys=True)

        if query_params:
            absolute_url += '?' + urlencode(query_params, doseq=True)

        headers = kwargs.pop('headers', {})
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Token %s' % config.AUTHMACHINE_API_TOKEN
        response = requests.request(method=method, url=absolute_url, headers=headers, **kwargs)

        return response
