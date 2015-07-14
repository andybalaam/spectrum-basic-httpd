FROM andybalaam/apache
MAINTAINER Andy Balaam <andybalaam@artificialworlds.net>

# non-free is for the spectrum-roms package :-(

RUN \
    perl -p -i -e 's/main/main non-free/' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y \
        git \
        gcc \
        make \
    && \
    git clone https://github.com/andybalaam/bas2tap.git && \
    cd bas2tap && \
    make

RUN \
    apt-get install -y \
        fuse-emulator-sdl \
        spectrum-roms \
        xvfb

RUN \
    apt-get remove -y \
        git \
        gcc \
        make \
    && \
    apt-get autoremove -y

COPY spectrum-basic.cgi  /usr/lib/cgi-bin/
COPY spectrum-basic.conf /etc/apache2/conf-available/
RUN /bin/ln -sf /etc/apache2/conf-available/spectrum-basic.conf /etc/apache2/conf-enabled/
RUN /bin/ln -sf /etc/apache2/mods-available/cgi.load            /etc/apache2/mods-enabled/
RUN /bin/ln -sf /etc/apache2/mods-available/actions.conf        /etc/apache2/mods-enabled/
RUN /bin/ln -sf /etc/apache2/mods-available/actions.load        /etc/apache2/mods-enabled/

COPY hello.basic /var/www/html/

EXPOSE 80

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

