The Heroku monitors allow users to monitor [Heroku](https://www.heroku.com) applications and instances.

---

## Dyno Status

The **Dyno Status** Monitor uses the Heroku platform API to poll the state of all dynos attached to the specified application. If the returned state is anything other than `up` or `idle` on any dyno, the Monitor is marked as false. This Monitor can be utilized to detect application crashes or infrastructure issues within Heroku.

---

## Dyno Status (Single)

The **Dyno Status (Single)** Monitor uses the Heroku platform API to poll the state of a single dyno. If the returned state is anything other than `up` or `idle`, the Monitor is marked as false. This Monitor can be utilized to detect application crashes or infrastructure issues within Heroku.

---

## Dyno Not Idle

The **Dyno Not Idle** Monitor uses the Heroku platform API to poll the state of all dynos attached to the specified application. If the returned state of any dyno is `idle`, the Monitor will be marked as false. This Monitor can be used to detect when dynos are over provisioned and not receiving enough traffic.

---

## Dyno Not Idle (Single)

The **Dyno Not Idle (Single)** Monitor uses the Heroku platform API to poll the state of a single dyno. If the returned state of any dyno is `idle`, the Monitor will be marked as false. This Monitor can be used to detect when dynos are over provisioned and not receiving enough traffic.

---