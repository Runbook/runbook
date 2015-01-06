


install:
	cd bookie.app ; python setup.py install

develop:
	cd bookie.app ; python setup.py develop

clean:
	cd bookie.app ; python setup.py clean --all ; rm -Rf dist/ bookie.egg-info/
