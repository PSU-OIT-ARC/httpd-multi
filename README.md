# httpdmulti

Run multiple instances of Apache on different ports with minimal changes
to your normal Apache configuration.

## Installation

### Development

    make init

### Production

    make init
    sudo make install

## How it works

httpdmulti looks in your `/etc/httpd/vhost.d` directory for all files
ending in `.vhost`. Each of those files should contain a `Listen`
directive and one or more `<VirtualHost>` sections.

httpdmulti will run the httpd command with these options set on the
command line:

    -Dhttpdmulti
    -c 'Include /etc/httpd/vhost.d/{name}.vhost'
    -c 'PidFile /var/run/httpd/httpdmulti-{name}.pid'
    -c 'CustomLog /var/log/httpd/{name}.access_log combined'
    -c 'ErrorLog /var/log/httpd/{name}.error_log'

It then generates a proxying vhost (copying in the ServerName and
ServerAlias directives) that proxies to the instance of Apache it just
spawned off). When the default Apache instance is reloaded (the one
running on port 80 and 443), it proxies to that other instance of Apache
running on some abitrary port when there is a ServerName or ServerAlias
match.

By default, the generated vhost is configured to redirect HTTP traffic
to HTTPS, and the HTTPS vhost does the actual proxying. If you do not
want to use SSL for that vhost, put `#nossl` on a line in the .vhost
file.

## Usage

Similar to httpd (operates on all httpdmulti instances):

    httpdmulti start
    httpdmulti restart
    httpdmulti graceful

You can also specify a single site:

    httpdmulti graceful -s quickticket

Print an available port number that you can use in a .vhost file for the
`Listen` directive:

    httpdmulti find-port

## Example vhost file

    Note: This is a real example taken from merope.

    # These lines are the most relevant to httpdmulti.
    Listen 9020
    User svusr368
    Group resgrp368

    # The VirtualHost section is just a normal vhost setup.
    <VirtualHost *>
        ServerName oregoninvasiveshotline.stage.rc.pdx.edu
        WSGIDaemonProcess oregoninvasiveshotline-stage processes=2 threads=25 umask=0002 display-name=%{GROUP} home=/vol/www/oregoninvasiveshotline
        WSGIProcessGroup oregoninvasiveshotline-stage
        WSGIScriptAlias / /vol/www/oregoninvasiveshotline/stage/wsgi/wsgi.py
        Alias /media /vol/www/oregoninvasiveshotline/media/stage
        Alias /static /vol/www/oregoninvasiveshotline/static/stage
        Alias /favicon.ico /vol/www/oregoninvasiveshotline/static/stage/favicon.ico
        Alias /robots.txt /vol/www/oregoninvasiveshotline/static/stage/robots.txt
    </VirtualHost>
