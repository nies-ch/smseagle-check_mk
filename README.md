# smseagle-check_mk
Plugin for Check_MK SMS alerts &amp; notifications with use of SMSEagle device

The following Python script can be used for Check_MK to send SMS alerts using SMSEagle devices. Just copy it as site user into the folder ~/local/share/check_mk/notifications and make it executeable. 

```
su - mysite
cp /var/tmp/notify_smseagle ~/local/share/check_mk/notifications
chmod 755 ~/local/share/check_mk/notifications/notify_smseagle
omd reload
```

A short message will only be sent, when the user has entered a valid phone number as pager address, according to PhoneRegex. Be careful when copying the Python code, because that language highly depends on how the block indentation with white space is done.

Further details can be found here: 
- https://checkmk.com/cms_notifications.html
- https://www.smseagle.eu/api/
