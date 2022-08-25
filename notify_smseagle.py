#!/usr/bin/env python3
# =============================================================================
# NOTIFY VIA SMS USING SMSEAGLE FAILOVER
# =============================================================================

import json
import urllib.request
import urllib.parse
import smtplib
import re
import sys
import socket
from os import environ
from email.mime.text import MIMEText


# -----------------------------------------------------------------------------
# Configuration Parameters in JSON file
# -----------------------------------------------------------------------------
CONFIG_FILE = environ['HOME'] + '/.notify_smseagle.json'


# -----------------------------------------------------------------------------
# read_jsonfile
# -----------------------------------------------------------------------------
def read_jsonfile(file):
    data = []
    with open(file) as json_file:
        data = json.load(json_file)
    # Defaults
    data["eagle_timeout"] = 10 if not "eagle_timeout" in data else data["eagle_timeout"]
    return data


# ----------------------------------------------------------------------------
# Complain 
# ----------------------------------------------------------------------------
def complain(error):
    """
    Complain about errors via email. If that fails, just print the error
    message to stdout.
    """
    print(error)
    msg = MIMEText(error)
    msg['To'] = cfg['mail_to']
    msg['From'] = cfg['mail_from'] 
    msg['Subject'] = 'Check_MK: SMS Notification Error'
    MessageSent  = False

    for mail_host in cfg['mail_hosts']:
        if not MessageSent:
            try:
                server = smtplib.SMTP(mail_host['host'], mail_host['port'])
                server.sendmail(cfg['mail_from'], cfg['mail_to'], msg.as_string())
                server.quit()
            except socket.error as e:
                print("Could not connect to " + mail_host['host'] + ": " + str(e))
            except smtplib.SMTPException as e:
                print("Sending email failed: " + str(e))
            except:
                print("Unknown error:", sys.exc_info()[0])
            else:
                MessageSent = True
                break
    return



# ----------------------------------------------------------------------------
# Format Message 
# ----------------------------------------------------------------------------
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



# ----------------------------------------------------------------------------
# Send Eagle SMS
# ----------------------------------------------------------------------------
def send_eagle_sms(to, message):
    """
    Sending SMS via SMSEagle HTTP API. Uses hosts defined in list cfg['eagle_hosts'].
    Upon failure an email with the error is sent and next host is used.
    """
    MessageSent  = False
    ErrorMessage = ''
    for eagle_host in cfg['eagle_hosts']:
        query_args = {
            'to':  to,
            'message': message }
        if 'access_token' in eagle_host:
             query_args['access_token'] = eagle_host['access_token']
        else:
            query_args['login'] = eagle_host['login']
            query_args['pass']  = eagle_host['pass']
        encoded_args = urllib.parse.urlencode(query_args)
        url = eagle_host['api_send_sms'] + '?' + encoded_args
        if not MessageSent:
            try:
                result = urllib.request.urlopen(url, None, cfg['eagle_timeout']).read()
            except urllib.request.HTTPError as e:
                complain('Sending SMS via SMSEagle %s failed: %s' 
                          % (eagle_host['api_send_sms'], str(e.code))) 
            except urllib.request.URLError as e:
                complain('Sending SMS via SMSEagle %s failed: %s'
                          % (eagle_host['api_send_sms'], str(e.args)))
            else:    
                if result.startswith(b'OK;'):
                    MessageSent = True
                    print('SMS successfully sent via %s to %s.' % (eagle_host['api_send_sms'], to))
                    break
                else:
                    MessageSent = False
                    complain('Sending SMS via SMSEagle %s failed: %s' 
                             % (eagle_host['api_send_sms'], result.rstrip()))
    return



# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

cfg = read_jsonfile(CONFIG_FILE)

if not 'NOTIFY_CONTACTPAGER' in environ:
    complain('Environment variable NOTIFY_CONTACTPAGER missing')
else:
    phone_number = environ['NOTIFY_CONTACTPAGER']
    if re.match(cfg['phone_regex'], phone_number):
        eagle_message = format_message()
        send_eagle_sms(phone_number, eagle_message)
