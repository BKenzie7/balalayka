#!/usr/bin/python
# -*- coding: utf-8 -*-

# from Queue import Queue
import time

def printer(event_queue):
    while 1:
        event = event_queue.get()
        print event
        event_queue.task_done()
        time.sleep(0.01)
