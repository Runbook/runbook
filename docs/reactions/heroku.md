The Heroku Reactions are designed to allow users to automatically perform common tasks for [Heroku](https://www.heroku.com/) applications. Common tasks include scaling, restarting dynos and rolling back application versions.

---

## Scale Out Dynos

The **Scale Out Dynos** Reaction will increase the defined dynos by 1 every time it is triggered. If this Reaction is attached to a Monitor that runs at a 30 second interval, the Reaction will increase the number of dynos by one until the Monitor changes state to one that does not match the `Call On` field.

This Reaction will not scale beyond the `Maximum Dyno Quantity`. Once this value is reached the Reaction will stop executing.

---

## Scale In Dynos

The **Scale In Dynos** Reaction will decrease the defined dynos by 1 every time it is triggered. If this Reaction is attached to a Monitor that runs at a 30 second interval, the Reaction will decrease the number of dynos by one until the Monitor changes state to one that does not match the `Call On` field.

This Reaction will not scale below the `Minimum Dyno Quantity`. Once this value is reached the Reaction will stop executing.

---

## Scale Up Dynos

The **Scale Up Dynos** Reaction will increase the size of the defined dyno/s every time it is triggered. If a dyno is currently `1X` size, it will be scaled to `2X` on the next invocation of this Reaction and to `PX` on the third.

This Reaction will not scale beyond the `Maximum Dyno Size` defined for the Reaction.

---

## Scale Down Dynos

The **Scale Down Dynos** Reaction will decrease the size of the defined dyno/s every time it is triggered. If a dyno is currently `PX` size, it will be scaled to `2X` on the next invocation of this Reaction and to `1X` on the third.

This Reaction will not scale below the `Minimum Dyno Size` defined for the Reaction.

---

## Restart Single Dyno

When triggered, the **Restart Single Dyno** Reaction will make a call to the Heroku Platform API to restart the specific dyno. This Reaction is a simple restart of one specific dyno.

---

## Restart All Dynos

When triggered, the **Restart All Dynos** Reaction will make a call to the Heroku Platform API to restart all dynos associated with the specified application.

---

## Rollback Release

When triggered, the **Rollback Release** Reaction will make a call to the Heroku Platform API to rollback the applications release by 1 version. This Reaction will continue rolling back the application version until the triggering Monitor is returned to it's desired state or the current version matches the `Minimum Release Version` defined in the Reaction.

---

## Create One-Off Dyno

One-off dynos in Heroku are generally used to kick off maintenance scripts or other back-end jobs. These dynos typically run a process until it stops and then they are complete. The **Create One-Off Dyno** Reaction allows users to spawn a one off dyno and specify any command they want to run.

A real world example of this Reaction would be detecting a database error using the **HTTP GET: Keyword** and launching a **Create One-Off Dyno** Reaction to run a clean up script.

---