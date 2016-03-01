import os
import signal
import subprocess
import sys
import time

from . import settings
from .vhostfile import VHostFile


def cleanup(exclude=()):
    """Kill httpdmulti processes."""
    httpd = settings.HTTPD
    identifier = settings.IDENTIFIER
    pid_dir = settings.PID_DIR
    for pid_file in os.listdir(pid_dir):
        pid_file = os.path.join(pid_dir, pid_file)
        if os.path.basename(pid_file).startswith(identifier) and pid_file not in exclude:
            killproc(pid_file, httpd)


def killproc(pid_file, binary, max_tries=10):
    """Kill process in ``pid_file``.

    Emulates the killproc /etc/init.d function. Sends a TERM signal to
    the process in ``pid_file``, assuming the binary matches the pid.
    Waits a maximum of ``max_tries`` seconds, then KILLs the process.

    """
    try:
        pid = int(open(pid_file).read().strip())
    except (TypeError, ValueError, OSError):
        return 1  # couldn't open the pid file

    # first send the SIGTERM signal
    if pid in pidof(binary):
        try_kill(pid, signal.SIGTERM)
        # give the process a little bit of time to clean up
        time.sleep(0.1)
    else:
        try_remove(pid_file)
        return 2  # the process wasn't running

    # now ensure we killed the process
    tries = 0
    while tries < max_tries:
        if pid in pidof(binary):
            time.sleep(1)
            tries += 1
        else:
            try_remove(pid_file)
            return 0

    # as a last resort...
    try_kill(pid, signal.SIGKILL)
    try_remove(pid_file)
    return 0


def pidof(binary):
    """Returns a set of pid numbers that are currently running the binary"""
    proc = subprocess.Popen(['pidof', binary], stdout=subprocess.PIPE)
    pids = proc.stdout.read().decode('utf-8').strip().split(' ')
    return set(int(pid) for pid in pids)


def try_kill(pid, signal_):
    """Send signal to process.

    Args:
        pid (int): Process ID
        signal_ (int|str): Signal ID or name

    """
    if isinstance(signal_, str):
        signal_ = getattr(signal, 'SIG{signal}'.format(signal=signal_.upper()))
    try:
        os.kill(pid, signal_)
        return True
    except OSError:
        return False


def try_remove(path):
    """Try to remove the file at path."""
    try:
        os.remove(path)
        return True
    except OSError:
        return False


def get_vhosts(site=None, directory=settings.VHOST_DIR, suffix=settings.VHOST_SUFFIX):
    vhosts = []
    port_vhost_map = {}

    if not os.path.exists(directory):
        raise NotADirectoryError(directory)

    for filename in os.listdir(directory):
        if not filename.endswith(suffix):
            continue

        vhost_path = os.path.join(directory, filename)
        vhost_file = VHostFile(path=vhost_path)

        if vhost_file.port in port_vhost_map:
            other_vhost_file = port_vhost_map[vhost_file.port]
            print(
                'Port collision in {vhost_file.path}; '
                '{other_vhost_file.path} already uses port {vhost_file.port}'
                .format(vhost_file=vhost_file, other_vhost_file=other_vhost_file),
                file=sys.stderr
            )

        port_vhost_map[vhost_file.port] = vhost_file
        vhosts.append(vhost_file)

    if site is not None:
        for vhost in vhosts:
            if site in (vhost.name, vhost.port):
                return [vhost]
        raise ValueError('Could not find vhost: %s' % site)

    return vhosts
