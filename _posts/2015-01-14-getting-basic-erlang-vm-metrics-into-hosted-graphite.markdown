---
layout: post
categories: erlang, code, monitoring
date: 2015/01/14 14:05:00
title: Getting basic Erlang VM metrics into Hosted Graphite
---

I've been working with Erlang for the last quarter, and since we very much
eat our own monitoring dogfood at
<a href="https://www.hostedgraphite.com/">Hosted Graphite</a>, I've been
exporting application and VM metrics from my software.

<a href="https://github.com/Feuerlabs/exometer">Exometer</a> is a nicely
designed monitoring library for Erlang which includes easy export to Graphite,
so it's what I've been using.

The question of getting started with it seems to come up a bit on
<a href="http://erlangcentral.org/wiki/index.php/Erlang_IRC_Channel">#erlang</a>,
so I've packaged up a simple library application:

[basic_metrics](https://github.com/emauton/basic_metrics)

Rather than using exometer's static configuration options, we build
everything dynamically in the module. It's a little verbose as a result, but
clear and self-contained. The exports there should also provide examples
for your own application metrics.

This library depends upon and uses Fred Hébert's
<a href="https://github.com/ferd/recon">recon</a> for additional metrics
useful in production. See also
<a href="http://www.erlang-in-anger.com/">Erlang in Anger</a>.

The exometer integration is based on Brian Troutwine's notes in
<a href="http://goo.gl/Xo4fWi">Monitoring with Exometer: An Ongoing Love Story</a>.
For lots more detail on using exometer, see that article and the
[exometer documentation](https://github.com/Feuerlabs/exometer/blob/master/README.md).

Brian also has a great talk online covering some of the same
details: [video](https://www.youtube.com/watch?v=3LcED3KrGbI), [slides](http://www.slideshare.net/BrianTroutwine1/erlang-factory-berlin-monitoring-complex-systems-keeping-your-head-on-straight-in-a-hard-world).
