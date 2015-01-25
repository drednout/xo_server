#!/bin/sh

#curl -i  -XPOST 'http://localhost:11301/login/email' --data 'email=dr@localhost&password=1'
curl -i  -XPOST 'http://localhost:12302/login' --data 'sid=9714eee20fedf7dbea31da18e2f99fc9ebd4fc0b'
curl -i  -XGET 'http://localhost:12302/get_profile?sid=9714eee20fedf7dbea31da18e2f99fc9ebd4fc0b'
curl -i  -XPOST 'http://localhost:12302/start_simple_game' --data 'sid=9714eee20fedf7dbea31da18e2f99fc9ebd4fc0b'
curl -i  -XGET 'http://localhost:12302/get_current_game?sid=9714eee20fedf7dbea31da18e2f99fc9ebd4fc0b'
