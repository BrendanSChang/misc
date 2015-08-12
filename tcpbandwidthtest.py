#!/usr/bin/python

"""
Test the hypothesis that TCP allocates bandwidth linearly with respect
to the number of connections. This test treats h1-h3 and h2-h4 as
separate tenants in this network. We use iperf to compare the bandwidth
of each connection, first with a single connection running on each
tenant and then with a 10-to-1 connection ratio.

We construct a network of 4 hosts and 2 switches, connected as follows:

h1                h3
  \             /
    - s1 -- s2 -
  /             \
h2                h4

"""

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.topo import Topo
from mininet.log import lg
from mininet.util import pmonitor, quietRun
# from mininet.link import TCLink
# from functools import partial

import sys
flush = sys.stdout.flush

class ThroughputTestTopo(Topo):
    "Topology for two switches, each with two hosts."

    def __init__(self):
        # Initialize topology.
        Topo.__init__(self)

        # Add hosts.
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        h4 = self.addHost("h4")

        # Add switches.
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        # Add links.
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(s1, s2)

def tcpBandwidthTest():
    "Test TCP throughput with different numbers of connections."

    topo = ThroughputTestTopo()

    # Select TCP Reno
    # (This is copied over from the linearbandwidth.py example, I don't
    # know if it applies here.)
    output = quietRun("sysctl -w net.ipv4.tcp_congestion_control=reno")
    assert "reno" in output

    Switch = OVSKernelSwitch

    # Currently there is no link delay introduced.
    # link = partial(TCLink, delay='1ms')
    net = Mininet(topo=topo, switch=Switch,
        controller=Controller, waitConnected=True)  #, link=link )
    net.start()

    print "*** testing basic connectivity"
    net.ping([net.get("h1"), net.get("h3")])
    net.ping([net.get("h2"), net.get("h4")])

    print "\n*** priming for tests"
    # Try to prime the pump to reduce PACKET_INs during test
    # since the reference controller is reactive
    net.get("h1").cmd("telnet", net.get("h3").IP(), "5001")
    net.get("h2").cmd("telnet", net.get("h4").IP(), "5001")

    # Set up iperf servers.
    net.get("h3").popen("iperf -s")
    net.get("h4").popen("iperf -s")

    popens = {}
    results = []

    print "\n*** testing 1:1 connection bandwidth"
    popens[net.get("h1")] = net.get("h1").popen(
            "iperf -c %s" % net.get("h3").IP())
    popens[net.get("h2")] = net.get("h2").popen(
            "iperf -c %s" % net.get("h4").IP())

    results.append({})
    for host, line in pmonitor(popens):
        if host:
            print "<%s>: %s" % (host.name, line.strip())
            results[0][host.name] = line.strip()
    # Find the ratio of the reported bandwidths.
    results[0]["ratio"] = (float(results[0]["h1"].split()[6]) /
        float(results[0]["h2"].split()[6]))

    print "\n*** testing 10:1 connection bandwidth"
    popens[net.get("h1")] = net.get("h1").popen(
            "iperf -c %s -P 10" % net.get("h3").IP())
    popens[net.get("h2")] = net.get("h2").popen(
            "iperf -c %s" % net.get("h4").IP())

    results.append({})
    for host, line in pmonitor(popens):
        if host:
            print "<%s>: %s" % (host.name, line.strip())
            results[1][host.name] = line.strip()
    # The units and format of the h1 response is slightly different from
    # the case above.
    results[1]["ratio"] = (1000 * float(results[1]["h1"].split()[5]) /
        float(results[1]["h2"].split()[6]))

    net.stop()

    print "\n*** results"
    print "1:1 connection throughput:"
    print "      [ ID] Interval       Transfer     Bandwidth"
    print "<h1>: %s" % results[0]["h1"]
    print "<h2>: %s" % results[0]["h2"]
    print "Throughput ratio h1/h2: %f" % results[0]["ratio"]
    print "\n10:1 connection throughput:"
    print "      [ ID] Interval       Transfer     Bandwidth"
    print "<h1>: %s" % results[1]["h1"]
    print "<h2>: %s" % results[1]["h2"]
    print "Throughput ratio h1/h2: %f" % results[1]["ratio"]

if __name__ == '__main__':
    lg.setLogLevel('info')
    print "*** Running tcpBandwidthTest"
    tcpBandwidthTest()
