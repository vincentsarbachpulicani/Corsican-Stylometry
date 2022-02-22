# Stylométrie en langue corse

## Description

Mes recherches commencèrent avec un mémoire de master soutenu en 2021 à l'Université de Strasbourg. Il s'agissait d'une étude comparative et quantitative entre deux revues différentes en apparence, mais représentatives de deux mouvements régulièrement assimilés ensemble à la fin des années 1930. L'objectif de ce mémoire était d'analyser l'objet culturel et matériel que représente un périodique afin de démontrer que les différences de formes et de fonds sont influencées par des variations idéologiques fondamentales entre l'irrédentisme fasciste et l'autonomisme corse de l'entre-deux-guerres. Pour ce faire, je me suis aidé d'une [base de données](https://heurist.huma-num.fr/heurist/?db=vsp_presse_corsiste_irredentiste&w=a&q=sortby%3A-m) particulièrement fournie qui pourrait se révéler utile pour la suite. Je me suis ensuite posé diverses questions sur l'anonymat des nombreux auteurs et articles. Dans le cadre de ce nouveau mémoire de recherche du master "Humanités numériques et computationnelles", de l'école nationale des Chartes, mon objectif est de déterminer quels sont les auteurs se dissimulant derrière un pseudonyme dans la signature d'articles en employant la stylométrie en langue corse. 

## *Preprocessing* des données

### Récupération des images de bonne qualité

Mon principal problème en ce début de recherche est l'accessibilité des données et métadonnées inhérentes à mes sources, à savoir la revue corse *A Muvra*. La visionneuse d'archive `THOT` des [archives de Corse](http://archives.isula.corsica/Internet_THOT/FrmSommaireFrame.asp) est difficilement exploitable et la numérisation des journaux à la BNF se termine en 1930. Néanmoins, afin de me constituer un premier corpus, je peux me baser sur les documents disponibles `gallica`. 

Afin d'exploiter des images de bonnes qualité avant d'opérer une phase d'océrisation, j'ai décidé de récupérer des images IIIF en haute résolution. Phase à certains problèmes de normalisation du nombre d'images en IIIF disponibles pour chaque numéro du journal, j'emploie le script `IIIF-Crawler`, développé par Thibault Clérice et Jean-Baptiste Camps. Cela me permet aussi, à termes, de ppovoir importer un nombre conséquent d'images de bonne qualité automatiquement.

Lors d'un stage effectué en février 2021 auprès de Guillaume Porte, ingénieur d'étude en humanités numériques rattaché à l'UR3400 ARCHE, j'ai eu l'occasion de développé un script permettant de récupérer automatiquement des métadonnées de revues de sociétés d'histoire lovcale alsacienne grâce aux identifiants `ark`. La réalisation de celui-ci rentrait dans le cadre du projet ***Alsatia Numerica*** visant à la création d'un portail permettant d'avoir accès facilement à toutes les ressources numérisées concernant l'histoire médiévale dans la région du Rhin supérieur, comme les thèses, les archives ou encore les articles de revues. L'idée est de réutiliser ce script et de l'adapter afin de récupérer les codes `ark` des articles d'*A Muvra* puis de les importer dans un fichier `.tsv` exploitable par le `IIIF-Crawler`. 

```bash
python3 iiifcrawler.py ID --source SOURCE --start 1 --end 2
```

En effet, cette commande ci-dessus permet de lancer le script `IIIF-Crawler`. Je vous renvoie vers la documentation du script disponible sur ce [dépôt](https://github.com/Jean-Baptiste-Camps/IIIF-Crawler). L'ID correspond dans mon cas à l'identifiant `ark`, source est `gallica`, le *start* et l'*end* sont les pages 1 et 4 dans la mesure où le format d'édition de la revue corse respecte ce nombre de pages à tarvers ses deux décennies d'existance. 

```bash
python3 iiifcrawler.py example.tsv
````

La commande ci-dessus permet de lire un fichier `.tsv` qui contient 4 colonnes : l'ID, la source, le *start* et l'*end*. Ainisi, générer automatiquement un fichier de ce type grâce à un script **python** qui exploite l'API de Gallica permet d'automatiser la démarche de récupération des images en haute résolution.

J'ai donc adapté le script réalisé dans le cadre de mon stage pour qu'il puisse récupérer le code `ark` de la revue, puis de chaque numéros. Le script s'occupe ensuite de créer un fichier `.tsv` qui peut être lu par le script `IIIF-Crawler`. la question s'est posée de savoir s'il fallait intégrer ce-dernier au script `IIIF-periodic-crawler` mais j'ai décidé d'utiliser directement le code inital à l'aide d'une commande de la librairie `os` pour ma faciliter la tâche. L'intégration au code est une manière d'améliorer ce script à l'avenir pour n'avoir qu'un seul fichier à utiliser.

Dans l'ensemble, le script fonctionne bien. Il reste néamoins très décevant car peu d'images en haute résolution sont téléchargées. Il va surement falloir trouver une autre idée.

***À suivre***

### Transcription automatique des textes

Pour la transcription des textes, je comptais utiliser le logiciel [eScriptorium](https://traces6.paris.inria.fr/) développé par l'Inria et le laboratoire [ALMAnaCH](https://files.inria.fr/almanach/index-en.html). Son interface intuitive permet de délimiter aisément des blocs de transcription, très utile pour la presse. J'ai d'abord essayé de transcrire mes textes à l'aide du modèle [*Modèle manuscrit DAHN NFC*](https://github.com/HTR-United) développé par Floriane Chiffoleau et trouvé sur le dépôt GitHub [HTR-United](https://github.com/HTR-United/dahncorpus). Néanmoins, se révélant finalement peu efficace dans le cadre de presses écrites en langue corse, je me suis orienté vers le modèle *19th century prints - HTRcatalogs Artlas* sous les conseils de Jean-Baptiste Camps. Bien plus efficace que le précédent, celui-ci semblait être une bonne source de travail pour entraîner un nouveau modèle propre aux presses corses afin d'avoir un taux d'efficacité optimal.

Néanmoins, la difficulté que j'ai eu pour entraîner un modèle de segmentation efficace m'handicapait et me faisait perdre du temps. j'ai pris la décision de basculer sur `tesseract-ocr` qui, en plus de posséder un module de transcription corse, permetd de compiler différentes langues notamment pour les textes écrits en plusieurs langues. J'ai créé un fichier `.bash` qui me permet de lancer automatiquement les commandes `tesseract` dans le terminal. Pour les almanachs, la transcription se fait en plusieurs étapes :

```bash
pdftoppm -r 300 -tiff texte.pdf texte
```

Cette commande permet de fragmenter en plusieurs autant de documents IIIF qu'il y a de pages dans un PDF. En effet, `tesseract` ne peut pas traiter un document unique et cette étape semble donc essentielle.

```bash
pdftoppm -r 300 -tiff *.pdf document
for f in *.tif; do
	tesseract $f $f -l fra+cos+ita
	tesseract $f $f -l fra+cos+ita alto
done
cat *.txt > document-total.txt
```

Cette dernière étape permet de transcrire tous les documents `.tif` grâce à une boucle et d'avoir en *output* un fichier `.txt` ainisi qu'un fichier en `xml/alto` avec la transcription. Enfin, on prend la décisions de concaténer tous les documents en un seul, plus utile pour le nettoyage du texte.

### Nettoyage du texte

Je me suis rapidement rendu compte lors de mes premiers résultats de transcription qu'il y avait un problème d'encodage des données textuelles. Certains caractères, qui semblaient identiques, n'étaient pas encodés en UTF-8 mais probalement en UTF-16. Afin de pouvoir nettoyer correctement le texte (accentuation et ponctuation), il m'a fallu faire un tableau de correspondance de ce type :

| **UTF-8** | **Encodage ES** |
| --------- | --------------- |
| ‘         | ’               |
| à         | à              |
| é         | é              |
| è         | è              |
| ò         | ò              |
| ô         | ô              |
| ù         | ù              |

Ainsi ce tableau, bien qu'en apparence simpliste, donne une idée des problèmes que j'ai pu avoir avec la normalisation de mes caractères. Suite aux conseils de Peter Stokes de l'EPHE, j'ai commencé à regardé des fonctions issues de librarires **python** pour normaliser l'unicode de mes textes. J'ai ainsi réglé ce problème avec la librairie `unicodedata` mais, ayant le projet d'utiliser **R**, j'ai donc décidé d'utiliser la package `stringi` et d'uitliser la fonction `stri_trans_nfc`. J'ai créé une fonction dénomme `clean_text`(à améliorer), disponible dans le repertoire "script" du dépôt, afin de nettoyer mes textes facilement.

Le basculement sur `tesseract` m'a permis de régler ce problème dès la base, l'unicode étant de base normalisé. Néanmoins, je compte quand même garder cette étape de normalisation "pour être sûr". Ma fonction `clean_text` permet de normaliser l'unicode du document `.txt`, de réguler la casse, de supprimer la ponctuation et l'accentuation des mots. Concernant l'accentuation, il s'agit d'un choix davantage méthodologique : il s'agit de savoir si nous prenoms en compte l'ortographe exacte des mots ou pas selon notre volet d'analyse.