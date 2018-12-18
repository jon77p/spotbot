#!/bin/bash
json=$(curl -s -f 'https://thewhitehat.club/status.json')
currentstate=$(echo $json | jq -r '.lab_open')
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
coffee=$(echo $json | jq -r '.coffee')
if [[ $currentstate == true || $coffee == true || $development == true ]]; then
	echo "Starting Raspotify..."
	$(sudo systemctl start raspotify.service)

	if [[ $(cat $logfile | tail -f -n 1) == "Playback:Halted" ]]
	then
		echo "Playback:Started" >> $logfile
	fi

	prevlog=$(cat $logfile | tail -f -n 1)
	currentlog=$(systemctl status raspotify | tail -f -n 2 | head -n 1)

	if [ "$currentlog" != "$prevlog" ]
	then
		echo "$currentlog" >> $logfile
		curl $url/api/refresh -d "data=test" -X PUT
	fi
	prevstate=false
elif [[ $currentstate == false && $coffee == false ]]; then
	echo "Stopping Raspotify..."
	$(sudo systemctl stop raspotify.service)
	$(rm $logfile)
	$(touch $logfile)
	echo "Playback:Halted" >> $logfile
	prevstate=true
fi
echo "Done!"
