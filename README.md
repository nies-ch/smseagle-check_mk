# Check_MK with SMS Notification using SMSEagle
Plugin for Check_MK SMS alerts &amp; notifications with use of SMSEagle device

The following Python script can be used for Check_MK to send SMS alerts using SMSEagle devices. A short message will only be sent, when the user has entered a valid phone number as pager address, according to PHONE_REGEX. Be careful when copying the Python code, because that language highly depends on how the block indentation with white space is done. Also syntax and library names change with different Python versions. It was my first Python script to learn that language.

Further details about Check_MK and SMSEagle:  
- https://checkmk.com/cms_notifications.html
- https://www.smseagle.eu/api/

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

- 2020-05-15: Publish to github.com. Rewrote from Python 2 to Python 3.
- 2018-09-05: Try multiple mail servers. Restrict mobile number to +41 or 0041.
- 2018-08-28: Don't send if NOTIFY_CONTACTPAGER is invalid format. 
- 2018-08-27: Added NOTIFY_NOTIFICATIONTYPE.
- 2018-08-23: First release