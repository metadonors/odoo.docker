FROM odoo:15.0

USER root

RUN mkdir -p /mnt/utils /mnt/bundle-addons \
    && chown -R odoo:odoo /mnt/utils /mnt/bundle-addons

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        vim \
        libtool \
        nginx \
        sudo \
        pkg-config \
        python3-dev \
       # python3 python3-dev python3-pip 
    && rm -rf /var/lib/apt/lists/*

COPY ./odoo/extra-requirements.txt /mnt/utils/extra-requirements.txt

RUN pip3 install -U wheel setuptools>=38.6.1
RUN pip3 install -r /mnt/utils/extra-requirements.txt

COPY ./odoo/scripts /mnt/utils/scripts
COPY ./odoo/conf /mnt/utils/scripts/conf
# COPY ./odoo/wait-for-it.sh /wait-for-it.sh

COPY ./odoo/conf/web/nginx.conf /etc/nginx/nginx.conf
COPY ./odoo/conf/web/odoo.conf /etc/nginx/conf.d/default.conf

COPY ./addons/ /mnt/bundle-addons/

COPY ./odoo/entrypoint.sh /entrypoint.sh


# CMD ["run"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]



