#!/bin/bash
app="netapp-preprod"
docker run -v /etc/localtime:/etc/localtime:ro -d --restart unless-stopped -p 80:80 --name=${app} -v $(pwd)/app ${app}