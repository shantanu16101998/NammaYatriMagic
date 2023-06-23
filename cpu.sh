#!/bin/bash
git add .
git commit -n -m "test"
branchName=`git rev-parse --abbrev-ref HEAD`
git remote add gitea "http://192.168.11.192:9001/piyushk/beckn-test.git"
git push gitea $branchName -f
curl --location --request POST 'http://192.168.11.192:9002/startBuild' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user": "shantanu",
    "branch": "'"$branchName"'",
    "buildCommand": ""
}'

buildDone=false
while [[ $buildDone == false ]]
do
  res=`curl --location --request POST 'http://192.168.11.192:9002/status' \
            --header 'Content-Type: application/json' \
            --data-raw '{
                "user": "username"
            }'
            `
  buildDone=`echo $res | jq '.done'`
  echo $buildDone
  echo $res
  sleep 2
done
