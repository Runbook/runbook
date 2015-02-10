"""Base Reaction class."""

import time


class BaseReaction(object):
    """Base class for a reaction.

    Actual reactions are supposed to subclass it and override the _Action method
    at minimum.
    """

    def __init__(self, **kwargs):
        self.redata = kwargs['redata']
        self.jdata = kwargs['jdata']
        self.rdb = kwargs['rdb']
        self.r_server = kwargs['r_server']
        self.config = kwargs['config']
        self.logger = kwargs['logger']

    def _ShouldRun(self):
        """Common set of conditions to check if the reaction should be run.

        Note that this is applicable to *most* reactions, but your reaction
        may have a different set of requirements. If it does, override this
        method.
        """
        return (
            # Check that we exceeded user specified failcount for the reaction
            # to trigger.
            self.jdata['failcount'] >= self.redata['trigger'] and
            # Check that we don't run the reaction more often than the specified
            # frequency.
            (time.time() - float(self.redata['lastrun'])) >= self.redata['frequency'] and
            # Should the reaction be called when the monitor is True or False?
            self.redata['data']['call_on'] in self.jdata['check']['status']
        )

    def Run(self):
        """Runs a reaction.

        Subclasses MUST NOT override.
        """
        if self._ShouldRun():
            return self._SafeAction()

    def _Action(self):
        """Actual business logic of the reaction.

        Subclasses MUST override.

        Returns: bool or None
            True, if the reaction execution was successful.
            False, if the reaction execution was unsuccessful.
            None, if the reaction execution was skipped.
        """
        raise NotImplementedError()

    def _SafeAction(self):
        """Wrapper around Action method.

        Catches all exceptions raised by Action and logs them, preventing the
        module itself to crash.

        Subclasses MUST NOT override.
        """
        try:
            return self._Action()
        except Exception, e:  #pylint: disable=broad-except
            self.logger.warning(
                '{module}: Reaction {id} failed: {message}'.format(
                    module=self.__module__,
                    id=self.redata['id'],
                    message=e.message))
            return False
