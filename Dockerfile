## ----------------------------------------------------------------------------
## ############################################################################
## ----------------------------------------------------------------------------

FROM ubuntu:trusty
MAINTAINER Hasan Karahan <hasan.karahan@blackhan.com>

## ----------------------------------------------------------------------------
## Part (#): `api-cache:ibm` ##################################################
## ----------------------------------------------------------------------------

CMD (sleep 60; npm start)

## ----------------------------------------------------------------------------
## Part (a): `api-cache:nil` ##################################################
## ----------------------------------------------------------------------------

# ubuntu: updates & upgrades
RUN apt-get -y update && \
    apt-get -y upgrade

# locale: `en_US.UTF-8`
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

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
## Part (c): `api-cache:dev` ##################################################
## ----------------------------------------------------------------------------

# api-cache: copy and unpack archive
ADD HEAD.zip /tmp/HEAD.zip
RUN mkdir -p /srv/api-cache.app
RUN unzip /tmp/HEAD.zip -d /srv/api-cache.app
RUN rm -f /tmp/HEAD.zip

# api-cache: python env
RUN cd /srv/api-cache.app && \
    /bin/bash -c './scripts/setup.sh'
RUN cd /srv/api-cache.app && \
    /bin/bash -c 'source bin/activate && ./setup.py install'
RUN cd /srv/api-cache.app && \
    /bin/bash -c 'mkdir -p .python-eggs'

# api-cache: setup repository owner
RUN chown www-data:www-data /srv/api-cache.app -R

## ----------------------------------------------------------------------------
## Part (d): `api-cache:run` ##################################################
## ----------------------------------------------------------------------------

# api-cache: `website.run`
RUN cd /srv/api-cache.app && echo '#!/bin/bash\n\
\n\
cd /srv/api-cache.app && CMD=$@ && /usr/bin/sudo -u www-data -g www-data \
    /bin/bash -c "source bin/activate && PYTHON_EGG_CACHE=.python-eggs $CMD"\n\
' > service.run && chmod +x service.run

# api-cache: execute `website.run`
ENTRYPOINT ["/srv/api-cache.app/service.run"]

## ----------------------------------------------------------------------------
## ############################################################################
## ----------------------------------------------------------------------------
