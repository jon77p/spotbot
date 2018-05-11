#!/bin/bash
currentstate=$(curl -s 'https://thewhitehat.club/status.json' | jq -r '.lab_open')
if [[ $currentstate == true ]]; then
	echo "Starting Raspotify..."
	$(sudo systemctl start raspotify.service)

	if [[ $(cat /home/pi/raspotify.log | tail -f -n 1) == "Playback:Halted" ]]
	then
		echo "Playback:Started" >> /home/pi/raspotify.log
	fi

	prevlog=$(cat /home/pi/raspotify.log | tail -f -n 1)
	currentlog=$(systemctl status raspotify | tail -f -n 2 | head -n 1)

	if [ "$currentlog" != "$prevlog" ]
	then
		echo "$currentlog" >> /home/pi/raspotify.log
	fi
	prevstate=false
else
	echo "Stopping Raspotify..."
	$(sudo systemctl stop raspotify.service)
	$(rm /home/pi/raspotify.log)
	$(touch /home/pi/raspotify.log)
	echo "Playback:Halted" >> /home/pi/raspotify.log
	prevstate=true
fi
echo "Done!"
