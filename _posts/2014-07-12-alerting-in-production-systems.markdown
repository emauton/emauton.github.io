---
layout: post
categories: sysadmin
date: 2014/07/12 16:30:00
title: Alerting in production systems
---
Anyone who has been (or is going) through the wringer of a noisy pager rotation may enjoy this talk, delivered at [intercom.io](https://www.intercom.io) in Dublin on July 1st:

[Pager Bound: high-signal alerting in production systems](/talks/pager-bound-notes.pdf).

+ Good alerting is something that needs to be designed: organic growth tends to not go so well;
+ page, ticket or log: eliminate email alerts;
+ if we must be paged out of bed, it should be for something that really needs human attention;
+ we can only handle ~2 events well per shift;
+ service-level objectives are a really useful way to orient our alerting to customer experience & business priorities;
+ page on the **symptom** as it relates to our SLOs, not the **cause**.

Following [Rob Ewaschuk](http://rob.infinitepigeons.org/)'s [philosophy on alerting](https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/edit).
