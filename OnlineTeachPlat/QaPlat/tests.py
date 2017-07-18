# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from LikeService import LikeService

from async.Event import EventType,EventModle,eventProducer,eventComsumer,workThread

from Queue import Queue
from threading import Thread as thread
import os,time

t = EventType()
t.setVaule("like")

a =  EventModle()
a.setKey("TYPE",t.getValue()).setKey("actorId","123")\
.setKey("entityType","1").setKey("entityId","798").setKey("entityOwnerId","159")
print a.getKey("TYPE")

b =  EventModle()
b.setKey("TYPE","email").setKey("actorId","123")\
.setKey("entityType","1").setKey("entityId","798").setKey("entityOwnerId","159")
print b.getKey("TYPE")


p = eventProducer()

t = workThread()
t.start()
i = 0
while True:
   
    i = i + 1
    print "test %s"%i
    p.fireEvnet(b)
    p.fireEvnet(a)
    time.sleep(5)



# c = eventComsumer()
# c.get()

# print m.getKey("TYPE")
# print m.getKey("actorId")
# print m.getKey("entityOwnerId")

