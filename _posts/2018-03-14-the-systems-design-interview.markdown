---
layout: post
categories: tldr, interviewing, advice 
date: 2018/03/14 19:40:00
title: The systems design interview
---
This post describes (roughly) the aims and format of typical systems design interviews, and gives guidance on how to approach them.

The intended audience is systems and software engineers who are less familiar with this style of interview.

*   [Context](#context)
    *   [The company](#the-company)
    *   [The interviewer](#the-interviewer)
    *   [The candidate](#the-candidate)
*   [Guidance](#guidance)
    *   [Format](#format)
    *   [Communication](#communication)
    *   [Decomposition](#decomposition)
    *   [Estimation](#estimation)
    *   [Elements](#elements)
    *   [Mocks](#mocks)
    *   [Psychology](#psychology)

# Context

## The company

Many companies - large and small - include a "systems design" slot in their
on-site interviews, where the candidate is asked to design a relatively
large-scale system - typically involving multiple cooperating machines and
services.

The aim of the company in these interviews is to gauge the candidate's
experience with and intuition for the design of distributed systems.

It's also a good opportunity to see how well the candidate communicates ideas,
and what working with them would be like at a design level.

## The interviewer

The interviewer shares the company's aims, more or less, and needs to:

*   set the scene, laying out the systems design scenario to be covered;
*   guide the interview, clarifying things and giving hints where necessary;
*   inflect the direction the discussion takes depending on the candidate's
    experience;
*   ask questions and dig into concrete elements of the design to make sure the
    candidate 
    1.  knows what they're talking about and
    1.  can reason about and defend specific points, rather than talking
        "abstractly" throughout the interview;
*   assess the candidate's domain knowledge, problem-solving ability,
    communications style, and culture fit.

Taken together, this is a fairly tall order, so usually interviewers in this
area have significant interviewing experience.

## The candidate

Your aim is obviously to get an offer. ;o) In this case, that means you need
to:

*   demonstrate good communication and problem solving skills;
*   show that you can apply any knowledge you have that is relevant to the
    problem domain and/or navigate the unfamiliar parts;
*   dig into and solve design issues appropriate to your experience level.

Think of yourself throughout as a "future colleague" - taking a collaborative
approach to the discussion.

# Guidance

## Format

Typically an interview like this comprises a single design question followed by
a long discussion. Roughly speaking, you can expect things to go like this:

1.  The interviewer sets up the scenario. Some examples:
    *   a popular service like [Gmail](https://gmail.com);
    *   a [distributed in-memory hashtable](https://en.wikipedia.org/wiki/Distributed_hash_table);
    *   a content delivery network like [AWS Cloudfront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html);
    *   a [logs analysis](https://en.wikipedia.org/wiki/Log_analysis) pipeline.
2.  The interviewer gives some starting data to work from: user numbers, data
    sizes, that sort of thing. It's important to note that this will be
    incomplete. Do not try to work from the initial conditions in splendid
    isolation. Instead,
3.  You clarify the scope of the problem, asking for any further data you feel
    you might need to start on the design.
4.  You decompose the problem into sub-problems.
5.  You start tackling one, again asking for any data not already provided, or
    deriving new data from what you've been given.
6.  The interviewer digs into concrete details, asks for clarifications, and
    provides hints or further information where necessary.
7.  Go to step 4 and repeat until time runs out. :o)

## Communication

Overcommunicate.

The interviewer wants to understand how you think, so staring at the whiteboard
for 5 minutes is not very useful to them. If you usually work in silence,
practice on paper before the interview, speaking aloud about what you are
doing.

If there's a whiteboard - there most probably is - use it for everything. If
there isn't, ask for paper. Write down design parameters given to you, or that
you derive. Draw system diagrams, data flow diagrams, API specifications. It
helps clarify your thinking, encourages useful decomposition of problems, and
makes it easier for the interviewer to follow and assess you.

Ask lots of questions. You are not expected to be able to just fly this without
interacting with your interviewer: treat them as a peer with whom you are
working through the design. If you are making an assumption (that you're aware
of), state it clearly and ask the interviewer if they'd like you to modify it.

## Decomposition

Don't attack the problem as a monolith. As soon as you've clarified the initial
design parameters with the interviewer, think about the "relatively
independent" elements of a system that could meet the design goals and sketch
them out on the board.

In large-scale designs, this often suggests appropriate (initial) division of
the solution into
[services](https://en.wikipedia.org/wiki/Service-oriented_architecture) which
can be designed independently, deriving their design parameters from those of
the overall problem.

Having sketched something, look over it critically and discuss it with your
interviewer: is there any major part of the original requirements that you
haven't addressed? Anything more loosely or tightly coupled than it should be?

Then, you can ask your interviewer which element they'd like you to tackle
first.

## Estimation

One of the things your interviewer will be looking for is how you handle
concrete elements of the design. This is often about e.g. how many machines you
are going to need for some sub-service given the design parameters, or what
volume of data you expect to have in flight or at rest at any given time.

So you need to be ready to make estimates and do some simple arithmetic. If
it's not something you've often done, try taking "[latency numbers every
programmer should
know](http://colin-scott.github.io/blog/2012/12/24/latency-trends/)" and
applying them to a problem or system you know well.  See how the theory
compares to your practical experience. :o)

You might enjoy working through "[computers are
fast](https://computers-are-fast.github.io/)" by Julia Evans and Kamal Marhubi
to sharpen your intuitions.

Back-of-the-envelope calculation like this helps constrain the solution space
and gives you a clearer idea of what might work. Note that an estimate can be
quite broad and remain useful: your objective is to determine "is this even
practical" rather than get (nearly) exact numbers.

## Elements

There are some fundamental things we need to keep in mind when designing a
system distributed across multiple machines, and becoming familiar with them
should help you navigate the problem domain.

Jeff Hodges' [notes on distributed systems for young
bloods](https://www.somethingsimilar.com/2013/01/14/notes-on-distributed-systems-for-young-bloods/)
covers many of these and is worth internalizing. My own talk "[Designing for
Brobdingnag](http://emauton.org/2014/07/15/designing-for-brobdingnag/)" also
looks at building blocks and patterns in large-scale systems design and
includes a set of further resources on the last page of notes.

This is a big area, but in order to tackle a large-scale design it will help to
have at least some idea of your options for:

*   Traffic management / request [load
    balancing](https://en.wikipedia.org/wiki/Load_balancing_(computing)) and
    [service discovery](https://en.wikipedia.org/wiki/Service_discovery);
*   [Sharding](https://en.wikipedia.org/wiki/Shard_(database_architecture)) of
    state, including
    [consistency](https://aphyr.com/posts/313-strong-consistency-models)
    models;
*   [Replication](https://en.wikipedia.org/wiki/Replication_(computing)) and
    [high availability](https://en.wikipedia.org/wiki/High_availability)
    strategies.

## Mocks

If you have access to someone who runs interviews like this (and doesn't have a
conflict of interest), ask them to help you by running a mock interview & then
writing up

*   feedback as though for an interview process and
*   specific notes you can use to improve.
 
## Psychology

Junior candidates sometimes get wigged out by these interviews and lock up. The
failure mode here is expecting too much of yourself: the interviewer knows your
experience and background (they've read your CV), so will already have a good
idea of the level they can expect. It's their job to appropriately assess the
discussion relative to your experience. So do your best, make a good stab at
the problem (see "Decomposition" above), try to have a good time, and above all
don't compare yourself to an "ideal, more experienced you".

Conversely, if you're a senior candidate with relevant domain knowledge, the
interviewer is justified in expecting a lot out of the discussion, and you may
find them digging pretty deep. Don't be shy about going into excruciating
design details if that's where the interviewer wants to go. They're trying to
assess your limits, and to get into concrete specifics: a sometime problem with
senior candidates is that they adeptly handwave these. :o)
