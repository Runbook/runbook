The Heroku Reactions are designed to allow users to automatically perform common tasks for Heroku applications. Common tasks include scaling, restarting dynos and rolling back application versions.

---

## Scale Out Dynos

The Scale Out Dynos reaction will increase the defined dynos by 1 every time it is triggered. If this reaction is attached to a monitor that runs at a 30 second interval the reaction will increase the number of dynos by one until the monitor changes state to one that does not match the `Call On` field.

This reaction will not scale beyond the `Maximum Dyno Quantity`. Once this value is reached the reaction will stop executing.

---

## Scale In Dynos

The Scale In Dynos reaction will decrease the defined dynos by 1 every time it is triggered. If this reaction is attached to a monitor that runs at a 30 second interval the reaction will decrease the number of dynos by one until the monitor changes state to one that does not match the `Call On` field.

This reaction will not scale below the `Minimum Dyno Quantity`. Once this value is reached the reaction will stop executing.

---

## Scale Up Dynos

The Scale Up Dynos reaction will increase the size of the defined dyno/s every time it is triggered. If a dyno is currently `1X` size, it will be scaled to `2X` on the next invocation of this reaction and to `PX` on the third.

This reaction will not scale beyond the `Maximum Dyno Size` defined for the reaction.

---

## Scale Down Dynos

The Scale Down Dynos reaction will decrease the size of the defined dyno/s every time it is triggered. If a dyno is currently `PX` size, it will be scaled to `2X` on the next invocation of this reaction and to `1X` on the third.

This reaction will not scale below the `Minimum Dyno Size` defined for the reaction.

---

## Restart Single Dyno

When triggered the Restart Single Dyno reaction will make a call to the Heroku Platform API to restart the specific dyno. This reaction is a simple restart of one specific dyno.

---

## Restart All Dynos

When triggered the Restart All Dynos reaction will make a call to the Heroku Platofrm API to restart all dynos associated with the specified application.

---

## Rollback Release

When triggered the Rollback Release reaction will make a call to the Heroku Platform API to rollback the applications release by 1 version. This reaction will continue rolling back the application version until the triggering monitor is returned to it's desired state or the current version matches the `Minimum Release Version` defined in the reaction.

---

## Create One-Off Dyno

One-off dynos in Heroku are generally used to kick off maitenance scripts or other backend jobs. These dynos typically run a process until it stops and then they are complete. The Create One-Off Dyno allows users to spawn a one off dyno and specify any command they want to run.

A real world example of this reaction would be detecting a database error using the HTTP Keyword monitor and launching a One-off dyno to run a clean up script.
