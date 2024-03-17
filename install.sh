#!/bin/bash
sudo mkdir -p /opt/ping_exporter
sudo cp ping_exporter.py /opt/ping_exporter/ping_exporter.py
echo '[Unit]
Description=Ping Exporter for Prometheus
After=network-online.target

[Service]
ExecStart=/usr/bin/python3 /opt/ping_exporter/ping_exporter.py
Restart=always

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/ping_exporter.service

sudo systemctl daemon-reload
sudo systemctl start ping_exporter
sudo systemctl enable ping_exporter
