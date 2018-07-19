FROM odoo:11.0

USER root

RUN echo "deb http://ftp.de.debian.org/debian testing main" >> /etc/apt/sources.list
RUN echo 'APT::Default-Release "stable";' | tee -a /etc/apt/apt.conf.d/00local
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
    && apt-get -y -t testing install python3 python3-dev python3-pip \
    && mkdir -p /mnt/utils /mnt/community-addons /mnt/dev-addons /mnt/bundle-addons \
    && chown -R odoo:odoo /mnt/utils /mnt/community-addons /mnt/dev-addons /mnt/bundle-addons

RUN git clone --depth=1 -b 11.0 https://github.com/OCA/web.git  /mnt/bundle-addons/web \
    && git clone --depth=1 -b 11.0 https://github.com/Openworx/backend_theme.git /mnt/bundle-addons/backend_theme

COPY extra-requirements.txt /mnt/utils/extra-requirements.txt
COPY scripts /mnt/utils/scripts
COPY conf /mnt/utils/scripts/conf
COPY entrypoint.sh /entrypoint.sh

COPY conf/web/nginx.conf /etc/nginx/nginx.conf
COPY conf/web/odoo.conf /etc/nginx/conf.d/default.conf

RUN pip3 install wheel \
    && pip3 install -r /mnt/utils/extra-requirements.txt

CMD ["run"]



