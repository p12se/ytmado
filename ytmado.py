# -*- coding: utf-8 -*-
import re
import os
import logging
import sys

import imaplib_connect
from pytube import YouTube

path_video = os.path.dirname(__file__) + '/video/'
logfile = os.path.dirname(__file__) + '/log/ytmado.log'
yt = YouTube()
mail_list = []
pattern = 'http://www.youtube.com/watch\?v\=[\w-]*' \
          '|https://www.youtube.com/watch\?v\=[\w-]*'

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', \
                    level=logging.DEBUG, filename=logfile)

c = imaplib_connect.open_connection()
logging.info(u'Connect OK')
c.select('INBOX', readonly=False)
logging.info(u'Inbox')
typ, data = c.search(None,'UnSeen')

if not data:
    logging.info(u'Not email\'s')
    sys.exit(0)
try:
    l = data[0].split()
    for i in l:
        typ, msg_data = c.fetch(i, '(BODY.PEEK[TEXT])')
        logging.info(u'Message read OK')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                mail_list.append(response_part[1])
        c.store(i, '+FLAGS', '\Seen')
        logging.info(u'Message seen OK')
except:
    c.close()
    c.logout()

try:
    links_to_mail = re.findall(pattern, mail_list[0])
    links = list(set(links_to_mail))
except IndexError:
    sys.exit(0)

for link in links:
    yt.url = str(link)
    try:
        video = (yt.filter('mp4')[-1])
        logging.info(video.filename + ' - ' + links[0])
        video.download(path_video)
        logging.info(u'Download file OK')
    except:
            logging.error(u'Error')

c.close()
c.logout()
#print(path_video)
#
#if __name__ == '__main__':
#    main()