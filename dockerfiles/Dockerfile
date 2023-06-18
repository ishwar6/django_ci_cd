FROM nginxinc/nginx-unprivileged:1-alpine
#to run docker service as a least-previleged user, don't use default nginx image. 
LABEL maintainer="ishwarjangid"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params

#nginx will listen for these configurations
ENV LISTEN_PORT=8000
ENV APP_PORT=9000
ENV APP_HOST=app 

#switch to root user
USER root 

RUN mkdir -p /vol/static  
#p creates subdirectory as well 
RUN chmod 755 /vol/static
#owner can do everything and 5 for group and public (they can write, can only read and execute -> nginx user can read this file)
RUN touch /etc/nginx/conf.d/default.conf
RUN chown nginx:nginx /etc/nginx/conf.d/default.conf 
#nginx user can update this empty file created by touch with template file that we created by using envsubst

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER nginx

CMD ["/entrypoint.sh"]

