FROM nginx:1.13.1-alpine

COPY ./configs/nginx.conf /etc/nginx/nginx.conf
COPY ./configs/odoo.conf /etc/nginx/conf.d/default.conf

VOLUME /etc/nginx/

EXPOSE 80 443

CMD ["nginx"]
