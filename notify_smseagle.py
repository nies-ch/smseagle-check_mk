#!/usr/bin/env python3

import urllib.request
import urllib.parse
import smtplib
import re
import sys
import socket
from os import environ
from email.mime.text import MIMEText

### Configuration Parameters

EAGLE_HOSTS    = [ '1.2.3.4', '5.6.7.8', '9.10.11.12' ]
EAGLE_LOGIN    = 'eagleuser'
EAGLE_PASSWORD = 'eaglepassword'
EAGLE_TIMEOUT  = 10
PHONE_REGEX    = '^(\+|00)41\d+$'
MAIL_FROM      = 'check_mk@example.com'
MAIL_TO        = 'my-email@example.com'
MAIL_HOSTS     = [ 'localhost', 'smtp1.example.com', 'smtp2.example.com' ]
MAIL_PORT      = 25


def complain(error):
    """
    Complain about errors via email. If that fails, just print the error
    message to stdout.
    """
    print(error)
    msg = MIMEText(error)
    msg['To'] = MAIL_TO
    msg['From'] = MAIL_FROM
    msg['Subject'] = 'Check_MK: SMS Notification Error'
    message_sent  = False

    for host in MAIL_HOSTS:
        if not message_sent:
            try:
                server = smtplib.SMTP(host, MAIL_PORT)
                server.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
                server.quit()
            except socket.error as e:
                print("Could not connect to " + host + ": " + str(e))
            except smtplib.SMTPException as e:
                print("Sending email failed: " + str(e))
            except:
                print("Unknown error:", sys.exc_info()[0])
            else:
                message_sent = True
                break
    return


def format_message():
    """
    Format the SMS message using the environment variables given by Check_MK.
    See https://mathias-kettner.com/cms_notifications.html for details.
    """ 
    if 'NOTIFY_WHAT' in environ:
        if environ['NOTIFY_WHAT'] == 'HOST':
            msg = "%s %s: %s (%s)" % (
                  environ['NOTIFY_NOTIFICATIONTYPE'], 
                  environ['NOTIFY_HOSTNAME'],
                  environ['NOTIFY_HOSTOUTPUT'],
                  environ['NOTIFY_SHORTDATETIME'])
        elif environ['NOTIFY_WHAT'] == 'SERVICE':
            msg = "%s %s: %s %s (%s)" % (
                  environ['NOTIFY_NOTIFICATIONTYPE'],
                  environ['NOTIFY_HOSTNAME'],
                  environ['NOTIFY_SERVICEDESC'],
                  environ['NOTIFY_SERVICEOUTPUT'],
                  environ['NOTIFY_SHORTDATETIME'])
        else:
            msg = "Unknown notification method: " + environ['NOTIFY_WHAT']
    else:
        msg = "Environment variable NOTIFY_WHAT not defined."
    return msg


def send_eagle_sms(to,message):
    """
    Sending SMS via SMSEagle HTTP API. Uses hosts defined in list EAGLE_HOSTS.
    Upon failure an email with the error is sent and next host is used.
    """
    query_args   = { 'login':EAGLE_LOGIN, 'pass':EAGLE_PASSWORD, 'to':to,
                     'message':message }
    encoded_args = urllib.parse.urlencode(query_args)
    message_sent  = False

    for host in EAGLE_HOSTS:
        url =  'http://%s/index.php/http_api/send_sms?%s' % (host, encoded_args)
        if not message_sent:
            try:
                result = urllib.request.urlopen(url,None,EAGLE_TIMEOUT).read()
            except urllib.request.HTTPError as e:
                complain('Sending SMS via SMSEagle %s failed: %s' 
                          % (host, str(e.code))) 
            except urllib.request.URLError as e:
                complain('Sending SMS via SMSEagle %s failed: %s'
                          % (host, str(e.args)))
            else:    
                if result.startswith('OK;'):
                    message_sent = True
                    print('SMS successfully sent via %s to %s.' % (host, to))
                    break
                else:
                    message_sent = False
                    complain('Sending SMS via SMSEagle %s failed: %s' 
                             % (host, result.rstrip()))
            
    return


if not 'NOTIFY_CONTACTPAGER' in environ:
    complain('Environment variable NOTIFY_CONTACTPAGER missing')
else:
    phone_number = environ['NOTIFY_CONTACTPAGER']
    if re.match(PHONE_REGEX, phone_number):
        eagle_message = format_message()
        send_eagle_sms(phone_number, eagle_message)