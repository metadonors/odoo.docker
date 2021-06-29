#!/bin/bash
set -e
args=("$@")

/usr/bin/env python3 /mnt/utils/scripts/generate_odoo_conf.py --template='/mnt/utils/scripts/conf/odoo.cfg.j2' --config='/mnt/utils/scripts/conf/odoo_conf.yaml' > /etc/odoo/odoo.conf

# set the postgres database host, port, user and password according to the environment
# and pass them as arguments to the odoo process if not present in the config file
: ${HOST:=${ODOO_DB_HOST:='db'}}
: ${PORT:=${ODOO_DB_PORT:='5432'}}
: ${USER:=${ODOO_DB_USER:=${POSTGRES_USER:='odoo'}}}
: ${PASSWORD:=${ODOO_DB_PASSWORD:=${POSTGRES_PASSWORD:='odoo'}}}

DB_ARGS=()
function check_config() {
    param="$1"
    value="$2"
    # if grep -q -E "^\s*\b${param}\b\s*=" "$ODOO_RC" ; then       
    #     value=$(grep -E "^\s*\b${param}\b\s*=" "$ODOO_RC" |cut -d " " -f3|sed 's/["\n\r]//g')
    # fi;
    DB_ARGS+=("--${param}")
    DB_ARGS+=("${value}")
}

check_config "db_host" "$HOST"
check_config "db_port" "$PORT"
check_config "db_user" "$USER"
check_config "db_password" "$PASSWORD"

case $1 in
    ipython)
        exec sudo -E -u odoo odoo ipython
        ;;
    shell)
        exec sudo -E -u odoo odoo shell ${args[@]:1}
        ;;
    upgrade)
        exec sudo -E -u odoo odoo -c /etc/odoo/odoo.conf -u ${args[@]:1} --stop-after-init
        ;;
    test)
        exec sudo -E -u odoo odoo -c /etc/odoo/odoo.conf --workers 0 --log-level=test --test-enable --stop-after-init -u ${args[@]:1}
        ;;
    test_all)
        exec sudo -E -u odoo odoo -c /etc/odoo/odoo.conf --workers 0 --test-enable --stop-after-init
        ;;
    run)
        wait-for-psql.py ${DB_ARGS[@]} --timeout=30
        echo "Starting nginx..."
        nginx -c /etc/nginx/nginx.conf &    
        echo "Starting Odoo..."
        sudo -E -u odoo odoo -c /etc/odoo/odoo.conf ${args[@]:1}
        ;;
    prod)
        wait-for-psql.py ${DB_ARGS[@]} --timeout=30
        echo "Starting nginx..."
        exec nginx -c /etc/nginx/nginx.conf &    

        echo "Starting Odoo with migrations..."
        exec sudo -E -u odoo odoo -c /etc/odoo/odoo.conf ${args[@]:1} -u project_migrations
        ;;
    *)
        exec "$@"
        ;;
esac
