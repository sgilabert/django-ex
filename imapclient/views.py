from django.shortcuts import render
from . import utilities
from . import safewalk

import logging

logger = logging.getLogger(__name__)

def read_secrets():

    # Request the secrets to Safewalk
    # -------------------------------
    service_url  = 'https://swk-integration.ddns.net:8443/'
    access_token = 'abc123'

    #client = safewalk.SafewalkClient(service_url, access_token)
    #secrets = client.get_secrets()

    identifier = '78463'
    key = '1919cf5936ad193c04b3460fb3845e9d9846d8c7'

    # Dummy
    secrets = dict(key=key, identifier=identifier, result='SUCCESS')

    if secrets is not None and secrets['result'] == 'SUCCESS':

        key        = secrets['key']
        identifier = secrets['identifier']

        # Read the secrets
        # ----------------
        # TODO : Read the secrets
        encrypted_account  = 'hbroiA5nFfhg5d3O8B1/BadhQ1/HkJOZIj0eFS3AiDuKW3o9FxPm4no22XjasGMX'
        encrypted_password = 'DHFRTHr3UeSTftF00jPma7tx/DemFPBR67dkBADi27pwREAc+ShwKIDcQHF+SreioGKZvPA6QJrPsuWviyc0d7F990mhCTK+0UQj5DfwjRQ='
        #
        cipher = utilities.AESCipher(key)
        decrypted_account  = cipher.decrypt(encrypted_account)
        decrypted_password = cipher.decrypt(encrypted_password)

        print 'Decrypted account is \'%s\'' % decrypted_account
        print 'Decrypted password is \'%s\'' % decrypted_password

        return dict(
            account  = decrypted_account,
            password = decrypted_password
        )

    return None



def index(request):

    secrets = read_secrets()

    return render(request, 'imapclient/index.html', {
        'account': secrets.get('account', '<undefined>'),
        'mails' : utilities.read_mailbox(secrets.get('account'), secrets.get('password'))
    })
