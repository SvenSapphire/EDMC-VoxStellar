import logging

import requests
import json
import hashlib
import hmac
from voxstellar.config import Config


class ApplicationSender:
    def __init__(self, voxstellar):
        self.voxstellar = voxstellar

        requests.packages.urllib3.util.connection.HAS_IPV6 = False

        self.requests_log = logging.getLogger("urllib3")
        self.requests_log.setLevel(logging.DEBUG)
        fh = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.requests_log.addHandler(fh)
        self.requests_log.propagate = False

        ## normal logger -------------------------------------------------------------------------------
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('application_sender.log')
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

    def send(self, cmdr, payload):
        url = Config(self.voxstellar).api('voxstellar')['url']
        key = Config(self.voxstellar).api('voxstellar')['key']
        version = Config(self.voxstellar).api('voxstellar')['version']

        json_data = json.dumps({
            'commander': cmdr,
            'data': payload
        })

        signature = hmac.new(key.encode('utf-8'), json_data.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'Signature': f'{signature}',
            'Connection': 'close',
            'User-Agent': f'EDMC-VoxStellar/{version}',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        self.logger.debug("-------------------------------- START REQUEST --------------------------------")
        response = requests.post(url, data=json_data, headers=headers)

        self.logger.debug("-------------------------------- RESOURCES USED --------------------------------")
        request = response.request
        self.logger.debug(f"Request URL: {request.url}")
        self.logger.debug(f"Request Method: {request.method}")
        self.logger.debug(f"Request Headers: {request.headers}")
        self.logger.debug(f"Request Body: {request.body}")
        self.logger.debug("-------------------------------- END REQUEST SECTION --------------------------------")

        if response.status_code == 200:
            self.logger.debug("Webhook sent successfully.")
        else:
            self.logger.debug(f"Webhook failed with status code: {response.status_code}")

        self.logger.debug(f"Response url: {response.url}")
        self.logger.debug(f"Response content: {response.content}")
        self.logger.debug(f"Response headers: {response.headers}")
        self.logger.debug(f"Response reason: {response.reason}")
        self.logger.debug(f"Response status code: {response.status_code}")
        self.logger.debug(f"Response elapsed time: {response.elapsed}")
        self.logger.debug(f"Response encoding: {response.encoding}")
        self.logger.debug("-------------------------------- END RESPONSE SECTION --------------------------------")
