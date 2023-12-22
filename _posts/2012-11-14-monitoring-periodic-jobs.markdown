---
layout: post
categories: sysadmin
date: 2012/11/14 00:00:00
title: Monitoring periodic jobs
---
Almost every production system has some set of jobs that run [periodically](http://www.stdlib.net/~colmmacc/2009/09/14/period-pain/). Typically these are analysis, reporting, backup or cleanup tasks that are best done outside the core 'always-on' components.

Often, these jobs are critical to the operation of the system. As such they require monitoring. Unfortunately, much periodic or cron job monitoring takes the form of email on success, failure, or other output.

This is a systems administration [anti-pattern](http://en.wikipedia.org/wiki/Anti-pattern). It's insidious, because it's essentially default operation for cron, and it's hard (locally) to see what harm one more periodic mail will do (globally).

As your systems scale, at best you have an expensive and slow logging mechanism; at worst, your team's personal mail filters become an integral part of your monitoring, or you miss a critical condition because mail delivery is wedged somewhere in your fleet.

In an interview for a [previous job](http://www.amazon.com/), I was pleased when my [prospective manager](http://ie.linkedin.com/in/richardarchbold) mentioned that his team's rules of engagement started as follows:

1. If you find something that's broken, fix it.
1. If it's emailing you, it's broken. See point 1.

I expect you'll find similar at most large sites. In [Google](http://www.google.com/) SRE, we try to eliminate email alert spam, with varying degrees of success. Our rules: exceptional conditions in automated systems should be signaled with

* **a page to a human** if immediate human attention is required;
* **a ticket/issue in a tracking system** if human attention is required but it can wait;
* **a log message or timeseries datapoint** if it's just something we might want to investigate or correlate against later.

So the usual informational emails from periodic jobs are log messages, and we export any other interesting information to our monitoring systems - e.g. 'last start', 'last success' timestamps, plus 'number of widgets processed'.

Once you have that data in your monitoring system, you can analyze, correlate, and alert to your heart's content. There are a lot of advantages here: instead of **N** emails from **N** servers, you can discard or count duplicates, alert on problems past a particular persistence or percentage threshold, or whatever makes most sense for your site. The model extends easily to e.g. "canary" jobs for new builds of the automation.

All of that said, at scale we tend to create batch processing jobs that run continuously as pipelines rather than cron jobs, particularly when dealing with multiple processing steps. They're easier to monitor, reason about, and plan capacity for. Also, you can and should eliminate certain periodic jobs altogether: e.g. code for fixing inconsistencies in data should really be built into the provider of that data.

One last note: if your periodic or other batch jobs and pipelines are worth monitoring, they're worth monitoring well. They deserve as much attention from the point of reliability engineering as any "serving path" binary. Typically this will mean redundancy both in their operation (i.e. don't run all your jobs in one basket) and their monitoring infrastructure (i.e. don't run all your probes from one basket).

Basket metaphors are optional, but good monitoring isn't.

*With thanks to [Dave O'Connor](http://blog.swearing.org) and [Niall Richard Murphy](http://www.heanet.ie/conferences/2011/speakers/id/31) for review and suggestions. I'd love to hear any thoughts from readers as well - drop me a mail.*
