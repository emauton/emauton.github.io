#!/usr/bin/python

import json

graph = json.load(open('room.json'))

print "digraph {"

for key in graph.keys():
  print '"%s" [label="%s"]' % (key, graph[key]["name"])
  for label, link_key in graph[key]["link"].items():
    print '"%s" -> "%s" [label="%s"]' % (key, link_key, label)

print "}"
