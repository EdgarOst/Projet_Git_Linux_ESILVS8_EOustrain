### Script de scraping de données sur le site Tradingsat 

echo "$(date +'%Y-%m-%d %H:%M:%S'),$(curl -s https://forex.tradingsat.com/cours-euro-dollar-FX0000EURUSD/ | grep '<span class=\"price\">' | sed 's/.*>\([^<]*\)<.*/\1/')" >> /home/ec2-user/prixUSD.csv
echo "$(date +'%Y-%m-%d %H:%M:%S'),$(curl -s https://forex.tradingsat.com/cours-euro-yen-FX0000EURJPY/ | grep '<span class=\"price\">' | sed 's/.*>\([^<]*\)<.*/\1/')" >> /home/ec2-user/prixYEN.csv
echo "$(date +'%Y-%m-%d %H:%M:%S'),$(curl -s https://forex.tradingsat.com/cours-euro-livre-sterling-FX0000EURGBP/ | grep '<span class=\"price\">' | sed 's/.*>\([^<]*\)<.*/\1/')" >> /home/ec2-user/prixGBP.csv
