# Heroku

The Heroku Reactions are designed to allow users to automatically perform common tasks for Heroku applications. Common tasks include scaling, restarting dynos and rolling back application versions.

## Call On

The Heroku Reactions all allow for the user to specify the `Call On` field, this field determines whether the reaction should be executed on Healthy or Failed monitors.

## Heroku: Scale Out Dynos

The Heroku: Scale Out Dynos reaction will increase the defined dynos by 1 every time it is triggered. If this reaction is attached to a monitor that runs at a 30 second interval the reaction will increase the number of dynos by one until the monitor changes state to one that does not match the `Call On` field.

This reaction will not scale beyond the `Maximum Dyno Quantity`. Once this value is reached the reaction will stop executing.

---

## Heroku: Scale In Dynos

The Heroku: Scale In Dynos reaction will decrease the defined dynos by 1 every time it is triggered. If this reaction is attached to a monitor that runs at a 30 second interval the reaction will decrease the number of dynos by one until the monitor changes state to one that does not match the `Call On` field.

This reaction will not scale below the `Minimum Dyno Quantity`. Once this value is reached the reaction will stop executing.

---

## Heroku: Scale Up Dynos

The Heroku: Scale Up Dynos reaction will increase the size of the defined dyno/s every time it is triggered. If a dyno is currently `1X` size, it will be scaled to `2X` on the next invocation of this reaction and to `PX` on the third.

This reaction will not scale beyond the `Maximum Dyno Size` defined for the reaction.

---

## Heroku: Scale Down Dynos

The Heroku: Scale Down Dynos reaction will decrease the size of the defined dyno/s every time it is triggered. If a dyno is currently `PX` size, it will be scaled to `2X` on the next invocation of this reaction and to `1X` on the third.

This reaction will not scale below the `Minimum Dyno Size` defined for the reaction.

---

## Heroku: Restart Single Dyno

When triggered the Heroku: Restart Single Dyno reaction will make a call to the Heroku Platform API to restart the specific dyno. This reaction is a simple restart of one specific dyno.

---

## Heroku: Restart All Dynos

When triggered the Heroku: Restart All Dynos reaction will make a call to the Heroku Platofrm API to restart all dynos associated with the specified application.

---

## Heroku: Rollback Release

When triggered the Heroku: Rollback Release reaction will make a call to the Heroku Platform API to rollback the applications release by 1 version. This reaction will continue rolling back the application version until the triggering monitor is returned to it's desired state or the current version matches the `Minimum Release Version` defined in the reaction.
