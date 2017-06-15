import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

########

import email
import imaplib

#
IMAP_SERVER = 'imap.gmail.com'
MAILBOX  = 'inbox'
QUANTITY = 15
CRITERIA = 'ALL'
MESSAGE_PARTS = '(RFC822)'

def read_mailbox(account, password):

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(account, password)
    mail.select(MAILBOX)

    typ, data = mail.search(None, CRITERIA)
    ids = data[0]

    id_list = ids.split()

    latest_email_id = int(id_list[-1])

    result = []

    for i in range(latest_email_id, latest_email_id - QUANTITY, -1):

        typ, data = mail.fetch(i, MESSAGE_PARTS)

        subject = ''
        sender = ''

        for response_part in data:

            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                subject = msg['subject']
                sender = msg['from']

        # add ellipsis (...) if subject length is greater than 35 characters
        if len(subject) > 35:
            subject = '%s...' % subject[0:32]

        result.append(dict(sender=sender, subject=subject))

    return result