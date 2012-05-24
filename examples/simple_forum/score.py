#!/usr/bin/env python2

import math
import datetime
import time

def score(now, t_0):
    return 0.5 ** ((now - t_0)/3600)

def t_offset(score):
    return -3600*math.log(score)/math.log(0.5)


ORIGIN = datetime.datetime.utcnow()
d = datetime.timedelta(minutes=1)

t_0 = time.mktime(ORIGIN.utctimetuple())
t = t_0

for i in range(1,61):
    now = time.mktime((ORIGIN+d*i).utctimetuple())
    t = now+t_offset(score(now, t)+ 1.0/(i+1))
    print t-now



