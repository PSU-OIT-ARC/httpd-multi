# httpd-multi

Run multiple instances of apache on different ports, with minimal changes to your normal apache configuration.

## How it Works

httpd-multi looks in your /etc/httpd/vhost.d directory for all files ending in
`.conf` that have a line matching

    <IfDefine {name}.{port}>

where {name} is a string in [A-Za-z0-9]+ and {port} is an integer number.

If the file matches, httpd-multi will issue the httpd command with these options set on the command line:

    -f /this/dir/base.conf # your base httpd configuration located in this directory
    -Dhttpdmulti # defines a variable you can use in conf files if needed
    -D{name}.{port} # defines the variable in the <IfDefine>
    -c 'Include path/to/vhost.conf' # includes the vhost file itself
    -c 'Listen {port}' # tell httpd to listen on the right port specified by the <IfDefine> flag
    -c 'PidFile run/{name}.{port}.pid' # specifies the PID file
    -c 'ErrorLog logs/{port}_error_log' # specifies the location of the log file

It passes any extra arguments along to httpd.

## Usage

Same as httpd:

    ./httpd-multi -k start
    ./httpd-multi -k restart
    ./httpd-multi -k reload

## Example vhost file in /etc/httpd/vhost.d/example.conf

    # Define a vhost that works on port 80, that proxies to port 8002
    <VirtualHost *:80>
        ServerName example.com
        ServerAlias *.example.com
        ProxyPreserveHost on
        ProxyPass / http://localhost:8002/ retry=1
        ProxyPassreverse / http://localhost:8002/
    </VirtualHost>


    # Define the vhost that should be running on port 8002
    <IfDefine example.8002>
        # we can set the user and group to anything
        User svusr114
        Group resgrp114
        <VirtualHost *:*>
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
    </IfDefine>

## Gotchas 

If you remove a vhost file, 
