"""Common utility classes and methods for reactions."""

import time

def ShouldRun(redata, jdata):
    """Common set of conditions to check if the reaction should be run.

    Note that this is applicable to *most* reactions, but your reaction may have
    a different set of requirements. Do NOT use blindly.
    """
    return (
        # Check that we exceeded user specified failcount for the reaction
        # to trigger.
        jdata['failcount'] >= redata['trigger'] and
        # Check that we don't run the reaction more often than the specified
        # frequency.
        (time.time() - float(redata['lastrun'])) >= redata['frequency'] and
        # Should the reaction be called when the monitor is True or False?
        redata['data']['call_on'] in jdata['check']['status']
    )
