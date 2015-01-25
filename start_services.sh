#!/bin/sh
curl -i -u guest:guest -XDELETE 'http://localhost:15672/api/vhosts/%2Fxo'
curl -i -u guest:guest -XPUT -H "content-type:application/json" 'http://localhost:15672/api/vhosts/%2Fxo'
curl -i -u guest:guest -XPUT -H "content-type:application/json"  'http://localhost:15672/api/permissions/%2Fxo/guest' -d  '{"configure":".*","write":".*","read":".*"}'

rm *.log
XO_SERVICE_ID=1 python xo_server/login/server.py cfg/login_service1.yml >> login1.log 2>&1 &
XO_SERVICE_ID=2 python xo_server/login/server.py cfg/login_service2.yml >> login2.log 2>&1 &
XO_SERVICE_ID=1 python xo_server/game/server.py cfg/game_service1.yml >> game1.log 2>&1 &
XO_SERVICE_ID=2 python xo_server/game/server.py cfg/game_service2.yml >> game2.log 2>&1 &
XO_SERVICE_ID=1 python xo_server/bind/server.py cfg/bind_service.yml >> bind.log 2>&1 &
