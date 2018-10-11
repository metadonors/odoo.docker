#!/bin/bash
set -e
args=("$@")

/usr/bin/env python3 /mnt/utils/scripts/generate_odoo_conf.py --template='/mnt/utils/scripts/conf/odoo.cfg.j2' --config='/mnt/utils/scripts/conf/odoo_conf.yaml' > /etc/odoo/odoo.conf

case $1 in
    ipython)
        exec sudo -E -u odoo ipython
        ;;
    shell)
        exec sudo -E -u odoo odoo shell ${args[@]:1}
        ;;
    upgrade)
        exec sudo -E -u odoo odoo -c /etc/odoo/odoo.conf -u ${args[@]:1} --stop-after-init
        ;;
    run)
        echo "Starting nginx..."
        nginx -c /etc/nginx/nginx.conf &    
        echo "Starting Odoo..."
        sudo -E -u odoo odoo -c /etc/odoo/odoo.conf ${args[@]:1}
        ;;
    *)
        exec "$@"
        ;;
esac
