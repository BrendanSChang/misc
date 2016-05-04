'''
This script is adapted from mininettcpbandwidthtest.py

It is meant to run the same TCP bandwidth allocation tests in an environment
with two logically isolated networks:

  HV1            HV2
 -----          -----
 | A | -- r1 -- | C |
 |   |          |   |
 | B | -- r2 -- | D |
 -----          -----

where HV1 and HV2 are two hypervisors hosting two VMs each. VMs A and B reside
on HV1 while VMs C and D reside on HV2. A and C form one logical network
connected by logical router r1 and B and D form the other logical network
connected by logical router r2.

Our test environment uses Openstack (Devstack) with OVN for L3 capabilities.
Therefore, we are effectively using a network deployed on OVS and OVN, where
logical routers are created as OVS switches.

The tests run iperf across each logical network simultaneously to gauge the
allocation of bandwidth when there is an even and uneven ratio of open TCP
connections in each network (specifically 1:1 and 10:1). We expect that the
allocations should follow in the same proportions.

Note that this assumes that the physical network should have the following
configuration:

HV1 -- sw1 -- sw2 -- HV2

where the link between the switches sw1 and sw2 is the bottleneck link.

'''

import sys
import paramiko
from threading import Thread


USER = "ubuntu"
KEY_PATH = "/home/ubuntu/devstack/id_rsa_test"


def run(ssh, host, server, out, parallel=1, window=True, time=True):
    cmd = "iperf -c " + server
    if parallel > 1:
        cmd += " -P %d" % parallel
    if window:
        cmd += " -w 500k"
    if time:
        cmd += " -t 150"
    stdin, stdout, stderr = ssh.exec_command(cmd);
    out[host] = stdout.read().splitlines()


def runTestRatio(sshs, hosts, servers, connectionRatio):
    print ("\n\tTesting {0}:{1} connection bandwidth"
              .format(
                  connectionRatio[0],
                  connectionRatio[1]
              )
          )

    output = {}
    threads = []
    for i in range(len(sshs)):
        t = Thread(
                target=run,
                args=(
                    sshs[i],
                    hosts[i],
                    servers[i],
                    output,
                    connectionRatio[i]
                )
            )
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Parse output.
    results = []
    for i in range(len(hosts)):
        h = hosts[i]
        print "\n\t\tHost: {0}".format(h)
        for line in output[h]:
            print "\t\t{0}".format(line)
        if connectionRatio[i] == 1:
            results.append(float(output[h][-1].strip().split()[6]))
        else:
            results.append(float(output[h][-1].strip().split()[5]))

    ratio = results[0]/results[1]
    print "\n\tThroughput ratio h1/h2: {0}".format(ratio)

    return ratio


def tcpBandwidthTest(iters=10):
    clients = ["10.0.0.3", "10.0.1.3"]
    servers= ["10.0.0.4", "10.0.1.4"]

    # Start iperf servers.
    # exec_command is non-blocking, so these do not need to be multithreaded.
    print "Starting iperf servers"
    server_sessions = []
    for s in servers:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(s, username=USER, key_filename=KEY_PATH)
        ssh.exec_command("iperf -s -w 500k")
        server_sessions.append(ssh)

    # Open the client sessions.
    print "Starting client sessions"
    client_sessions = []
    for c in clients:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(c, username=USER, key_filename=KEY_PATH)
        client_sessions.append(ssh)

    # Prime the connections.
    print "Priming for tests"
    for i in range(len(client_sessions)):
        client_sessions[i].exec_command("telnet " + servers[i] + " 5001")

    results = [[], [], [], []]
    ratios = [(1, 1), (10, 10), (10, 1), (1, 10)]
    for i in range(iters):
        print "\nRunning iteration {0}".format(i+1)
        for j in range(len(ratios)):
            results[j].append(
                           runTestRatio(
                               client_sessions, clients, servers, ratios[j]))

    print "\nAverage throughput ratios"
    for i in range(len(ratios)):
        print "\t{0}: {1}".format(ratios[i], sum(results[i])/len(results[i]))

    # Close connections.
    print "\nClosing connections"
    for c in client_sessions:
        c.close()

    for s in server_sessions:
        s.exec_command("pkill iperf")
        s.close()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print "Usage: python ./ovnbandwidthtest.py [number of trials]"
    else:
        print "Running tcpBandwidthTest"
        if len(sys.argv) == 1:
            tcpBandwidthTest()
        else:
            tcpBandwidthTest(int(sys.argv[1]))

