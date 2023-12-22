---
layout: post
categories: work, operations, process
date: 2021/8/31 11:45:00
title: Oncall compensation structures
---

The subject of compensation for [developers
oncall](https://johnbarton.co/posts/developers-on-call) comes up from time to
time.

It can be difficult to find public examples of compensation structures to use.

These notes are from a quick survey of existing stuff I could find via
discussions in opsy chats, the Internet, and direct questions to my network.

## Asking questions

First, for those on the job hunt, a list of questions to ask about oncall, gathered from the [Irish Tech Community](https://irishtechcommunity.com/):

*   Do you compensate being oncall (i.e. value the stress) or just when you get called (bullshit) or never (warning sign)?
*   What is the response time? Is it 5 mins (no life), 15-30 mins (some life, depending on if you have kids), or an hour (you can go to the cinema with your laptop)?
*   What percentage of your time is operations, when you’re oncall?
*   How many people are in the rotation? If < 6, is there a realistic plan in place to fix that?
    *   You need at least 4 people for a reasonable shift pattern, plus one for maintenance (e.g. holidays) + one for emergency (e.g. attrition).
*   Is there one person oncall in a shift or is it a primary/secondary kind of thing?

## Notes from the 'net

Second, some posts that cover oncall compensation in various detail: 

*   <https://www.atlassian.com/incident-management/on-call/on-call-pay>
    *   Kind of marketing white-paper stuff for OpsGenie which seems to have some support for oncall comp calculations. But some good notes on comp structures.
*   <https://sre.google/sre-book/being-on-call/#compensation>
    *   Google’s (short) take on it in the SRE book.
*   <https://johnbarton.co/posts/developers-on-call>
    *   Has a good section on comp with philosophy as well as basic structure ideas.
*   <https://copyconstruct.medium.com/on-call-b0bd8c5ea4e0>
    *   Long, philosophical, no comp structure details but good thinking around why it should be comp’d in “Toward a more sustainable and humane on-call” section.

## Example structures

Finally, a set of example compensation structures from various companies.

A fintech company in south America:

*   If you are oncall but not working, +33% of equivalent hourly rate.
*   Paged and start working, +300% of your hourly for that period.
*   Some more extras for nights or weekends.
*   They just exported data from Pagerduty: time working was acknowledgement → resolution.
*   People would not resolve until they were finished any report or comms work that had to be done out-of-hours.
*   This apparently was just how labour laws in that country apply - works the same way for doctors.

A medium-sized SaaS company operating across US / EU:

*   Time off as standard if you actually get paged out of hours: ½ day per four hours or part thereof in responding.
*   Comp at 25% for oncall time regardless.
*   Comp → 100% for the time you’re responding.
*   Because of how their shift structure works, this all tends to amount to roughly a 10% lift in salary, plus time to recover.

A large multinational:

*   Some teams have business-hours only shifts for internal infra APIs.
*   Other teams have customer-facing services and much stricter on-call.
*   Those latter get paid per shift, get a mifi, and get time off etc.
*   ^ didn’t get exact comp structure here.

Another large multinational:

*   Three tiers of oncall, depending on pager SLA.
*   Tier 1: >= 99.9% availability SLA, 5min pager response SLA.
    *   Comp paid at ⅔ for outside hours
    *   That is, outside business hours accrue hours at 2h for every 3h oncall.
*   Tier 2: >= 99.9% availability SLA, > 5min but <= 15min pager response SLA.
    *   Comp paid at ⅓ for outside hours.
    *   That is, outside business hours accrue hours at 1h for every 3h oncall.
*   Tier 3: everything else, not comped.
*   Mon-Fri comp paid outside 9-6 core hours. Sat & Sun all comped.
*   So if you were oncall 6am-6pm Mon-Sun that’d be like
*   3 x 5h for Mon-Fri
*   2 x 12h for Sat-Sun
*   So 39h compensatable, converting into pay as 13h at tier 2 or 26h tier 1.
*   You could take this as either time in lieu (at 8h/day) or cash (pro-rated to salary).

A medium-sized SaaS multinational:

*   Shifts are either weekday or weekend.
*   Pay according to 60h week (hourly equiv. from salary) if weekday shift.
*   According to 40h week + 24h if weekend shift.
*   Payout doubles if schedule includes public/bank holidays.
*   Contact there mentioned this was very similar to structure in last job, another similar-sized SaaS.

[Intercom's oncall implementation](https://www.intercom.com/blog/rapid-response-how-we-developed-an-on-call-team-at-intercom/):

*   Former Ruby monolith sharded out over the last few years into services. Heavy on AWS and [running less software](https://www.intercom.com/blog/run-less-software/).
*   An unusual structure, but interesting: specifically because they have modified their approach to avoid having “too many people/teams oncall”.
*   Virtual team, volunteers from any team in the org.
*   6-month rotations in that virtual team, having taken a handful of shifts.
*   Oncall went from being spread across more than 30 engineers to just 6 or 7.
*   “We put in place a level of compensation that we were happy with for taking a week’s worth of on call shifts.”
    *   Not sure of precise structure, presumably a bonus per week oncall.

Criteo, medium-sized Adtech HQ’d in France. This is from a [3y old Reddit thread](https://www.reddit.com/r/devops/comments/72lj1q/what_is_your_company_oncall_compensation_model/):

*   SREs are oncall. Pager response time is 30 minutes. (!)
*   They are paid for oncall for nights/weekends etc. Exact comp unspecified.
*   If you are paged, you get comped time as well in exchange (½ day at least).
*   Internet & phone bill reimbursed for oncall engineers.
*   If you work during the night, you have to stay home until you get 11h consecutive rest (French law).
