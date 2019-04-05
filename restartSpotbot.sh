#!/bin/bash

systemctl daemon-reload
systemctl restart librespot.service
systemctl restart spotbot.service
systemctl restart nginx.service
systemctl restart spotbot_script.service
systemctl restart spotbot_script.timer
