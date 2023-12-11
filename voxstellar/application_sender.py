import time
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

        Debug.logger.debug("------------------------ HIT ------------------------")

        signature = hmac.new(key.encode('utf-8'), json_data.encode('utf-8'), hashlib.sha256)
        signature_hex = signature.hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'Signature': f'{signature_hex}'
        }

        Debug.logger.debug("------------------------ HIT AFTER ENCRYPTION ------------------------")

        Debug.logger.debug(json_data)
        Debug.logger.debug(f'{signature_hex}')

        # measure the time how long this will take
        start = time.time()
        response = requests.post(url, data=json_data, headers=headers)
        end = time.time()

        if response.status_code == 200:
            Debug.logger.debug("Webhook sent successfully.")
            Debug.logger.debug(f"Webhook took {end - start} seconds to complete.")
        else:
            Debug.logger.debug(f"Webhook failed with status code: {response.status_code}")
