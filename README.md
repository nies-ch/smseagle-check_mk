# CheckMK with SMS Notification using SMSEagle

Notification plugin for Check_MK SMS alerts and notifications with use of SMSEagle device.

The following Python script can be used for CheckMK to send SMS alerts using SMSEagle devices. A short message will only be sent, when the user has entered a valid phone number as pager address, according to phone_regex. Be careful when copying the Python code, because that language highly depends on how the block indentation with white space is done. Also syntax and library names change with different Python versions. It was my first Python script to learn that language.

## Sample Configuration File in JSON Format

API supports user/password login and access token style. The SMSEagle devices are processed in the order defined. If sending fails, then send alert via mail using defined mail_hosts.

```
{
  "eagle_hosts": [
    { "api_send_sms": "http://1.2.3.4/http_api/send_sms", "login": "eagleuser", "pass": "********" },
    { "api_send_sms": "http://1.2.3.5/http_api/send_sms", "access_token": "**********************" }
  ],
  "eagle_timeout": 10,
  "phone_regex": "^(\\+|00)\\d+$",
  "mail_from" : "checkmk@example.com",
  "mail_to"   : "monitoring@example.com",
  "mail_hosts": [
    { "host": "localhost", "port": 25 },
    { "host": "smtp1.example.com", "port": 25 },
    { "host": "smtp2.example.com", "port": 25 }
  ]
}
```

## Installation

```
cd /tmp
git clone https://github.com/nies-ch/smseagle-check_mk
su - mysite
cp /tmp/smseagle-check_mk/notify_smseagle.py ~/local/share/check_mk/notifications
chmod 755 ~/local/share/check_mk/notifications/notify_smseagle.py
omd reload
```

## Changes

- 2022-08-25: Moved configuration parameters into dedicated JSON file.
- 2020-05-15: Publish to github.com. Rewrote from Python 2 to Python 3.
- 2018-09-05: Try multiple mail servers. Restrict mobile number to +41 or 0041.
- 2018-08-28: Don't send if NOTIFY_CONTACTPAGER is invalid format. 
- 2018-08-27: Added NOTIFY_NOTIFICATIONTYPE.
- 2018-08-23: First release

## To Do

- Adjust code to get Get 3G/4G signal strenght and modem state via API before sending. If that's not okay, show error message and choose next SMSEagle device


## References

Further details about Check_MK and SMSEagle:  
- https://checkmk.com/cms_notifications.html
- https://www.smseagle.eu/api/