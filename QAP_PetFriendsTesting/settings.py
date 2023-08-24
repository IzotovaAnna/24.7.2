import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

unvalid_email = os.getenv('unvalid_email')
unvalid_password = os.getenv('unvalid_password')

invalid_auth_key = {'key': '555c0c8710fd04e2f53c3637407c7b1080e9f40be53e41a84dc94637'}