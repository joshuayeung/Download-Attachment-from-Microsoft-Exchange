#!/usr/bin/python
#coding=utf-8

from datetime import datetime, timedelta
#import pytz
from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, ServiceAccount, \
    EWSDateTime, EWSTimeZone, Configuration, NTLM, GSSAPI, CalendarItem, Message, \
    Mailbox, Attendee, Q, ExtendedProperty, FileAttachment, ItemAttachment, \
    HTMLBody, Build, Version, FolderCollection
import os

# You can also get the local timezone defined in your operating system
tz = EWSTimeZone.timezone('Asia/Hong_Kong')

# Specify your credentials. Username is usually in WINDOMAIN\username format, where WINDOMAIN is
# the name of the Windows Domain your username is connected to
credentials = Credentials(username='john@example.com', password='topsecret')

ews_url = 'mail.example.com'
ews_auth_type = 'NTLM'
primary_smtp_address = 'john@example.com'

config = Configuration(service_endpoint=ews_url, credentials=credentials, auth_type=ews_auth_type)

# An Account is the account on the Exchange server that you want to connect to.
account = Account(
    primary_smtp_address=primary_smtp_address,
    config=config, autodiscover=False,
    access_type=DELEGATE,
)


from ftplib import FTP
ftp_server_ip = FTP_SERVER_IP
username = 'username'
password = 'password'
remote_path = 'remote_path'
local_path = 'local_path'

with FTP(ftp_server_ip) as ftp:
    ftp.login(user=username, passwd=password)
    ftp.cwd(remote_path + '/copied data')
    filelist = [file for file in ftp.nlst() if file.startswith('YOUR_FILE_PREFIX')]

some_folder = account.inbox / 'some_folder'
for item in some_folder.all():
    print(item.subject, item.datetime_received.astimezone(tz))
    for attachment in item.attachments:
        if isinstance(attachment, FileAttachment):
            if attachment.name not in filelist:
                local_path = os.path.join(local_path, attachment.name)
                with open(local_path, 'wb') as f:
                    f.write(attachment.content)
                print('Saved attachment to', local_path)
                with FTP(ftp_server_ip) as ftp:
                    ftp.login(user=username, passwd=password)
                    ftp.cwd(remote_path)
                    file = open(local_path, 'rb')
                    ftp.storbinary('STOR {}'.format(attachment.name), file)
                    file.close()
