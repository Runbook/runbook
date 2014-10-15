#!/usr/bin/python
# Module for making calls to cloudflares API
######################################################################
#### callAPI(request, userdata)
#### checkZone(failedip, userdata)
# delRecord(rec,userdata)
# addRecord(rec,userdata)
# Benjamin J. Cane - 11/3/2013
######################################################################

import urllib
import urllib2
import json


def callAPI(request, usrdata):
    """ Call the cloudflare API with requested data and return results """
    # Build API Request
    data = []
    for value in usrdata:
        data.append(value)
    for value in request:
        data.append(value)

    # Encode & Send POST Data
    data = urllib.urlencode(data)
    url = "https://www.cloudflare.com/api_json.html"
    req = urllib2.Request(url, data)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    page = urllib2.urlopen(req).read()

    # Put json response into objects
    json_data = json.loads(page)
    return json_data


def checkZone(failed, usrdata):
    """ Check the cloudflare zone record for entries to remove """
    # Call api
    request = [('a', 'rec_load_all')]
    json_data = callAPI(request, usrdata)

    # Dicts and Lists for later
    failedrecs = {}
    names = {}
    recs = []
    faileddata = {}
    recdata = {}

    # Parse the response and tally failed entries
    # Check if the json request is successful
    if json_data["result"] == "success":
        # each zone is a dict in objs dict
        for line in json_data["response"]["recs"]["objs"]:
            # Added this to avoid duplicate zone names (i.e. MX records)
            # example key is A-somedomain.com
            key = line["type"] + "-" + line["name"]
            try:
                names[key] = names[key] + 1
            except KeyError:
                names[key] = 1

            if line["content"] == failed:
                failedrecs[line["rec_id"]] = key
                faileddata[line["rec_id"]] = {'type': line["type"],
                                              'name': line["name"],
                                              'content': line["content"],
                                              'service_mode': line["service_mode"],
                                              'ttl': line["ttl"],
                                              'prio': line["prio"]}

        # Go through failed records
        for rec in failedrecs.keys():
            if names[failedrecs[rec]] > 1:
                # if record isn't the last entry add for removal
                recs.append(rec)
                recdata[rec] = faileddata[rec]

        # Return the records that have failed
        return recs, recdata


def delRecord(rec, usrdata):
    """ Delete the record from cloudflares zone """
    # Call api
    request = [('a', 'rec_delete')]
    request.append(('id', rec))
    json_data = callAPI(request, usrdata)

    # Check api results
    if json_data["result"] == "success":
        return True
    else:
        return False


def addRecord(rec, usrdata, service_mode=False):
    """ Add a record to cloudflares DNS zone """
    # Call api
    rec2 = [('a', 'rec_edit')]
    for x in rec:
        rec2.append(x)
    request = ('a', 'rec_new')
    rec.append(request)
    json_data = callAPI(rec, usrdata)

    if json_data["result"] == "success":
        if service_mode is True:
            id = ('id', json_data["response"]["rec"]["obj"]["rec_id"])
            rec2.append(id)
            json_data2 = callAPI(rec2, usrdata)
            if json_data2["result"] == "success":
                return True
            else:
                return False
        else:
            return True
    else:
        return False
