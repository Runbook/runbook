# Module for interacting with CloudFlare
# updated for v4 of cloudflare API

import requests
import json


baseurl = "https://api.cloudflare.com/client/v4"


def validate_response(req, logger):
    ''' General response validation '''
    logger.debug("cloudflare: CloudFlare replied with " + str(req.status_code))
    if req.status_code == 200:
        data = json.loads(req.text)
        if data['success'] is True:
            return True
    else:
        logger.debug("cloudflare: Response text: %s" % req.text)
        return False

def get_zone_analytics(email, key, domain, logger, start_time, end_time):
    ''' Grab Analytics from CloudFlares API for desired zone '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    zoneid = get_zoneid(email, key, domain, logger)
    url = "%s/zones/%s/analytics/dashboard" % (baseurl, zoneid)
    url = "%s?since=%s&until=%s&exclude_series=false" % (url,
                                                        start_time, end_time)
    logger.debug("cloudflare: Grabbing analytics from url " + url)
    try:
        req = requests.get(url=url, headers=headers)
        if validate_response(req, logger):
            metrics = json.loads(req.text)
            return metrics
        else:
            return None
    except:
        return None
    

def change_zone_settings(email, key, domain, logger, setting, value):
    ''' Get the ZoneID for the specified domain '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    zoneid = get_zoneid(email, key, domain, logger)
    url = "%s/zones/%s/settings/%s" % (baseurl,
                                       zoneid, setting)
    payload = json.dumps(value)
    logger.debug("cloudflare: Requesting url " + url)
    try:
        req = requests.patch(url=url, headers=headers, data=payload)
        if validate_response(req, logger):
            return True
        else:
            return False
    except:
        return False


def get_recs_by_domain(email, key, domain, logger):
    ''' Get the DNS Records for a domain by domain name '''
    zoneid = get_zoneid(email, key, domain, logger)
    return get_recs(email, key, zoneid, logger)


def get_zoneid(email, key, domain, logger):
    ''' Get the ZoneID for the specified domain '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "%s/zones?name=%s" % (baseurl, domain)
    logger.debug("cloudflare: Requesting url " + url)
    try:
        req = requests.get(url=url, headers=headers)
        if validate_response(req, logger):
            data = json.loads(req.text)
            for zone in data['result']:
                if zone['name'] == domain:
                    return zone['id']
        else:
            return None
    except:
        return None


def get_recs(email, key, zoneid, logger, page=1, search={}):
    ''' Return a dictionary of records that match searchstring or zoneid '''
    return_data = {}
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "%s/zones/%s/dns_records?per_page=100" % (baseurl, str(zoneid))
    for param in search.keys():
        url = "%s&%s=%s" % (url, param, search[param])
    if page > 1:
        url = "%s&page=%s" % (url, str(page))
    logger.debug('cloudflare: Requesting url ' + url)
    try:
        req = requests.get(url=url, headers=headers)
        if validate_response(req, logger):
            data = json.loads(req.text)
            if data['result_info']['total_pages'] > page:
                newpage = page + 1
                newdata = get_recs(email, key, zoneid, logger, page=newpage, search=search)
                for new in newdata.keys():
                    return_data[new] = newdata[new]
            for rec in data['result']:
                return_data[rec['id']] = rec
        return return_data
    except:
        return return_data

def add_rec(email, key, zoneid, logger, rec):
    ''' Add a new DNS record using the rec dictionary as json data '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "%s/zones/%s/dns_records" % (baseurl, str(zoneid))
    payload = json.dumps(rec)
    try:
        req = requests.post(url=url, headers=headers, data=payload)
        return validate_response(req, logger)
    except:
        return False


def del_rec(email, key, zoneid, logger, recid):
    ''' Delete the specified DNS entry '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "%s/zones/%s/dns_records/%s" % (baseurl, str(zoneid), str(recid))
    try:
        req = requests.delete(url=url, headers=headers)
        return validate_response(req, logger)
    except:
        return False


def update_rec(email, key, zoneid, logger, recid, rec):
    ''' Update DNS record '''
    headers = {
        'X-Auth-Email' : email,
        'X-Auth-Key' : key,
        'Content-Type' : 'application/json'
    }
    url = "%s/zones/%s/dns_records/%s" % (baseurl, str(zoneid), str(recid))
    payload = json.dumps(rec)
    try:
        req = requests.put(url=url, headers=headers, data=payload)
        return validate_response(req, logger)
    except:
        return False
