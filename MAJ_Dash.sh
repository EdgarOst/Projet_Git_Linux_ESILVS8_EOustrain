### Script de mise à jour de dash qui kill le port et relance le script python

kill $(lsof -t -i:8050)
/usr/bin/python3 /home/ec2-user/Projet_Git_Linux_ESILVS8_EOustrain/Projet_Linux_S8.py
