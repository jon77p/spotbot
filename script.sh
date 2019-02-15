#!/bin/bash
json=$(curl -s -f 'https://thewhitehat.club/api/status')
currentstate=$(echo $json | jq -r '.data.status')
development=false
if [[ $# != "2" && $# != "3" ]]; then
	echo "$#"
	echo "Usage: ./script.sh (-dev) <log_file> <server_url>"
	exit
fi
if [[ $1 == "-dev" ]]; then
	development=true
	logfile=$2
	url=$3
else
	logfile=$1
	url=$2
fi
if [[ $currentstate == 'open' ]]; then
	echo "Starting Librespot..."
	$(sudo systemctl start librespot.service)

	if [[ $(cat $logfile | tail -f -n 1) == "Playback:Halted" ]]
	then
		echo "Playback:Started" >> $logfile
	fi

	prevlog=$(cat $logfile | tail -f -n 1)
	currentlog=$(systemctl status librespot.service | tail -f -n 2 | head -n 1)

	if [ "$currentlog" != "$prevlog" ]
	then
		echo "$currentlog" >> $logfile
		curl $url/api/refresh -d "data=test" -X PUT
	fi
	prevstate=false
else
	echo "Stopping Librespot..."
	$(sudo systemctl stop librespot.service)
	$(rm $logfile)
	$(touch $logfile)
	echo "Playback:Halted" >> $logfile
	prevstate=true
fi
echo "Done!"
