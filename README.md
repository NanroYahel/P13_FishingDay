# P13_FishingDay
Parcours développeur d’application Python. Projet n°13

L'application est disponible à l'adresse : http://fishingday.herokuapp.com/


### M�mo pour le d�ploiement 

- Le token fourni par heroku pour le CI/CD est valable jusqu'au 26/11/2020. Passécette date, il faudra g�n�rer un nouveau token et le mettre dans le fichier `.travis.yml` apr�s l'avoir chiffr�.
La commande `travis encrypt $(heroku auth:token) --add deploy.api_key` permet de r�aliser ces deux op�rations, à condition d'avoir installéles CLI heroku et travis.
