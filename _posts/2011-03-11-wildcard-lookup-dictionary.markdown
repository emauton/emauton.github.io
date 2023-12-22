---
layout: post
categories: code
date: 2011/03/11 00:00:00
title: Wildcard lookup dictionary
---
[A friend](http://www.apeofsteel.com/) suggested a fun little programming problem to me: efficiently matching scrabble tiles (including blanks or wildcards) to a dictionary of words.

he first thing I tried was a simple approach based on walking through a [trie](http://en.wikipedia.org/wiki/Trie) representation of the dictionary, and that did pretty well.

[Another friend](http://niallm.livejournal.com/) suggested that something using [prime-based set membership testing](http://www.stdlib.net/~colmmacc/2010/09/02/prime-and-proper/) might be fast. That's what my eventual solution is based on, and the proof of concept is reasonably snappy.

Code:

* [wild_dictionary](/code/wild_dictionary.py)
* [wild_server](/code/wild_server.py)
