## ----------------------------------------------------------------------------
## ############################################################################
## ----------------------------------------------------------------------------

FROM ubuntu:xenial
MAINTAINER Hasan Karahan <hasan.karahan@blackhan.com>

## ----------------------------------------------------------------------------
## Part (#): `apicache:ibm` ###################################################
## ----------------------------------------------------------------------------

## CMD (sleep 60; npm start)

## ----------------------------------------------------------------------------
## Part (a): `apicache:nil` ###################################################
## ----------------------------------------------------------------------------

# ubuntu: updates & upgrades
RUN apt-get -y update && \
    apt-get -y upgrade

# basic tools
RUN apt-get -y install sudo
RUN apt-get -y install unzip
RUN apt-get -y install curl

# builds, python, pip, virtualenv
RUN apt-get -y install build-essential
RUN apt-get -y install python-all
RUN apt-get -y install python-all-dev
RUN apt-get -y install python-pip
RUN apt-get -y install python-virtualenv

# clean & remove
RUN apt-get -y clean
RUN apt-get -y autoclean
RUN apt-get -y autoremove

## ----------------------------------------------------------------------------
## Part (c): `apicache:dev` ###################################################
## ----------------------------------------------------------------------------

# apicache: copy and unpack archive
ADD HEAD.zip /tmp/HEAD.zip
RUN mkdir -p /srv/apicache.app
RUN unzip /tmp/HEAD.zip -d /srv/apicache.app
RUN rm -f /tmp/HEAD.zip

# apicache: python env
RUN cd /srv/apicache.app && \
    /bin/bash -c './scripts/setup.sh'
RUN cd /srv/apicache.app && \
    /bin/bash -c 'source bin/activate && ./setup.py install'
RUN cd /srv/apicache.app && \
    /bin/bash -c 'mkdir -p .python-eggs'

# apicache: setup repository owner
RUN chown www-data:www-data /srv/apicache.app -R

## ----------------------------------------------------------------------------
## Part (d): `apicache:run` ###################################################
## ----------------------------------------------------------------------------

# apicache: `service.run`
RUN cd /srv/apicache.app && echo '#!/bin/bash\n\
\n\
cd /srv/apicache.app && CMD=$@ && /usr/bin/sudo -u www-data -g www-data \
    /bin/bash -c "source bin/activate && PYTHON_EGG_CACHE=.python-eggs $CMD"\n\
' > service.run && chmod +x service.run

# apicache: execute `service.run`
ENTRYPOINT ["/srv/apicache.app/service.run"]

## ----------------------------------------------------------------------------
## ############################################################################
## ----------------------------------------------------------------------------
