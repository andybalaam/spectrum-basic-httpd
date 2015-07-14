FROM andybalaam/apache
MAINTAINER Andy Balaam <andybalaam@artificialworlds.net>

EXPOSE 80
EXPOSE 443

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

