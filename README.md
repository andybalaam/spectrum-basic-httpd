ZX Spectrum BASIC httpd Server
==============================

Finally, you can write CGI scripts for serving web pages in good old ZX Spectrum BASIC.

## Run with Docker

    # Get Docker
    sudo apt-get install docker.io
    
    # Write some ZX Spectrum BASIC code for dealing with requests
    mkdir $HOME/zx
    echo '1000 LPRINT "HTTP/1.0 200 OK"' > $HOME/zx
    docker run -p 80:80 -v $HOME/zx:/var/www/ -d andybalaam/spectrum-basic-httpd

    # In another terminal, try it out
    curl -v http://localhost:80

## Run without Docker

* Compile BAS2TAP from https://github.com/andybalaam/bas2tap and put the exe in /bas2tap/bas2tap
* Install Apache 2 web server
* Configure Apache to use the spectrum-basic.cgi file for .basic files.  Something like this:
    AddHandler spectrum-basic .basic
    Action spectrum-basic /cgi-bin/spectrum-basic.cgi

