CloudRoutes API
================

## Types of API Requests

### Server Requests

* Check in

### Monitor Requests

* Change Monitor Status
* Request Monitor Status
* Request Monitor Details

### Reaction Reqeusts

* Notify Reaction Run
* Reqeust Reaction Details

## API Request Details

### Server Requests


#### Check in


##### Request

    { 
      "action" : "checkin",
      "apikey" : "asdjfladsjflksdajljfla",
      "hostname" : "test01.example.com",
      "user" : "test@example.com"
      "time" : 1423434232.000
    }

##### Response

    {
      "action" : "checkin",
      "result" : "success",
      "workqueue" : [
                      { "name" : "Bla",
                        "type" : "monitor",
                        "data" : {
                                    "ctype" : "unix-shell",
                                    "cmd" : "ls -la | grep -q test"
                                  },
                        "status" : "healthy"
                      },
                      { "name" : "Bla",
                        "type" : "reaction",
                        "data" : {
                                    "ctype" : "unix-shell",
                                    "cmd" : "ls -la | grep -q test",
                                    "call_on" : "failed"
                                  },
                        "status" : "healthy"
                      } 
                    ],
      "responding_host" : "a.cloudrout.es"
    }
  
### Monitor Requests

#### Change Monitor Status

##### Request

    {
      "action" : "change",
      "apikey" : "asdfasdfsafdsa",
      "cid" : "32331231",
      "status" : "failed",
      "time" : 142323422.00,
      "user" : "test@example.com
    }

##### Response

    {
      "action" : "change",
      "result" : "success",
    }
      
