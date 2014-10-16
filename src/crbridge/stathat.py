"""
stathat
~~~~~~~~~~~~~~

Blah blah blah.
"""

import urllib
import urllib2
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError(
                'You need something for json encoding! simplejson, Django, or Python >= 2.6')
try:
    from gevent import monkey
    from gevent.pool import Group
    import atexit
    monkey.patch_socket()
    monkey.patch_ssl()
    async_group = Group()
    HAS_GEVENT = True

    @atexit.register
    def _cleanup():
        async_group.join()
except ImportError:
    HAS_GEVENT = False

__all__ = ('StatHat', 'StatHatEZ', 'StatHatError',
           'ez_count', 'ez_value', 'classic_count', 'classic_value')

# We like security. :)
STATHAT_ENDPOINT = 'https://api.stathat.com'


class StatHatError(Exception):

    """Generic StatHat error."""


class _StatHatBase(object):
    VALUE_PATH = '/v'
    COUNT_PATH = '/c'

    @staticmethod
    def has_async():
        """Check if async support is available. Returns True if gevent is installed."""

        return HAS_GEVENT

    def __init__(self, **kwargs):
        self._auth = kwargs

    def tick(self, async=True):
        """Convenient helper for: count(1)"""

        return self.count(async=async)

    def count(self, count=1, async=True):
        """Request to track a counter. Returns True on success or raises a :class:`StatHatError`.

        :param count: Optional argument, Number you want to count, default=1.
        :param async: Optional argument to override the async behavior if gevent is available.
        """

        return self._send(self.COUNT_PATH, {'count': count}, async=async)

    def value(self, value, async=True):
        """Request to track a specific value. Returns True on success or raises a :class:`StatHatError`.

        :param value: Value you want to track.
        :param async: Optional argument to override the async behavior if gevent is available.
        """
        return self._send(self.VALUE_PATH, {'value': value}, async=async)

    def _send(self, path, data, async):
        endpoint = STATHAT_ENDPOINT + path
        payload = self._auth.copy()
        payload.update(data)

        if HAS_GEVENT and async is not False:
            # Async request should be completely silent and ignore any
            # errors that may be thrown.
            async_group.spawn(self._send_inner, endpoint, payload, silent=True)
        else:
            # If the request isn't async, we should make an effort
            # to parse the response and return it, or raise a proper exception
            try:
                raw = self._send_inner(endpoint, payload)
            except urllib2.URLError, e:
                # Network issue or something else affecting the general request
                raise StatHatError(e)
            try:
                resp = json.loads(raw)
            except Exception:
                # JSON decoding failed meaning StatHat returned something bad
                raise StatHatError('Something bad happened: %s' % raw)
            if 'msg' in resp and 'status' in resp:
                if resp['status'] != 200:
                    # Normal error from StatHat
                    raise StatHatError(resp['msg'])
            else:
                # 'msg' and 'status' keys weren't returned, something bad happened
                raise StatHatError('Something bad happened: %s' % raw)
        return True

    def _send_inner(self, endpoint, data, silent=False):
        try:
            return urllib2.urlopen(endpoint, urllib.urlencode(data)).read()
        except urllib2.URLError:
            # We want to surface the error on non-async requests
            if not silent:
                raise
            return None


class StatHat(_StatHatBase):

    def __init__(self, user_key, stat_key):
        """Implements the Classic API <http://www.stathat.com/docs/api>

        :param user_key: Private key identifying the user.
        :param stat_key: Private key identifying the stat.
        """

        super(StatHat, self).__init__(ukey=user_key, key=stat_key)


class StatHatEZ(_StatHatBase):
    VALUE_PATH = '/ez'
    COUNT_PATH = '/ez'

    def __init__(self, ezkey, stat_name):
        """Implements the EZ API <http://www.stathat.com/docs/api>

        :param ezkey: Your account "EZ key" or email address.
        :param stat_name: The ad-hoc stat name to use.
        """

        super(StatHatEZ, self).__init__(ezkey=ezkey, stat=stat_name)


def ez_count(ezkey, stat_name, count=1, async=True):
    """Convenience function for sending one off "count" calls to the EZ api.

    :param ezkey: Your account "EZ key" or email address.
    :param stat_name: The ad-hoc stat name to use.
    :param count: Optional argument, Number you want to count, default=1.
    :param async: Optional argument to override the async behavior if gevent is available.
    """

    stats = StatHatEZ(ezkey, stat_name)
    return stats.count(count, async=async)


def ez_value(ezkey, stat_name, value, async=True):
    """Convenience function for sending one off "value" calls to the EZ api.

    :param ezkey: Your account "EZ key" or email address.
    :param stat_name: The ad-hoc stat name to use.
    :param value: Value you want to track.
    :param async: Optional argument to override the async behavior if gevent is available.
    """

    stats = StatHatEZ(ezkey, stat_name)
    return stats.value(value, async=async)


def classic_count(user_key, stat_key, count=1, async=True):
    """Convenience function for sending one off "count" calls to the Classic api.

    :param user_key: Private key identifying the user.
    :param stat_key: Private key identifying the stat.
    :param count: Optional argument, Number you want to count, default=1.
    :param async: Optional argument to override the async behavior if gevent is available.
    """

    stats = StatHat(user_key, stat_key)
    return stats.count(count, async=async)


def classic_value(user_key, stat_key, value, async=True):
    """Convenience function for sending one off "value" calls to the Classic api.

    :param user_key: Private key identifying the user.
    :param stat_key: Private key identifying the stat.
    :param value: Value you want to track.
    :param async: Optional argument to override the async behavior if gevent is available.
    """

    stats = StatHat(user_key, stat_key)
    return stats.value(value, async=async)
