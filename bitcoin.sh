#!/bin/bash

# Récupère le prix actuel du Bitcoin depuis Cryptorank
bit=$(curl -s https://cryptorank.io/price/bitcoin | grep -oP '<div class="sc-3a84429e-0 kYOmyq">\$ \w+,\w+<' | grep -oP '\w+,\w+' | sed 's/,//g')

# Chemin d'accès au fichier CSV
CSV='/home/ec2-user/projet/data.csv'

# Ajoute la date actuelle et le prix du Bitcoin dans le fichier CSV
echo "$(date +%s),$bit" >> "$CSV"
