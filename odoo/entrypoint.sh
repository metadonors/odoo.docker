#!/bin/bash
set -e
args=("$@")

/usr/bin/env python3 /mnt/utils/scripts/generate_odoo_conf.py --template='/mnt/utils/scripts/conf/odoo.cfg.j2' --config='/mnt/utils/scripts/conf/odoo_conf.yaml' > /etc/odoo/odoo.conf

case $1 in
    ipython)
        exec ipython
        ;;
    shell)
        exec odoo shell ${args[@]:1}
        ;;
    upgrade)
        exec odoo -c /etc/odoo/odoo.conf -u ${args[@]:1} --stop-after-init
        
        ;;
    run)
        exec odoo -c /etc/odoo/odoo.conf ${args[@]:1}
        ;;
    *)
        exec "$@"
        ;;
esac
