import argparse
import os
import subprocess
import sys

from . import settings
from .utils import cleanup, get_vhosts


# TODO: Move to a better location
def find_open_port(start_port=settings.VHOST_PROXY_PORT_START):
    vhosts = get_vhosts()
    ports_in_use = set(v.port for v in vhosts)
    port = start_port
    while port in ports_in_use:
        port += 1
    return port


# TODO: Move to a better location
def call_httpd(action, site=None, httpd=settings.HTTPD, identifier=settings.IDENTIFIER,
               pid_dir=settings.PID_DIR, proxy_vhost_name=settings.PROXY_VHOST_NAME,
               directory=settings.HTTPDMULTI_DIR, suffix=settings.VHOST_SUFFIX):
    """This calls httpd with the specified action.

        httpd -k {action}

    It operates either on all sites or just one site.

    When operating on all sites, the sites are located by looking in the
    ``vhost_dir`` for files with a .vhost extension. After the httpd
    action is run for each site, any sites that were already running but
    not found in ``vhost_dir`` are cleaned up (i.e., killed off).

    When operating on one site, specified via the ``site`` arg, the site
    is located by looking for ``{site}.vhost`` in ``vhost_dir``. No site
    cleanup is done in this case.

    """
    vhosts = get_vhosts(site=site, directory=directory, suffix=suffix)
    proxy_vhosts = []

    # PID files that won't be cleaned up.
    exclude_pid_files = set()

    # Run httpd action on either all sites or just ``site``.
    for vhost in vhosts:
        print('==', vhost.name)
        pid_file_name = '{identifier}-{name}.pid'.format(identifier=identifier, name=vhost.name)
        pid_file_path = os.path.join(pid_dir, pid_file_name)
        exclude_pid_files.add(pid_file_path)
        cmd = [
            httpd,
            '-D', 'httpdmulti',
            '-c', 'Include {path}'.format(path=vhost.path),
            '-c', 'PidFile {path}'.format(path=pid_file_path),
            '-c', 'CustomLog /var/log/httpd/{0.name}.access_log combined'.format(vhost),
            '-c', 'ErrorLog /var/log/httpd/{0.name}.error_log'.format(vhost),
            '-k', action,
        ]
        print(subprocess.list2cmdline(cmd))
        subprocess.call(cmd)

    # Rewrite proxy config file.
    # XXX: Maybe don't *always* do this.
    for vhost in get_vhosts():
        proxy_vhosts.append(str(vhost))
    with open(proxy_vhost_name, 'w') as fp:
        fp.write('# This is generated. Do not edit. See httpdmulti script.\n')
        fp.write('\n'.join(proxy_vhosts))
        fp.write('\n')

    # Reload the base Apache process's config so it picks up the new
    # proxy config.
    print('== main')
    cmd = [httpd, '-k', 'graceful']
    print(subprocess.list2cmdline(cmd))
    subprocess.call(cmd)

    if site is None:
        print('Cleaning up...')
        cleanup(exclude=exclude_pid_files)


def main(argv=None):

    def _find_open_port(args):
        print(find_open_port())

    def _call_httpd(args):
        call_httpd(action=args.action, site=args.site)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_port = subparsers.add_parser('find-port', help='Find an open port')
    parser_port.set_defaults(func=_find_open_port)

    actions = ('start', 'restart', 'graceful', 'graceful-stop', 'stop')
    for action in actions:
        action_subparser = subparsers.add_parser(action)
        action_subparser.set_defaults(func=_call_httpd, action=action)
        action_subparser.add_argument('-s', '--site', default=None)

    args = parser.parse_args(argv)

    try:
        func = args.func
    except AttributeError:
        parser.print_usage()
    else:
        return func(args)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
