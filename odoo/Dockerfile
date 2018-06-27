FROM odoo:11.0

USER root



RUN apt-get update \
    && apt-get install -y git \
    && mkdir -p /mnt/utils /mnt/community-addons /mnt/dev-addons /mnt/bundle-addons \
    && chown -R odoo:odoo /mnt/utils /mnt/community-addons /mnt/dev-addons /mnt/bundle-addons

RUN git clone --depth=1 -b 11.0 https://github.com/OCA/web.git  /mnt/bundle-addons/web \
    && git clone --depth=1 -b 11.0 https://github.com/Openworx/backend_theme.git /mnt/bundle-addons/backend_theme

COPY extra-requirements.txt /mnt/utils/extra-requirements.txt
COPY scripts /mnt/utils/scripts
COPY conf /mnt/utils/scripts/conf
COPY entrypoint.sh /entrypoint.sh

RUN pip3 install wheel \
    && pip3 install -r /mnt/utils/extra-requirements.txt

USER odoo

CMD ["run"]



