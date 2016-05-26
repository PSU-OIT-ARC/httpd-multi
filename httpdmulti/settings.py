import os

# Path to the httpd executable.
HTTPD = '/usr/sbin/httpd'

# Path to the root vhost directory.
VHOST_DIR = '/etc/httpd/vhost.d'

# Path to the directory containing httpdmulti config files.
HTTPDMULTI_DIR = os.path.join(VHOST_DIR, 'httpdmulti.d')

# Path to the directory containing the main (non-httpdmulti) config
# files. This is where the httpdmulti proxy config file will be saved
# to (see PROXY_VHOST_NAME below).
MAIN_DIR = os.path.join(VHOST_DIR, 'main.d')

# The suffix on the files we want to parse to create additional
# instances of Apache for.
VHOST_SUFFIX = '.vhost'

# A name to use for pid files so we know which ones belong to us.
IDENTIFIER = 'httpdmulti'

# Where to store PID files.
PID_DIR = '/var/run/httpd'

# Path to the generated proxy config file. It will contain a bunch of
# <VirtualHost>s that proxy to the individual Apache instances started
# by httpdmulti. This file needs to be included from the main Apache
# config file.
PROXY_VHOST_NAME = os.path.join(MAIN_DIR, 'httpd-multi-proxies.conf')

# Start port for vhosts.
VHOST_PROXY_PORT_START = 9000
