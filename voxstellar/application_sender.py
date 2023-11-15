import requests
import json
import hashlib
import hmac

from voxstellar.debug import Debug
from voxstellar.config import Config

SECRET_KEY = 'sexy69'


class ApplicationSender:
    def __init__(self, voxstellar):
        self.voxstellar = voxstellar

    def send(self, cmdr, payload):

        url = Config(self.voxstellar).api('voxstellar')['url']
        key = Config(self.voxstellar).api('voxstellar')['key']

        json_data = json.dumps({
            'commander': cmdr,
            'data': payload
        })

        signature = hmac.new(key.encode('utf-8'), json_data.encode('utf-8'), hashlib.sha256)
        signature_hex = signature.hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'Signature': f'{signature_hex}'
        }
        response = requests.post(url, data=json_data, headers=headers)

        # TODO: finish response
        if response.status_code == 200:
            Debug.logger.debug("Webhook sent successfully.")
        else:
            Debug.logger.debug(f"Webhook failed with status code: {response.status_code}")
