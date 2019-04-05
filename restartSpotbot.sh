#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl restart librespot.service
sudo systemctl restart spotbot.service
sudo systemctl restart nginx.service
sudo systemctl restart spotbot_script.service
sudo systemctl restart spotbot_script.timer
