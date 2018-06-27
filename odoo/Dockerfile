FROM odoo:11.0

USER root

RUN mkdir -p /mnt/utils /mnt/community-addons /mnt/dev-addons \
    && chown -R odoo:odoo /mnt/utils /mnt/community-addons /mnt/dev-addons

# RUN git clone --depth=1 -b 11.0 https://github.com/OCA/web.git  /mnt/community-addons/web 


COPY extra-requirements.txt /mnt/utils/extra-requirements.txt
COPY scripts /mnt/utils/scripts
COPY conf /mnt/utils/scripts/conf
COPY entrypoint.sh /entrypoint.sh

RUN pip3 install wheel \
    && pip3 install -r /mnt/utils/extra-requirements.txt

USER odoo

CMD ["run"]



