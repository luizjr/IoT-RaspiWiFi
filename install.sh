#!/bin/sh -e
echo "Instalando RaspiWiFi Headless..."
git clone https://github.com/marvmex/IoT-RaspiWiFi.git
cd IoT-RaspiWiFi
echo "Iniciando..."
sudo sh start.sh
