#!/usr/bin/env python3

"""
auto send password when login on the server through the gateway
"""
import pexpect, subprocess
import struct, fcntl, sys, signal
import termios


def sigwinch_handler(pinstance):
    """
    adjust window size when get winch signal
    """
    def handler(sig, data):
        s = struct.pack("HHHH", 0, 0, 0, 0)
        a = struct.unpack("hhhh", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
        pinstance.setwinsize(a[0], a[1])
    return handler

def login(host):
    """
    login public host via gateway host, then change user
    """


    """ change this settings to make use.  """
    gateway_user = "lonli"
    gateway_ip = "127.0.0.1"
    gateway_port = "22"
    gateway_key = "/home/lonli/.ssh/id_rsa"

    """ change abbove settings to make use.  """


    if host:
        try:
            subprocess.check_output(["ssh", "-p", gateway_port, "-i", gateway_key,
                "{0}@{1}".format(gateway_user, gateway_ip), "grep {0} ~/.ssh/config".format(host)])
        except subprocess.CalledProcessError as e:
            print("'{0}' does not exists in the configuratian of the gateway!".format(host), file=sys.stderr)
            return

    to_gateway = "ssh -p {0} -i {1} {2}@{3}".format(gateway_port, gateway_key, gateway_user, gateway_ip)
    ssh = pexpect.spawn(to_gateway)
    if host:

    
        """ change this settings to make use.  """
        exps = [
            ("lonli@arch", 'echo -n "Enter diretory : " && read && [ -d "${REPLY}" ] && cd ${REPLY}'),
            ("Enter diretory : ", "/tmp"),
            ("/tmp", "pwd"),
        ]
        """ change abbove session to make use.  """


        for p, s in exps:
            # print("expect : {0}, then send : {1}".format(p, s))
            ssh.expect(p)
            ssh.sendline(s)
    winch_handler = sigwinch_handler(ssh)
    signal.signal(signal.SIGWINCH, winch_handler)
    winch_handler(None, None)
    ssh.interact()

if "__main__" == __name__:
    login(sys.argv[1] if len(sys.argv) > 1 else None) # just to gateway if no host.
