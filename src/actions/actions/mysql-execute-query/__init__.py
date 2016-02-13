from ..utils import ShouldRun
import pymysql

def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    if ShouldRun(redata, jdata):

        try:
            db = pymysql.connect(host=redata['data']['server'],
                                 user=redata['data']['user'],
                                 password=redata['data']['password'],
                                 cursorclass=pymysql.cursors.DictCursor)
        except: #pylint: disable=broad-except
            raise Exception('Failed to connect to db service')

        try:
            with db.cursor() as cursor:
                if cursor.execute(redata['data']['sql']):
                    return True
                else:
                    raise Exception('SQL execution failed: {0}'.format(cursor.fetchall()))
        finally:
            db.close()


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:  #pylint: disable=broad-except
        redata = kwargs['redata']
        logger = kwargs['logger']
        logger.warning(
            'mysql-execute-query: Reaction {id} failed: {message}'.format(
                id=redata['id'], message=e.message))
        return False
