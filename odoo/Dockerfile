FROM odoo:12.0

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


RUN git clone --depth=1 -b 12.0 https://github.com/OCA/web.git  /mnt/bundle-addons/web \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/website.git /mnt/bundle-addons/website \
    && git clone --depth=1 -b 12.0 https://github.com/muk-it/muk_base.git /mnt/bundle-addons/muk_base \
    && git clone --depth=1 -b 12.0 https://github.com/muk-it/muk_web.git /mnt/bundle-addons/muk_web \
    && git clone --depth=1 -b 12.0  https://github.com/OCA/server-ux.git /mnt/bundle-addons/server-ux \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/server-tools.git /mnt/bundle-addons/server-tools \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/account-invoicing.git /mnt/bundle-addons/account-invoicing \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/partner-contact.git /mnt/bundle-addons/partner-contact \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/queue.git /mnt/bundle-addons/queue \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/rest-framework.git /mnt/bundle-addons/rest-framework \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/connector.git /mnt/bundle-addons/connector \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/purchase-workflow.git /mnt/bundle-addons/purchase-workflow \
    && git clone --depth=1 -b 12.0 https://github.com/OCA/contract.git /mnt/bundle-addons/contract

    
    

COPY extra-requirements.txt /mnt/utils/extra-requirements.txt
COPY scripts /mnt/utils/scripts
COPY conf /mnt/utils/scripts/conf
COPY entrypoint.sh /entrypoint.sh

COPY conf/web/nginx.conf /etc/nginx/nginx.conf
COPY conf/web/odoo.conf /etc/nginx/conf.d/default.conf

RUN pip3 install wheel \
    && pip3 install -r /mnt/utils/extra-requirements.txt

CMD ["run"]



