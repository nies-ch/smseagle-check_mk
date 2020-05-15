# Check_MK with SMS Notification using SMSEagle
Plugin for Check_MK SMS alerts &amp; notifications with use of SMSEagle device

The following Python script can be used for Check_MK to send SMS alerts using SMSEagle devices. A short message will only be sent, when the user has entered a valid phone number as pager address, according to PhoneRegex. Be careful when copying the Python code, because that language highly depends on how the block indentation with white space is done.

## Installation

```
cd /tmp
git clone https://github.com/nies-ch/smseagle-check_mk
su - mysite
cp /tmp/smseagle-check_mk/notify_smseagle.py ~/local/share/check_mk/notifications
chmod 755 ~/local/share/check_mk/notifications/notify_smseagle.py
omd reload
```

Further details about Check_MK and SMSEagle:  
- https://checkmk.com/cms_notifications.html
- https://www.smseagle.eu/api/
