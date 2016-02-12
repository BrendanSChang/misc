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

import paramiko
from threading import Thread


KEY_PATH = "/home/ubuntu/devstack/id_rsa_test"

output = {}


def run(ssh, host, server, parallel=False):
    cmd = "iperf -c " + server
    if parallel:
        cmd += " -P 10"
    stdin, stdout, stderr = ssh.exec_command(cmd);
    output[host] = stdout.read().splitlines()


def tcpBandwidthTest():
    clients = ["172.24.4.3", "172.24.4.4"]
    servers_pub = ["172.24.4.5", "172.24.4.6"]
    servers_priv = ["10.0.2.6", "10.0.1.4"]

    # Start iperf servers.
    # exec_command is non-blocking, so these do not need to be multithreaded.
    print "Starting iperf servers"
    server_sessions = []
    for s in servers_pub:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(s, username="ubuntu", key_filename=KEY_PATH)
        ssh.exec_command("iperf -s")
        server_sessions.append(ssh)

    # Open the client sessions.
    print "Starting client sessions"
    client_sessions = []
    for c in clients:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(c, username="ubuntu", key_filename=KEY_PATH)
        client_sessions.append(ssh)

    # Prime the connections.
    print "Priming for tests"
    for i in range(len(client_sessions)):
        client_sessions[i].exec_command("telnet " + servers_priv[i] + " 5001")

    # Run 1:1 test.
    print "\nTesting 1:1 connection bandwidth"
    threads = []
    for i in range(len(client_sessions)):
        t = Thread(
                target=run,
                args=(client_sessions[i], clients[i], servers_priv[i])
            )
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Parse output.
    results = []
    for c in clients:
        print "\nHost: %s" % c
        for line in output[c]:
            print line
        results.append(float(output[c][-1].strip().split()[6]))
    print "\nThroughput ratio h1/h2: %f" % (results[0]/results[1])

    # Run 10:1 test.
    print "\nTesting 10:1 connection bandwidth"
    for i in range(len(client_sessions)):
        t = Thread(
                target=run,
                args=(
                    client_sessions[i],
                    clients[i],
                    servers_priv[i],
                    (i%2 == 0)
                )
            )
        threads[i] = t

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Parse output.
    # In this case, the output formats are slightly different so we treat each
    # case individually.
    print "\nHost: %s" % clients[0]
    for line in output[clients[0]]:
        print line
    results[0] = float(output[clients[0]][-1].strip().split()[5])
    
    print "\nHost: %s" % clients[1]
    for line in output[clients[1]]:
        print line
    results[1] = float(output[clients[1]][-1].strip().split()[6])
    print "\nThroughput ratio h1/h2: %f" % (results[0]/results[1])

    # Close connections.
    print "\nClosing connections"
    for c in client_sessions:
        c.close()

    for s in server_sessions:
        s.exec_command("pkill iperf")
        s.close()


if __name__ == "__main__":
    print "Running tcpBandwidthTest"
    tcpBandwidthTest()

