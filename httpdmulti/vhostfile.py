import os
import pkg_resources
import re


LISTEN_RE = re.compile(r'^\s*Listen\s+(?P<port>\d+)\s*', re.I)
NAME_OR_ALIAS_RE = re.compile(r'^\s*(ServerName|ServerAlias)', re.I)


class VHostFile:

    """Encapsulates a vhost file.

    Args:
        path: Path to a valid vhost file with a Listen directive

    """

    def __init__(self, path):
        self.path = path
        self.name = os.path.splitext(os.path.basename(path))[0]
        self.port = None
        self.name_and_alias_directives = []
        self.ssl = True

        with open(self.path) as fp:
            lines = fp.read().splitlines()

        for line in lines:
            line = line.strip()

            match = LISTEN_RE.search(line)
            if match:
                self.port = int(match.group('port'))
                continue

            match = NAME_OR_ALIAS_RE.search(line)
            if match:
                self.name_and_alias_directives.append(line)
                continue

            match = line == '#nossl'
            if match:
                self.ssl = False
                continue

        if self.port is None:
            raise ValueError(
                '{0.path} does not specify a port number. Hint: Add a Listen directive.'
                .format(self)
            )

    def __str__(self):
        """Return <VirtualHost> section."""
        proxy_vhost_params = {
            'name': self.name,
            'port': self.port,
            'directives': '\n        '.join(self.name_and_alias_directives)
        }
        template = os.path.join('templates', 'ssl.conf' if self.ssl else 'nonssl.conf')
        template = pkg_resources.resource_filename('httpdmulti', template)
        with open(template) as fp:
            contents = fp.read()
        contents = contents.format(**proxy_vhost_params)
        return contents
