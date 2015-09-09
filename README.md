ZX Spectrum BASIC httpd Server
==============================

Finally, you can write CGI scripts for serving web pages in good old ZX Spectrum BASIC.

## Run with Docker

Get Docker:

    wget -qO- https://get.docker.com/ | sh

Run the server:

    make run

In another terminal, try it out:

    curl -v http://localhost:80/hello.basic

## Run without Docker

* Compile BAS2TAP from https://github.com/andybalaam/bas2tap and put the exe in /bas2tap/bas2tap
* Install Apache 2 web server
* Configure Apache to use the spectrum-basic.cgi file for .basic files.  Something like this:
    AddHandler spectrum-basic .basic
    Action spectrum-basic /cgi-bin/spectrum-basic.cgi
* Put your .basic files into /var/www/html
* Start Apache
* Navigate to e.g. http://localhost:80/hello.basic

## Explanation

http://www.artificialworlds.net/blog/2015/09/09/zx-spectrum-basic-web-server/

## TODO

- Docs on a derived docker container that allows you to drop in your own .basic files

- Support multiple simultaneous connections by using xvfb-run -a, and
  somehow kill the right Xvfb at the end.  Alternatively,
  kill the right fuse instance, and Xvfb and xvfb-run should get killed
  automatically.  Alternatively, kill the whole tree from xvfb-run down.

