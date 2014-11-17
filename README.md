# httpd-multi

Run multiple instances of apache on different ports, with minimal changes to your normal apache configuration.

## How it Works

httpd-multi looks in your /etc/httpd/vhost.d directory for all files ending in
`.vhost` that have ServerName or ServerAlias lines.

If the file matches, httpd-multi will issue the httpd command with these options set on the command line:

    -f base.conf # your base httpd configuration located in /etc/httpd
    -Dhttpdmulti # defines a variable you can use in conf files if needed
    -C 'User apache'
    -C 'Group apache'
    -c 'Include path/to/vhost.vhost' # includes the vhost file itself
    -c 'Listen {port}' # tell httpd to listen on an arbitrary port
    -c 'PidFile /var/run/httpd/httpdmulti.name.vhost.pid' # specifies the PID file

It then generates a normal vhost file (coping in the ServerName and ServerAlias directives) that proxies to the instance of apache it just spawned off. When the default apache instance is reloaded (the one running on port 80), it automagically proxies to that other instance of Apache running on some abitrary port.

It passes any extra arguments along to httpd, so the usage is the same as httpd.

## Usage

Same as httpd:

    ./httpd-multi -k start
    ./httpd-multi -k restart
    ./httpd-multi -k reload

## Example vhost file in /etc/httpd/vhost.d/example.vhost

    # we can set the user and group to anything
    User svusr114
    Group resgrp114
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
