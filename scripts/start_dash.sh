#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl enable dash.service
sudo systemctl start dash.service
sudo systemctl status dash.service