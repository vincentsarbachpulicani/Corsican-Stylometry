# Stylométrie en langue corse

## Description

Mes recherches commencèrent avec un mémoire de master soutenu en 2021 à l'Université de Strasbourg. Il s'agissait d'une étude comparative et quantitative entre deux revues différentes en apparence, mais représentatives de deux mouvements régulièrement assimilés ensemble à la fin des années 1930. L'objectif de ce mémoire était d'analyser l'objet culturel et matériel que représente un périodique afin de démontrer que les différences de formes et de fonds sont influencées par des variations idéologiques fondamentales entre l'irrédentisme fasciste et l'autonomisme corse de l'entre-deux-guerres. A la suite de cette étude, je me suis posé diverses questions sur l'anonymat des nombreux auteurs et articles. Dans le cadre de ce nouveau mémoire de recherche du master "Humanités numériques et computationnelles", de l'école nationale des Chartes, mon objectif est de déterminer quels sont les auteurs se dissimulant derrière un pseudonyme dans la signature d'articles en employant des méthodes de stylométrie en langue corse.

## *Preprocessing* des données

### Récupération des images de bonne qualité

Mon principal problème en ce début de recherche est l'accessibilité des données et métadonnées inhérentes à mes sources, à savoir la revue corse *A Muvra*. La visionneuse d'archive `THOT` des archives de Corse est difficilement exploitable et la numérisation des journaux à la BNF se termine en 1930. Néanmoins, afin de me constituer un premier corpus, je peux me baser sur les documents disponibles `gallica`. 

Afin d'exploiter des images de bonnes qualité avant d'opérer une phase d'océrisation, j'ai décidé de récupérer des images IIIF en haute résolution. Phase à certains problèmes de normalisation du nombre d'images en IIIF disponibles pour chaque numéro du journal, j'emploie le script `IIIF-Crawler`, développé par Thibault Clérice et Jean-Baptiste Camps. Cela me permet aussi, à termes, de ppuvoir importer un nombre conséquent d'images de bonne qualité automatiquement.