---
layout: post
categories: sysadmin
date: 2013/08/27 00:00:00
title: Keeping a lab book
---

Many years ago, a [friend](http://www.stdlib.net/~colmmacc/) mentioned that he kept a [lab book](http://en.wikipedia.org/wiki/Lab_notebook) for systems work, so I started to do the same.

I've found it works well for less-defined, experimental or tentative work - for example performance optimizations or exploring new technology; it keeps state organized and external to my poor stinging brain, and leaves me with documentation (as well as tips and tricks) to look back on. Being explicit about expectations, hypotheses, and what variables you're changing as you work is a useful discipline.

Also, it's a good idea to keep a record of how you produced those fascinating results: perhaps you (or someone else) would like to repeat your experiment on a different binary or configuration; perhaps you'll need the raw data in the flamewar when you post your results. ;o)

Here's the template I use. If you like keeping notes as you hypothesize, measure, rinse and repeat, then you might find it useful. Maintaining it in a wiki works well. Also, I like to use collapsible sections so I can record but later hide excessive detail.

**Lab book**: Title of this experiment/lab session.

**Dates**: The period you ran the experiment over.

**Team members**: Who was involved.

**Purpose**
> The background of your experiment; what you intend to find out; any hypotheses you already have; references to supporting documentation or experiments.

**Materials**
> What you're using to produce your results: for example, the version of a binary or the revision number of a configuration you're experimenting with, plus links to any supporting scripts or other tools you're using.

**Procedure and data**
> What you did, how you did it, and what you found out. Consider pasting in commandlines and results. Write for your reader (who may be your future self) - be reasonably detailed and thorough. If you have raw data dumps, perhaps link them, and just include a few representative lines here. Link in any interesting graphs.

**Analysis**
> What you think it all means, and what actions you're going to take as a result of your experiment. Do you need to open some bugs? Do you need to do some more experiments?
