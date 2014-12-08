The Heroku monitors allow users to monitor Heroku applications and instances.

---

## Dyno Status

This monitor uses the Heroku platform API to poll the state of a all dynos attached to the specified application. If the returned state is anything other than `up` or `idle` on any dyno, the monitor is marked as false. This monitor can be utilized to detect application crashes or infrastructure issues within Heroku.

---

## Dyno Status (Single)

This monitor uses the Heroku platform API to poll the state of a single dyno. If the returned state is anything other than `up` or `idle`, the monitor is marked as false. This monitor can be utilized to detect application crashes or infrastructure issues within Heroku.

---

## Dyno Not Idle

This monitor uses the Heroku platform API to poll the state of all dynos attached to the specified application. If the returned state of any dyno is `idle` the monitor will be marked as false. This monitor can be used to detect when dyno's are over provisioned and not receiving enough traffic.

---

## Dyno Not Idle (Single)

This monitor uses the Heroku platform API to poll the state of a single dyno. If the returned state of any dyno is `idle` the monitor will be marked as false. This monitor can be used to detect when dyno's are over provisioned and not receiving enough traffic.
