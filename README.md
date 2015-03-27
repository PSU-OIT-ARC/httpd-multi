# httpd-multi

Run multiple instances of apache on different ports, with minimal changes to your normal apache configuration.

## How it Works

httpd-multi looks in your /etc/httpd/vhost.d directory for all files ending in `.vhost`. Each of those files should contain a listen directive and one or more &lt;VirtualHost&gt;s

httpd-multi will issue the httpd command with these options set on the command line:

    -Dhttpdmulti # defines a variable you can use in conf files if needed
    -C 'User apache'
    -C 'Group apache'
    -c 'Include path/to/vhost.vhost' # includes the vhost file itself
    -c 'PidFile /var/run/httpd/httpdmulti.name.vhost.pid' # specifies the PID file

It then generates a normal vhost file (coping in the ServerName and ServerAlias directives) that proxies to the instance of apache it just spawned off (0proxy.conf). When the default apache instance is reloaded (the one running on port 80), it proxies to that other instance of Apache running on some abitrary port when there is a ServerName or ServerAlias match.

It passes any extra arguments along to httpd, so the usage is (almost) the same as httpd.

## Usage

Same as httpd:

    ./httpd-multi -k start
    ./httpd-multi -k restart
    ./httpd-multi -k reload

Print an available port number that you can use in a .vhost file for the `Listen` directive:

    ./httpd-multi

## Example vhost file in /etc/httpd/vhost.d/example.vhost

    # we can set the user and group to anything
    User svusr114
    Group resgrp114
    Listen 9001
    <VirtualHost *:*>
        ServerName example.com
        ServerAlias *.example.com
        ErrorLog /var/log/httpd/example.error_log
        CustomLog /var/log/httpd/example.access_log vhost
        # django
        WSGIDaemonProcess example processes=2 threads=2 umask=0002 home=/tmp display-name=%{GROUP}
        WSGIProcessGroup  example
        WSGIScriptAlias / /path/to/wsgi.py

        Alias /media/logos /path/to/media/logos
        Alias /static /path/to/static

        XSendFile on
        XSendFilePath /path/to/media

        <Directory /path/to/static>
            AllowOverride All
        </Directory>

    </VirtualHost>
