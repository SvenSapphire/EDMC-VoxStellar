import time
import requests
import json
import hashlib
import hmac

from voxstellar.debug import Debug
from voxstellar.config import Config


class ApplicationSender:
    def __init__(self, voxstellar):
        self.voxstellar = voxstellar

    def send(self, cmdr, payload):
        url = Config(self.voxstellar).api('voxstellar')['url']
        key = Config(self.voxstellar).api('voxstellar')['key']
        version = Config(self.voxstellar).api('voxstellar')['version']

        json_data = json.dumps({
            'commander': cmdr,
            'data': payload
        })

        signature = hmac.new(key.encode('utf-8'), json_data.encode('utf-8'), hashlib.sha256)
        signature_hex = signature.hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'Signature': f'{signature_hex}',
            'Connection': 'close',
            'User-Agent': f'EDMC-VoxStellar/{version}',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        Debug.logger.debug(f"Sending data to {url}...")

        start_time = time.time()
        response = requests.post(url, data=json_data, headers=headers)
        end_time = time.time()

        Debug.logger.debug(f"Sending data took {end_time - start_time} seconds.")

        if response.status_code == 200:
            Debug.logger.debug("Webhook sent successfully.")
        else:
            Debug.logger.debug(f"Webhook failed with status code: {response.status_code}")
