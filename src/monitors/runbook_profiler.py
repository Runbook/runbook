#!/usr/bin/env python

import os
import gc
import datetime
from functools import wraps

from guppy import hpy

"""
# Runbook profiler

Runbook profiler is a very lightweight memory and time usage profiler.
It is intended to be used with long running processes.


## Performance impact

The time profiler incurs virtually no performance hit.
The memory profiler incurs a moderate to high hit ranging from:
. 30% for heavy memory/cpu usage functions 
. 250% for light memory/cpu usage ones


## Installing

Additional pip requirements are:
guppy==0.1.10


## Usage

To use the profiler, you need to do the following import:
from runbook_profiler import time_profile, mem_profile, full_profile

Currently, the profiler allows for functions of interest to be 
profiled by using one of the following decorators:
@time_profile # time only profiling
@mem_profile  # memory only profiling
@full_profile # time and memory profiling

To enable each of those decorators, the following environment variables 
have to be set:
FULL_PROFILE=1
TIME_PROFILE=1
MEM_PROFILE=1


## Running runbook_profiler

### using primes(10000000)

$ time FULL_PROFILE=1 python src/monitors/runbook_profile.py 
primes;2799.772 ms;'(10000000,)'
primes;23783.38 KB;20717.55 KB;'(10000000,)'
primes;0.059 ms;'(100,)'
primes;2832.31 KB;0.39 KB;'(100,)'
call_time;0.067 ms;'()'
call_time;2833.46 KB;0.07 KB;'()'

real	0m4.248s
user	0m4.019s
sys	0m0.155s

$ time  python src/monitors/runbook_profile.py 

real	0m2.798s
user	0m2.644s
sys	0m0.136s

$ time  python src/monitors/runbook_profile.py 

real	0m2.921s
user	0m2.730s
sys	0m0.156s

$ time TIME_PROFILE=1 python src/monitors/runbook_profile.py 
primes;2837.574 ms;'(10000000,)'
primes;0.083 ms;'(100,)'
call_time;0.013 ms;'()'

real	0m2.971s
user	0m2.684s
sys	0m0.255s

$ time MEM_PROFILE=1 python src/monitors/runbook_profile.py 
primes;23782.41 KB;20717.16 KB;'(10000000,)'
primes;2831.73 KB;0.39 KB;'(100,)'
call_time;2832.31 KB;0.07 KB;'()'

real	0m4.102s
user	0m3.887s
sys	0m0.192s


### using primes(100000000)

$ time  python src/monitors/runbook_profile.py 

real	0m29.124s
user	0m27.671s
sys	0m1.386s

$ time MEM_PROFILE=1 python src/monitors/runbook_profile.py 
primes;182920.45 KB;179855.19 KB;'(100000000,)'
primes;2831.74 KB;0.39 KB;'(100,)'
call_time;2832.32 KB;0.07 KB;'()'

real	0m40.977s
user	0m39.421s
sys	0m1.461s

"""

def asbool(str):
    if str.lower() in ['yes', 'y', 'true', '1']:
        return True
    else:
        return False

# Thanks to Martijn Pieters
# http://stackoverflow.com/a/10724898/
class conditional_decorator(object):
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            # Return the function unchanged, not decorated.
            return func
        return self.decorator(func)

    def mod(self, *args, **kwargs):
        new_decorator = self.decorator(*args, **kwargs)
        return conditional_decorator(new_decorator, self.condition)

# Thanks to Jochen Ritzel
# http://stackoverflow.com/a/5409569/
def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco

        
def full_arg_extractor(*args, **kwargs):
    return args, kwargs

def sample_arg_extractor(*args, **kwargs):
    return args


def time_log(name, secs, args):
    print "{0};{1} ms;'{2}'".format(name, secs*1000, args)

def mem_log(name, totmembytes, memdiffbytes, args):
    print "{0};{1:.2f} KB;{2:.2f} KB;'{3}'".format(name, float(totmembytes)/1024, float(memdiffbytes)/1024, args)

class memory_profiling_decorator(object):
    def __init__(self, arg_extractor):
        self.arg_extractor = arg_extractor

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            gc.disable()
            start = hpy().heap().size
            res = func(*args, **kwargs)
            end = hpy().heap().size
            gc.enable()
            mem_log(name=func.__name__, totmembytes=end , memdiffbytes=(end-start), args=self.arg_extractor(*args, **kwargs))
            return res
        return wrapper

class time_profiling_decorator(object):
    def __init__(self, arg_extractor):
        self.arg_extractor = arg_extractor

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            res = func(*args, **kwargs)
            end = datetime.datetime.now()
            time_log(name=func.__name__, secs=(end-start).total_seconds(), args=self.arg_extractor(*args, **kwargs))
            return res
        return wrapper


FULL_PROFILE=asbool(os.getenv('FULL_PROFILE', ''))
MEM_PROFILE=asbool(os.getenv('MEM_PROFILE', ''))
TIME_PROFILE=asbool(os.getenv('TIME_PROFILE', ''))

time_prof = time_profiling_decorator(sample_arg_extractor)
mem_prof = memory_profiling_decorator(sample_arg_extractor)

mem_profile = conditional_decorator(mem_prof, FULL_PROFILE or MEM_PROFILE)
time_profile = conditional_decorator(time_prof, FULL_PROFILE or TIME_PROFILE)
full_profile = composed(mem_profile, time_profile)

if __name__ == '__main__':
    @full_profile
#    @time_profile
#    @mem_profile
    def primes(n): 
        if n==2:
            return [2]
        elif n<2:
            return []
        s=range(3,n+1,2)
        mroot = n ** 0.5
        half=(n+1)/2-1
        i=0
        m=3
        while m <= mroot:
            if s[i]:
                j=(m*m-3)/2
                s[j]=0
                while j<half:
                    s[j]=0
                    j+=m
            i=i+1
            m=2*i+3
        return [2]+[x for x in s if x]
    
#    primes(100000000)
    primes(1000000)

    @full_profile
    def call_time():
        datetime.datetime.now()

    call_time()
