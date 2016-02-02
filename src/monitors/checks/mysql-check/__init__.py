''' Perform a mysql show status and measure metrics '''
import pymysql

def check(**kwargs):
    ''' Measure MySQL Status '''
    jdata = kwargs['jdata']
    logger = kwargs['logger']

    status = {}
    try:
        # Connect to DB Instance
        db = pymysql.connect(host=jdata['data']['server'],
                            user=jdata['data']['user'],
                            password=jdata['data']['password'],
                            cursorclass=pymysql.cursors.DictCursor)
    except: #pylint disable=broad-except
        logger.debug("mysql-check: Failed to connect to db service")
        return False

    try:
        with db.cursor() as cursor:
            # Get Status
            cursor.execute("show status")
            for result in cursor.fetchall():
                status[result['Variable_name']] = result['Value']
    finally:
        db.close()

    if jdata['data']['status_variable'] in status.keys():
        logger.debug("mysql-check: Status Variable {0} is {1}, checking if {2} than {3}".format(
            jdata['data']['status_variable'],
            status[jdata['data']['status_variable']],
            jdata['data']['threshold_type'],
            jdata['data']['threshold']))

        if "greater" in jdata['data']['threshold_type']:
            if int(status[jdata['data']['status_variable']]) > int(jdata['data']['threshold']):
                return False
            else:
                return True

        if "less" in jdata['data']['threshold_type']:
            if int(status[jdata['data']['status_variable']]) < int(jdata['data']['threshold']):
                return False
            else:
                return True

    else:
        logger.debug("mysql-check: {0} not found in returned data".format(
            jdata['data']['status_variable']))
        return None
