#!/bin/bash
sudo ln -s etc/systemd/system/librespot.service /etc/systemd/system/librespot.service
sudo ln -s etc/systemd/system/spotbot.service /etc/systemd/system/spotbot.service
sudo ln -s etc/systemd/system/spotbot_script.service /etc/systemd/system/spotbot_script.service
sudo ln -s etc/systemd/system/spotbot_script.timer /etc/systemd/system/spotbot_script.timer
sudo systemctl daemon-reload
sudo systemctl start librespot.service
sudo systemctl enable librespot.service
sudo systemctl start spotbot.service
sudo systemctl enable spotbot.service
sudo systemctl start spotbot_script.service
sudo systemctl enable spotbot_script.service
sudo systemctl start spotbot_script.timer
sudo ln -s etc/nginx/sites-available/spotbot /etc/nginx/sites-available/spotbot
sudo ln -s /etc/nginx/sites-available/spotbot /etc/nginx/sites-enabled/spotbot
sudo systemctl restart nginx
