# Path to the httpd executable.
HTTPD = '/usr/sbin/httpd'

# Path to the vhost directory.
VHOST_DIR = '/etc/httpd/vhost.d'

# The suffix on the files we want to parse to create additional
# instances of Apache for.
VHOST_SUFFIX = '.vhost'

# A name to use for pid files so we know which ones belong to us.
IDENTIFIER = 'httpdmulti'

# Where to store PID files.
PID_DIR = '/var/run/httpd'

# Path to the generated Apache confif file that proxies to our
# httpdmulti instances.
PROXY_VHOST_NAME = 'main-conf.d/httpd-multi-proxies.conf'

# Start port for vhosts.
VHOST_PROXY_PORT_START = 9000
