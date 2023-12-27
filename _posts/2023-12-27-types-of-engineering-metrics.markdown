---
layout: post
title: Types of engineering metrics
date: 2023/12/27 18:30:00
categories: thoughts work
---

I've found myself expressing from time to time that there are different types
or "levels" of metrics we can use in and around engineering, and that each has
different requirements.

An incomplete set of examples that I feel are most relevant to **engineers**
follows. Note that as we move "up" levels of abstraction here, the value of the
metrics is increasingly about the conversation that "pushing on the numbers"
can stimulate.

See [Will Larson's
notes](https://lethain.com/measuring-engineering-organizations/) for more
discussion and a broader taxonomy, mostly focused on "investment-level" metrics
below.

### 1. Operations-level metrics

Emitted by our software services: the stuff we put on service dashboards,
representing workloads and how they're doing. **May** have alerting attached,
but [probably
shouldn't](https://emauton.org/2014/07/12/alerting-in-production-systems/).

Precision is king, here: we want each metric to have a clear meaning and
implications. "Muddiness" or subtlety is the enemy. A good example of the
latter is [Linux load
average](https://www.brendangregg.com/blog/2017-08-08/linux-load-averages.html).
_Caveat operator_.

### 2. Service-level metrics

Emitted by our services and the infrastructure around them (for example,
[synthetic probes](https://en.wikipedia.org/wiki/Synthetic_monitoring)). Often
used as
[service level indicators](https://en.wikipedia.org/wiki/Service_level_indicator)
to understand customer experience and [user
journeys](https://en.wikipedia.org/wiki/User_journey); may also include
adoption and capacity metrics. **Often** have alerting attached.

While we want to _define_ these precisely - see for example the [Art of SLOs
workshop](https://sre.google/resources/practices-and-processes/art-of-slos/) -
it's OK for there to be uncertainties, subtleties, and warnings attached. Often
we have to choose proxies for customer experience, or it's prohibitively
expensive to measure some important part of a user journey.

So we're fine with service-level metrics needing to have an explanation
attached: some bullet points, or a few paragraphs.

### 3. Investment-level metrics

Gathered in lots of different ways, often across a broad swath of systems and
services. Used to drive or inform a specific large-scale investment by a group
or organization: a difficult migration, the health of some org-level process.
As likely to be delivered by a more traditional
[BI](https://en.wikipedia.org/wiki/Business_intelligence) system as by Datadog
dashboards. **Rarely** have alerting attached.

Again, we want a reasonably clear definition of a metric like this. However, it
can be even less precise than a service-level metric, and have more caveats and
edge-cases attached. It's almost always a proxy - often a "trailing edge"
indicator - for some important effort we're trying to drive across the
business.

It's OK for a metric like this to have a page or a whole document explaining
it, as long as we agree it provides a useful "needle we can move" over time.
