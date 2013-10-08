# -*- coding: utf-8 -*-
# Настройки
#

import imaplib

email = {
    'username': '',
    'password': '',
    'hostname': ''
    }

def open_connection(verbose=False):
    connection = imaplib.IMAP4_SSL(email['hostname'])
    connection.login(
        email['username'],
        email['password']
    )

    return connection

if __name__ == '__main__':
    c = open_connection(verbose=True)
    try:
        print (c)
    finally:
        c.logout()

