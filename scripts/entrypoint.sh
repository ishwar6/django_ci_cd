#!/bin/sh

set -e        #it will throw error if some command fails in the script
envsubst < /etc/nginx/default.conf.tpl / /etc/nginx/conf.d/defualt.conf

#start the nginx in docker but not in background
nginx -g 'daemon off;'


