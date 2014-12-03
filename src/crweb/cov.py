import os
import unittest
import coverage

cov = coverage.coverage(branch=True, include='src/crweb/*')
cov.start()
tests = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2, buffer=True).run(tests)
cov.stop()
cov.save()
print 'Coverage Summary:'
cov.report()
basedir = os.path.abspath(os.path.dirname(__file__))
covdir = os.path.join(basedir, 'tmp/coverage')
cov.html_report(directory=covdir)
print('HTML version: file://%s/index.html' % covdir)
cov.erase()
