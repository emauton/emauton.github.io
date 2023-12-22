---
layout: post
categories: tldr, python, work
date: 2018/03/14 18:55:00
title: Python in private repos
---

At `$currentplace` we work mostly in Python. We do everything we can to
automate away busywork, so we like CI and the family of related tools and
ideas. We've put quite a bit of work into a smooth build/test/deploy cycle, and
along the way I've spent more time than I care to think of messing about with
Python packaging.

Last month, a [friend](http://pythonfangirl.blogspot.ie) asked how we manage
build dependencies, and my long answer eventually turned into a company blog
post:

[Developing and deploying Python in private repos](https://blog.hostedgraphite.com/2018/02/12/developing-and-deploying-python-in-private-repos/)

> At [Hosted Graphite](https://www.hostedgraphite.com/), most of our deployed services are written in [Python](https://www.python.org/), and run across a large installation of [Ubuntu Linux](https://www.ubuntu.com/) hosts.
>
> Unfortunately, the Python packaging and deployment ecosystem is something of a tire fire, particularly if your code is in private [Git](https://git-scm.com/) repositories. There are quite a few ways to do it, and not many of them work well.
>
> This post tells the story of what we have tried, where we are now, and what we recommend to programmers in a similar situation.
