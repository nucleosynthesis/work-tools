#!/usr/bin/env python 
import sys
args = (sys.argv[1:])
print "combineCards.py ",
for arg in args: print " %s=%s "%(arg.replace(".txt",""),arg),
print

