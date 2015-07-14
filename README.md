ZX Spectrum BASIC httpd Server
==============================

Finally, you can write CGI scripts for serving web pages in good old ZX Spectrum BASIC.

To run from the Docker repository:

    **NOT WORKING YET**
    sudo apt-get install docker.io
    docker run -p 80:80 -p 443:443 -v /home/jdoe/mysite/:/var/www/ -d andybalaam/spectrum-basic-httpd
    **NOT WORKING YET**

To run without Docker, install Apache HTTPD and configure it to use spectrum-basic.cgi as a CGI-handler for .basic files, with something like this:

    AddHandler spectrum-basic .basic
    Action spectrum-basic /cgi-bin/spectrum-basic.cgi

