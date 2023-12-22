---
layout: post
categories: erlang
date: 2015/05/06 00:00:00
title: Distributed Erlang
---
This document is a short guide to the structure and internals of the
[Erlang/OTP](https://github.com/erlang/otp) distributed messaging facility.

The intended audience is Erlang programmers with experience using [distributed
Erlang](http://www.erlang.org/doc/reference_manual/distributed.html) and an
interest in its implementation.

Overview
--------

The protocol Erlang nodes use to communicate is described between the
[distribution
protocol](http://www.erlang.org/doc/apps/erts/erl_dist_protocol.html) and
[external term format](http://www.erlang.org/doc/apps/erts/erl_ext_dist.html)
sections of [the ERTS user
guide](http://www.erlang.org/doc/apps/erts/users_guide.html).

The implementation is supported by features of the system applications,
libraries, and the [BEAM
emulator](http://www.erlang-factory.com/upload/presentations/708/HitchhikersTouroftheBEAM.pdf).

Sections below describe process structure, flow of control, and points of
contact between subsystems, with links to the source code at [a recent commit
hash on the `maint`
branch](https://github.com/erlang/otp/tree/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f).

Transport
---------

The distributed protocol typically uses a single TCP socket over IPv4. The
protocol used can be specified with the
[proto\_dist](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/net_kernel.erl#L1309)
argument to the VM, and is respected by the [net\_kernel
module](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/net_kernel.erl)
when it sets up either its own distributed listener or connects to remote
nodes.

To find the protocol modules specified by `proto_dist`, add `_dist.erl` in the
[Erlang/OTP source](https://github.com/erlang/otp/).

* [inet\_tcp](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/inet_tcp_dist.erl),
  the default; handles TCP streams with IPv4 addressing.
* [inet6\_tcp](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/inet6_tcp_dist.erl),
  an undocumented module prepared to handle TCP with IPv6 addressing. In
  principle there's no reason `inet_tcp` could not be protocol-agnostic in this
  respect, but for now programmers setting up nodes on IPv6 networks need to
  specify `-proto_dist inet6_tcp`.
* [inet\_tls](), connection using TLS to verify clients and encrypt internode
  traffic. Setup is detailed in the [Secure Socket Layer User's
  Guide](http://www.erlang.org/doc/apps/ssl/ssl_distribution.html). Note that
  particularly within Erlang's usual LAN deployment context, other options such
  as an [internode VPN](http://luca.ntop.org/n2n.pdf) might be more
  convenient.

As well as transport negotation, the protocol modules handle node registration
and lookup, so a particular transport could use something other than
[epmd](http://www.erlang.org/doc/man/epmd.html) if required.

Discovery
---------

Before applications on the network can talk, they need to locate one another
with some form of [service
discovery](http://en.wikipedia.org/wiki/Service_discovery). Erlang/OTP relies
on both [DNS](http://en.wikipedia.org/wiki/Domain_Name_System) and a
[portmap](http://en.wikipedia.org/wiki/Portmap)-style service called
[epmd](http://www.erlang.org/doc/man/epmd.html) (for "Erlang Port Mapping
Daemon").

`epmd` is a simple standalone daemon [written in
C](https://github.com/erlang/otp/tree/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/epmd) which listens at port
`4369` on a host running Erlang nodes. It implements a simple binary protocol to
register and look up `(Erlang node, TCP port)` mappings. See the links from
the [overview](#overview) above for details.

The Erlang system applications interact with `epmd` via the [erl\_epmd
module](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/erl_epmd.erl).

Notes:

* An Erlang node starts `epmd` automatically if it is not already running on
  the host at startup. This is [built
  in](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/etc/common/erlexec.c#L1192)
  to the low-level `erlexec` C program used by `erl` to invoke the emulator.
* Each node registering itself with `epmd` maintains its open TCP connection
  after sending `ALIVE2_REQ`; `epmd` deregisters the node when that connection
  is closed or lost.
* The `Extra` field of `ALIVE2_REQ` is faithfully stored and echoed back by
  `epmd` in `PORT2_RESP` responses, but is not currently used.
* Both `Name` and `Extra` can have a maximum size of
  [MAXSYMLEN](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/epmd/src/epmd_int.h#L250).

System
------

Setup and maintenance of distributed Erlang listening and connection is handled
by the [kernel application](http://erlang.org/doc/man/kernel_app.html)'s
[net\_kernel](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/net_kernel.erl)
module.

The process hierarchy:

<img alt="A diagram showing the net\_sup process supervised by kernel\_sup and
in turn supervising net\_kernel and its supporting processes."
src="/img/net_sup_and_children.png" width="400" />

`net_kernel` is started by the [net\_sup
supervisor](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/erl_distribution.erl#L35),
if it can find `-sname` or `-name` arguments on the `erl` commandline. Started
alongside it are
[erl\_epmd](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/erl_epmd.erl)
and [auth](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/auth.erl).
All three are `gen_servers`. The latter two respectively handle maintaining a
connection to `epmd`, as discussed above, and
[cookie](http://www.erlang.org/doc/reference_manual/distributed.html)
management (including the backend for `erlang:{set,get}_cookie`).

`net_kernel` immediately sets up a listening socket for the node by invoking
`Mod:listen/1` for the `proto_dist` module (by default
[inet\_tcp\_dist](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/inet_tcp_dist.erl)).
Note the facility to [supply listen
options](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/inet_tcp_dist.erl#L105)
for distributed Erlang sockets via the commandline.

After registering this as the node's distribution socket with the emulator (via
`erlang:setnode/2`, see below), `net_kernel` invokes `Mod:accept/1`, e.g. [for
inet\_tcp\_dist](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/inet_tcp_dist.erl#L126).
By default, this creates the `listener` process in the diagram above, running
`inet_tcp_dist:accept_loop/2`.

After this, there are two cases for `net_kernel` to deal with:

1. An incoming connection from another node.
   This
   [triggers](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/net_kernel.erl#L601)
   a call to the proto\_dist `Mod:accept_connection/5` which in turn starts one of
   the `connectionN` processes in the diagram above and [performs the distributed
   Erlang
   handshake](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/inet_tcp_dist.erl#L172)
   using the
   [dist\_util](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/dist_util.erl)
   module. On a successful handshake, `dist_util:do_setnode/1` registers the newly
   connected node with the emulator (via `erlang:setnode/3`, see below).

1. An outgoing connection to another node.
   This is handled by `net_kernel:connect/1`, which is called transparently by the
   `d*` functions in the
   [erlang](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/preloaded/src/erlang.erl#L2850)
   module (see the emulator section below). `net_kernel:connect/1` does much the
   same work as for an incoming connection (including setting up one of the
   `connectionN` processes in the diagram above), but via `Mod:setup/5` in the
   `proto_dist` module.

Finally, note that `net_kernel` can also be
[invoked](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/lib/kernel/src/net_kernel.erl#L1114)
as part of the
[erlang:spawn/4](http://www.erlang.org/doc/man/erlang.html#spawn-4) to spawn
processes on a foreign node.

Emulator
--------

While the Erlang system, via `net_kernel`, handles connection setup, the nuts
and bolts of the distributed Erlang protocol are handled by the emulator
itself. The API it exposes is small, however, and mostly found in the built-in
functions registered by
[dist.c](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/emulator/beam/dist.c#L2492).

First up are the `setnode` BIFs. These register either the local node
(`erlang:setnode/2`) or remote nodes (`erlang:setnode/3`) in the emulator's
[node
tables](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/emulator/beam/erl_node_tables.h#L23).
There are separate distribution tables for visible and hidden nodes; this is
how the `-hidden` node commandline argument is used. The `erlang:nodes/0` BIF
reads these tables directly.

BIFs like
[erlang:send/2](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/emulator/beam/bif.c#L2156)
look up the node tables and call into the [`erts_dsig_*`
functions](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/emulator/beam/dist.h#L111)
to handle distributed messaging. If a connection is necessary, these can trap
back to e.g.
[erlang:dsend/2](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/preloaded/src/erlang.erl#L2901)
to invoke connection setup via `net_kernel`.

Once connections are established,
[erts\_dsig\_send\_\*](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/emulator/beam/dist.c#L712)
are used to do the actual messaging. Message encoding in the
[external term format](http://www.erlang.org/doc/apps/erts/erl_ext_dist.html)
is handled by
[dsig\_send](https://github.com/erlang/otp/blob/ff1e0b2fe44a347670a5d72c45c061fefa6abc7f/erts/emulator/beam/dist.c#L1697).

Updates
-------

Please send any comments or suggestions for this document to <a href="mailto:cian@emauton.org">cian@emauton.org</a>.
