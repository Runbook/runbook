The **Notifications** Reactions are designed to be a collection of notification services. While our desire is to build a system that requires zero human interaction, you can think of this as a system for escalating issues to a human when necessary.

---

## Email Notifications

The **Email Notifications** Reaction is designed to allow users to notify a specific user of Monitor condition changes. Currently email notifications are limited to one every 15 minutes. This is to prevent "Inbox Armageddon" where many Monitors fail and the end user receives an unmanageable number of emails.

---

## Nexmo SMS Notifications

The **Nexmo SMS Notifications** Reaction is designed to allow users to send an SMS message to mobile devices around the world. This reaction utilizes your own Nexmo API key, it is important to ensure both triggering and frequency values are set correctly.

---

## Twilio SMS Notifications

The **Twilio SMS Notifications** Reaction is designed to allow users to send an SMS message to mobile devices around the world. This reaction utilizes your own Twilio API key, it is important to ensure both triggering and frequency values are set correctly.

---

## PagerDuty Incident

The **PagerDuty Incident** Reaction is designed to allow users to trigger incidents with PagerDuty's API. Currently this reaction only triggers incidents and does not close them.
