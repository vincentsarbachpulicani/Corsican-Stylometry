# Stylométrie en langue corse

## L'organisation du dépôt

**base_de_donnees** -> dossier contenant le fichier `.csv` de la base de données Heurist

**bibliographie** -> dossier contenant la biblio personnelle, le mémmorie de M1HN et le mémoire d'histoire contemporaine réalisé à l'université de Strasbourg

**data** -> dossier qui contient les données produites ou exploitées pendant la recherche

**projets_ext** -> dossier qui contient des scripts produits par des chercheurs tiers ou lors des projets différents

**ressources** -> dossier avec tous les scripts de traitement des données ou plus généralement de fonctionnement (scripts secondaires)

**statistiques_exploratoires** -> dossier contenant toutes les ressources sur l'analyse lexicométrique du corpus en langue corse (moderne/ancien)

**topic-modeling** -> dossier contenant toutes les ressources sur le topic modeling

## Description

Avec l’émergence des nationalismes du XIXe siècle se greffent conjointement des mouvements régionalistes d’affirmations et de revendications de particularismes culturels. La Corse s’insère très bien dans cette dynamique et se présente même comme un lieu propice au développement de telles idées. La centralisation de l’État autour d’une capitale forte et les politiques d’assimilation des populations indigènes à la frontière de la France ont poussé certains acteurs à défendre ces particularismes. Tradition jacobine de la « République une et indivisible », parfois largement exagérée, c’est notamment à partir du Second Empire et du règne de Napoléon III que la francisation de la Corse prend tout son sens. Cela s’est traduit par l’apprentissage du français à l’école en lieu et place du corse, des plans de relance économique et industrielle du territoire ou encore par la participation massive des Corses à l’effort colonial. Dès lors naissent les premières brigues d’une lutte régionaliste sur l’île c’est-à-dire par la défense de la langue corse, centrale dans la préservation des identités. C’est le cas de Santu Casanova, poète et rédacteur en chef de la revue *A Tramuntana* (« la Tramontane ») dont il est également le fondateur en 1896. L’un des aboutissements des nationalismes du XIXe siècle est bien connu, c’est la Première Guerre mondiale. Le désastre que cet événement engendre se ressent beaucoup sur l’île que ce soit en termes démographiques ou sociétaux. Encore aujourd’hui le nombre d’insulaires morts lors de ce qu’ils appellent le *scumpientu*, la « catastrophe », est difficile à chiffrer. Par ailleurs, cela a donné lieu à de nombreux débats idéologiques autour du sacrifice des Corses pour la « Grande Patrie » ou au nom d’une guerre qui ne les concernait pas.

Il existe en Corse une volonté de structurer et d’étudier les évolutions de l’emploi de la langue corse depuis les années 1980. On peut notamment mentionner les travaux de la linguiste Marie-José Dalbera-Stefanaggi avec son *Nouvel atlas linguistique et ethnographique de la Corse* dont le premier volume paraît en 1995.Dans les rééditions de cette œuvre majeure dans les années 2000, l’autrice incorpore notamment ses travaux sur la création d’un Banque de Données Langue Corse ([BDLC](https://bdlc.univ-corse.fr/bdlc/corse.php)). Il s’agit là de la première initiative dans la volonté de lemmatiser dans l’espace et le temps la langue corse. L’apport des humanités numériques dans cette problématique est assez neuf. Les réflexions des chercheurs sur l’outillage des langues régionales en utilisant le TALN (Traitement Automatique du langage Naturel) se sont vraiment accélérées à partir de la deuxième moitié de la décennie 2010. Notre démarche s’inscrit donc dans cette continuité. Face au manque d’outils pour traiter et analyser la langue corse, océriser des données textuelles afin qu’elles puissent être exploitées dans des recherches en humanités numériques représente un enjeux de taille dans l’avenir de la discipline en Corse.

Mes propres recherches commencèrent avec un mémoire de master soutenu en 2021 à l'Université de Strasbourg. Il s'agissait d'une étude comparative et quantitative entre deux revues différentes en apparence, mais représentatives de deux mouvements régulièrement assimilés ensemble à la fin des années 1930. L'objectif de ce mémoire était d'analyser l'objet culturel et matériel que représente un périodique afin de démontrer que les différences de formes et de fonds sont influencées par des variations idéologiques fondamentales entre l'irrédentisme fasciste et l'autonomisme corse de l'entre-deux-guerres. Pour ce faire, je me suis aidé d'une [base de données](https://heurist.huma-num.fr/heurist/?db=vsp_presse_corsiste_irredentiste&w=a&q=sortby%3A-m) particulièrement fournie qui pourrait se révéler utile pour la suite. Je me suis ensuite posé diverses questions sur l'anonymat des nombreux auteurs et articles. Dans le cadre de ce nouveau mémoire de recherche du master "Humanités numériques et computationnelles", de l'école nationale des Chartes, mon objectif est de déterminer quels sont les auteurs se dissimulant derrière un pseudonyme dans la signature d'articles en employant la stylométrie en langue corse. Pour le moment, mes sources sont les éditions du journal régionaliste de l'entre-deux-guerres *A Muvra* ainsi que les almanachs consécutifs de ces publications, imprimés par la *Stamparia di A Muvra* et dirigés par le sulfureux Petru Rocca.

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

Dans l'ensemble, le script fonctionne bien même s'il y a parfois quelques petites erreurs qu'il faut corriger manuellement en téléchargeant en ligne directement les images manquantes.

***À suivre***

### Traitement des images

L'étape suivante est de traiter les images à l'aide du logiciel ScanTailor en rognant les images au textes et en binarisant. Pour cela, j'ai écrit un script qui permet de trier les images obtenues par l'étape précédente en fonction de leur numéro (voir le script `sorted_images` dans le dossier `rename_files`), c'est-à-dire réunir les pages 1, 2 et 3 entre elles, en les renommant en fonction de leur identifiant ARK.

L'étape de ScanTailor est nécessaire car il s'agit d'améliorer la qualité de l'image afin que l'étape de transcription se déroule bien. L'idée est donc de binariser avec la méthode Otsu (paramétrée en 30-Thicker). En sortie, nous avon des images en noir et blanc avec un contrast plus net pour faciliter la détection optique des caractères mais aussi les séparateurs de colonne des journaux.


### Transcription automatique des textes : *recognition*


Pour la transcription des textes, je comptais utiliser le logiciel [eScriptorium](https://traces6.paris.inria.fr/) développé par l'Inria et le laboratoire [ALMAnaCH](https://files.inria.fr/almanach/index-en.html). Son interface intuitive permet de délimiter aisément des blocs de transcription, très utile pour la presse. J'ai d'abord essayé de transcrire mes textes à l'aide du modèle [*Modèle manuscrit DAHN NFC*](https://github.com/HTR-United) développé par Floriane Chiffoleau et trouvé sur le dépôt GitHub [HTR-United](https://github.com/HTR-United/dahncorpus). Néanmoins, se révélant finalement peu efficace dans le cadre de presses écrites en langue corse, je me suis orienté vers le modèle *19th century prints - HTRcatalogs Artlas* sous les conseils de Jean-Baptiste Camps. Bien plus efficace que le précédent, celui-ci semblait être une bonne source de travail pour entraîner un nouveau modèle propre aux presses corses afin d'avoir un taux d'efficacité optimal.

Néanmoins, la difficulté que j'ai eu pour entraîner un modèle de segmentation efficace m'handicapait et me faisait perdre du temps. j'ai pris la décision de basculer sur `tesseract-ocr` qui, en plus de posséder un module de transcription corse, permetd de compiler différentes langues notamment pour les textes écrits en plusieurs langues. J'ai créé un fichier `.bash` qui me permet de lancer automatiquement les commandes `tesseract` dans le terminal. Pour les almanachs, la transcription se fait en plusieurs étapes :

```bash
pdftoppm -r 300 -tiff texte.pdf texte
```

Cette commande permet de fragmenter en plusieurs autant de documents IIIF qu'il y a de pages dans un PDF. En effet, `tesseract` ne peut pas traiter un document unique et cette étape semble donc essentielle.

```bash
pdftoppm -r 300 -tiff *.pdf document
for f in *.tif; do
	tesseract $f $(basename $f .tiff) -l fra+cos+ita
	tesseract $f $(basename $f .tiff) -l fra+cos+ita alto
done
cat *.txt > document-total.txt
```

Cette dernière étape permet de transcrire tous les documents `.tif` grâce à une boucle et d'avoir en *output* un fichier `.txt` avec la transcription ainsi qu'un fichier XML/ALTO. Enfin, on prend la décisions de concaténer tous les documents en un seul, plus utile pour le nettoyage du texte.


### Transcription automatique des textes : *layout analysis*

Si les modèles de reconnaissance de caractères se montrent très prometteurs dans les résultats obtenus, que ce soient des modèles Kraken ou Tesseract, la vraie difficulté se trouve ailleurs. Les sources de presse ont des mises en pages complexes qui diffèrent des ouvrages "classiques", entendez ici des pages de textes avec une colonne unique ou deux au maximum. Le modèle de segmentation de base sur eScriptorium se trouve être très peu performant pour mes sources ce qui nécessiteraient l'entraînement d'un nouveau modèle adapté. Il semblerait que ce problème des *complex layout analysis* ait déjà été traité mais il est difficile de trouver des *dataset* de modèles dispoinibles facilement en ligne. On peut notamment noter l'initiative de *Library of Congress* et du [*Newspaper Navigator*](https://news-navigator.labs.loc.gov/).

Ce problème est le même pour Tesseract-OCR, qui suit un modèle de segmentation basique de détection des lignes successives : très efficace pour les textes ayant qu'une seule colonne. Il semblerait néanmoins qu'il existe des paramètres de modifications des PSM (*Page Segmentation Modes*) afin de prendre en compte différentes mises en page.

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

## Statistiques exploratoires

### Premiers résultats avec *R* : analyse de deux corpus

***Principe***

L’objectif était d’évaluer les évolutions grammaticales de deux corpus de textes originaires d’époques différentes. Le premier est composé de plusieurs textes variés publiés dans les années 1920 par la Stamparia di a Muvra, organe de publication des « muvristes ». Le second corpus est une traduction contemporaine du *Comte de Monte Cristo* disponible sur le site de la revue dialectale [*Tempi Rivista*](https://tempicorsica.com/). Les textes sont variés et abordent des thèmes et styles différents, mais notre travail se concentrait essentiellement sur les mots-outils donc cela n’est, en principe, pas un problème pour nous. À terme, nous voulions savoir sous quelles formes prennent les évolutions grammaticales les plus basiques en 100 ans d’écriture de la langue corse.

***Méthodologie et limites***

Dans un premier temps, il était nécessaire de nettoyer correctement nos textes. Pour cela, j’ai créé une fonction `clean_text` qui, à l’aide d’expressions régulières, se débarrassait de la ponctuation et de la casse. Cette fonction sert également à normaliser les textes de deux manières :

— Une normalisation de l’encodage, les textes provenant pour certains d’eScriptorium, l’unicode n’est pas forcément respecté, particulièrement au niveau des accents, faussant ainsi les résultats.

— une normalisation de l’écriture, les textes anciens (OLD) ayant une graphie différente des textes contemporains (NEW). Par exemple, le verbe être à la 3 e personne du singulier s’écrit soit « è » ou soit « hè ».

Les 8 textes sont ensuite divisés en deux dossiers pour former les deux corpus différents, qui seront par la suite importer dans RStudio. Séparer les deux corpus est très important car nous sommes dans le cadre d’une étude comparative : si le script peut en effet être plus long et moins écologique, cela reste la manière la plus efficace de comparer deux dataset entre eux. Dans la première phase de notre analyse, j’ai créé une *dataframe* qui contient le nombre de caractères totaux de chacun des corpus puis le nombre de mots une fois la tokénisation effectuée. J’ai ensuite fait le choix de calculer le nombre de caractères moyens par mots, élément intéressant pour déterminer s’il y a un phénomène de littérarisation de la langue corse ou non. nous observerons les résultats obtenus dans notre troisième partie. Une fois ce premier tableau effectué, qui compare des données relativement basiques des deux corpus, il a fallu calculer les fréquences de mots, ce qu’on appelle les MFW (*Most Frequent Words*). C’est à cette étape que la constitution de deux corpus différents prend tout son sens. J’ai donc créé deux objets *dataframes* comportant les 15 MFW de chaque corpus avec leur fréquence absolue et leur taux en pourcentage donnant en sortie deux histogrammes. Enfin, dans une dernière étape, j’ai effectué une réduction de dimension du calcul de la fréquence des mots afin de produire une matrice de correspondance du taux de fréquence de chacun desdits mots dans les textes du corpus. Cela permet ensuite de visualiser ces résultats à travers une heatmap classifiée par des dendrogrammes permettant de repérer des groupes de mots plus ou moins utiliser dans les corpus. La métrique utilisée pour réaliser ces dendrogramme est la distance euclidienne, la métrique de base proposée par RStudio. Durant cette étude, j’ai fait face à quelques problèmes et découvert les limites d’une telle méthodologie. D’abord, j’ai eu des difficultés à effectuer la réduction dimensionnelle, les matrices en sortie n’étant pas totalement satisfaisantes selon moi, même si la projection de données me semble relativement cohérente.

Ensuite, le corpus a présenté deux problèmes qui tendent à légèrement fausser les résultats : d’abord vis-à-vis des différences de graphies évoquées précédemment, comme la négation « ùn » où l’accentuation n’est pas présente dans les textes anciens, causant une ambiguïté par homonymie syntaxique avec le déterminant cardinal « un » ; d’où la limite d’avoir un texte non lemmatisé car le contexte ne peut être pris en compte pour marquer la différence. Puis d’un point de vue sémantique, les textes anciens sont variés, allant de la monographie à la poésie, alors que les textes contemporains sont une traduction. L’usage fait des mots-vides n’est pas forcément le même et donc leur quantité peut varier suivant le type de texte. Enfin, certains textes provenant d’un processus d’océrisation, il peut y avoir des déchets de transcriptions provoquant du bruit dans mes corpus, d’où le besoin de nettoyer une deuxième fois le texte. Ceci étant dit, cela ne doit pas avoir modifié les résultats finaux.

***Interprétation des résultats***

La première phase du script nous a permis d’obtenir ce tableau comparatif des caractéristiques globales des deux corpus :

![](/statistiques_exploratoires/analyse_gramm_1_siecle/images/tableau.png)

![](/statistiques_exploratoires/analyse_gramm_1_siecle/images/histo.png)

![](/statistiques_exploratoires/analyse_gramm_1_siecle/images/heatmap.png)

Le tableau 1 permet de nous rendre compte que, pour un texte de taille relativement équivalente, les mots sont en moyenne 10% plus long dans les textes anciens que dans les textes contemporains. Cela peut s’expliquer peut-être par le genre de textes, comme nous avons vu précédemment, ou alors dans la volonté de littérarisation d’une langue principalement orale dans les années 1920, en cherchant à complexifier le langage pour la rendre crédible. Ce constat est hypothétique évidemment, mais correspond néanmoins à une forme de réalité du terrain avec la floraison de nombreux romans et nouvelles en langue corse à l’entre-deux-guerres alors que le corse contemporain s’écrit davantage dans la vie quotidienne, poussant les auteurs de nos jours à, peut-être, adopter des pratiques orthographiques et grammaticales moins complexes. Selon les figures 1, le mot le plus utilisé dans le corpus OLD est l’article « di » alors que la forme conjuguée du verbe esse « hè » est le terme le plus employé dans le corpus NEW. Les différences entre les deux corpus ne se font pas uniquement au niveau des mots-outils en euxmêmes. Les graphiques nous montrent également une plus grande homogénéité dans l’utilisation des différents mots-outils de la langue corse dans les textes contemporains. À l’inverse, les textes anciens utilisent essentiellement 4 mots : « a », « di », « u », « e ». Encore une fois, faisons attentions aux ambiguïtés induisent par une graphie plus simpliste à l’époque de l’entre-deuxguerres. Les figures 2 appuient encore plus ce résultat, les heatmap permettent de mettre en valeur plus clairement deux groupes principaux d’emploi des stopwords dans chaque corpus grâce à la classification ascendante hiérarchique des mots-outils.