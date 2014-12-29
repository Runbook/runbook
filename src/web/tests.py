import unittest

tests = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2, buffer=True).run(tests)
