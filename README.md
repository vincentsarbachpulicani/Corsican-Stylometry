# Stylométrie en langue corse

## Description

Mes recherches commencèrent avec un mémoire de master soutenu en 2021 à l'Université de Strasbourg. Il s'agissait d'une étude comparative et quantitative entre deux revues différentes en apparence, mais représentatives de deux mouvements régulièrement assimilés ensemble à la fin des années 1930. L'objectif de ce mémoire était d'analyser l'objet culturel et matériel que représente un périodique afin de démontrer que les différences de formes et de fonds sont influencées par des variations idéologiques fondamentales entre l'irrédentisme fasciste et l'autonomisme corse de l'entre-deux-guerres. A la suite de cette étude, je me suis posé diverses questions sur l'anonymat des nombreux auteurs et articles. Dans le cadre de ce nouveau mémoire de recherche du master "Humanités numériques et computationnelles", de l'école nationale des Chartes, mon objectif est de déterminer quels sont les auteurs se dissimulant derrière un pseudonyme dans la signature d'articles en employant des méthodes de stylométrie en langue corse.

## *Preprocessing* des données

### Récupération des images de bonne qualité

Mon principal problème en ce début de recherche est l'accessibilité des données et métadonnées inhérentes à mes sources, à savoir la revue corse *A Muvra*. La visionneuse d'archive `THOT` des archives de Corse est difficilement exploitable et la numérisation des journaux à la BNF se termine en 1930. Néanmoins, afin de me constituer un premier corpus, je peux me baser sur les documents disponibles `gallica`. 

Afin d'exploiter des images de bonnes qualité avant d'opérer une phase d'océrisation, j'ai décidé de récupérer des images IIIF en haute résolution. Phase à certains problèmes de normalisation du nombre d'images en IIIF disponibles pour chaque numéro du journal, j'emploie le script `IIIF-Crawler`, développé par Thibault Clérice et Jean-Baptiste Camps. Cela me permet aussi, à termes, de ppovoir importer un nombre conséquent d'images de bonne qualité automatiquement.

Lors d'un stage effectué en février 2021 auprès de Guillaume Porte, ingénieur d'étude en humanités numériques rattaché à l'UR3400 ARCHE, j'ai eu l'occasion de développé un script permettant de récupérer automatiquement des métadonnées de revues de sociétés d'histoire lovcale alsacienne grâce aux identifiants `ark`. La réalisation de celui-ci rentrait dans le cadre du projet ***Alsatia Numerica*** visant à la création d'un portail permettant d'avoir accès facilement à toutes les ressources numérisées concernant l'histoire médiévale dans la région du Rhin supérieur, comme les thèses, les archives ou encore les articles de revues. L'idée est de réutiliser ce script et de l'adapter afin de récupérer les codes `ark` des articles d'*A Muvra* puis de les importer dans un fichier `.tsv` exploitable par le `IIIF-Crawler`. 

```bash
python3 iiifcrawler.py ID --source SOURCE --start 1 --end 2
```

En effet, cette commande ci-dessus permet de lancer le script `IIIF-Crawler`. Je vous renvoie vers la documentation du script disponible sur ce [dépôt](https://github.com/Jean-Baptiste-Camps/IIIF-Crawler). L'ID correspond dans mon cas à l'identifiant `ark`, source est `gallica`, le *start* et l'*end* sont les pages 1 et 4 dans la mesure où le format d'édition de la revue corse respecte ce nombre de pages à tarvers ses deux décennies d'existance. 

```bash
python3 iiifcrawler.py example.tsv
````

La commande ci-dessus permet de lire un fichier `.tsv` qui contient 4 colonnes : l'ID, la source, le *start* et l'*end*. Ainisi, générer automatiquement un fichier de ce type grâce à un script python qui exploite l'API de Gallica permet d'automatiser la démarche de récupération des images en haute résolution.