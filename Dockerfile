FROM odoo:12.0

USER root

#RUN echo "deb http://ftp.de.debian.org/debian testing main" >> /etc/apt/sources.list
#RUN echo 'APT::Default-Release "stable";' | tee -a /etc/apt/apt.conf.d/00local
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        vim \
        build-essential \
        autoconf \
        libtool \
        nginx \
        sudo \
        openssh-client \
        pkg-config \
    && apt-get -y install python3 python3-dev python3-pip \
    && mkdir -p /mnt/utils /mnt/bundle-addons \
    && chown -R odoo:odoo /mnt/utils /mnt/bundle-addons


COPY ./odoo/extra-requirements.txt /mnt/utils/extra-requirements.txt
COPY ./odoo/scripts /mnt/utils/scripts
COPY ./odoo/conf /mnt/utils/scripts/conf
COPY ./odoo/entrypoint.sh /entrypoint.sh
COPY ./odoo/wait-for-it.sh /wait-for-it.sh

COPY ./odoo/conf/web/nginx.conf /etc/nginx/nginx.conf
COPY ./odoo/conf/web/odoo.conf /etc/nginx/conf.d/default.conf

COPY ./addons/ /mnt/bundle-addons/

RUN pip3 install wheel \
    && pip3 install -r /mnt/utils/extra-requirements.txt

CMD ["run"]



