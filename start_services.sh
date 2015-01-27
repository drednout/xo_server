#!/bin/sh

#clean rabbitmq vhost, if needed
#curl -i -u guest:guest -XDELETE 'http://localhost:15672/api/vhosts/%2Fxo'
#curl -i -u guest:guest -XPUT -H "content-type:application/json" 'http://localhost:15672/api/vhosts/%2Fxo'
#curl -i -u guest:guest -XPUT -H "content-type:application/json"  'http://localhost:15672/api/permissions/%2Fxo/guest' -d  '{"configure":".*","write":".*","read":".*"}'

mkdir -p logs
mkdir -p run

supervisord -c cfg/supervisord_local.conf
