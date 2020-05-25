## Table des matière

- [Animanga](#animanga)
  - [Table des versions](#table-des-versions)
  - [Résumé de l'énoncé](#résumé-de-lénoncé)
  - [Organisation](#organisation)
  - [Livrable](#livrable)
  - [Matériel et logicles à disposition](#matériel-et-logicles-à-disposition)
  - [Descriptif complet du projet](#descriptif-complet-du-projet)
    - [Sitemap](#sitemap)
    - [Description succinte du contenu des pages du site](#description-succinte-du-contenu-des-pages-du-site)
  - [Méthodologie](#méthodologie)
    - [1. S’informer](#1-sinformer)
    - [2. Planifier](#2-planifier)
    - [3. Décider](#3-décider)
    - [4. Réaliser](#4-réaliser)
    - [5. Contrôler](#5-contrôler)
    - [6. Évaluer](#6-évaluer)

<div style='page-break-after: always; break-after: page; text-align:right;'></div>

## Table des versions

| N° de version | Date       | Auteur                                    | Modifications                           |
| ------------- | ---------- | ----------------------------------------- | --------------------------------------- |
| 0.1           | 2020-25-05 | Tanguy Cavagna \<<tanguy.cvgn@eduge.ch>\> | Création de la base de la documentation |


## Résumé de l'énoncé

*Les informations suivantes sont éxtraites du cahier des charges du TPI.*

## Organisation

| Éléve                                     | Maître d'apprentissage                   | Experts                                                      |
| ----------------------------------------- | ---------------------------------------- | ------------------------------------------------------------ |
| Tanguy Cavagna \<<tanguy.cvgn@eduge.ch>\> | Pascal Bonvin \<<edu-bonvinp@eduge.ch>\> | Nicolas Terrond \<<nicolas.terrond@sig-ge.ch>\><br />Robin Bouille \<<robin.bouille@gmail.com>\> |

## Livrable

<table>
    <thead>
        <tr>
            <th>Pour les experts et le formateur</td>
            <th>Pour le formateur</td>
        </tr>
    </thead>
	<tbody>
        <tr>
            <td>Planning réel détaillé du projet</td>
            <td rowspan="4">Accès au GitHub</td>
        </tr>
        <tr>
            <td>Documentation du projet contenant le code source au format PDF</td>
        </tr>
        <tr>
            <td>Journal de bord</td>
        </tr>
        <tr>
            <td>Résumé du TPI (1 page A4)</td>
        </tr>
	</tbody>
</table>

## Matériel et logicles à disposition

* Un PC standard école, 2 écrans
* Pycharm
* Netbeans
* Suite office
* MySQl, Sqlite3, Flask, connexion internet

## Descriptif complet du projet

Lorsqu’il s’agit de réaliser un site web, la tradition de l’école d’informatique encourage l’utilisation de PHP et Mysql. Dans le cas de ce diplôme, il s’agit de réaliser un site local avec Python Flask et de gérer les données dans une base de données Sqlite3. De plus la base de donnée locale est synchronisée unidirectionnelement avec une base de donnée Mysql sur un serveur distant. L’ambition de ce projet est de démontrer qu’il est possible de créer un application WEB sans passer par l’installation d’un serveur apache et d’une base données Mysql. A noter que le candidat est un élève brillant qui maîtrise le langage Python.

Les données initiales qui permettront de remplir la base de données sont accessibles sur github au format json (https://github.com/manami-project/anime-offline-database). Elles devront être converties et synchronisées dans la base de données locale qui reste à déterminer.

### Sitemap

![](https://i.loli.net/2020/05/25/Ii93wL5DjEHexbY.png)

### Description succinte du contenu des pages du site

* La page index permet d'avoir le champ de recherche, un bouton "aléatoire", ainsi que les favoris de l'utilisateur et son flux d'activité si connecter.
* La page à propos contient toutes les informations concernant le site ainsi que les librairies utilisées.
* La page connexion permet simplement de se connecter.
* La page inscription, de s'inscrire.
* La page anime / manga permet de voir les informations / actions sur un anime / manga sélectionner (rediriger sur cette page lorsque l'on clique sur un anime / manga sur la page index après une recherche).
* La page aide contient l'aide du site.
* La page profil contient les information de l'utilisateur ainsi que les listes personnelles, dans lesquelles des animes / manga peuvent être ajoutés, ainsi que leur contenu.
* La page favoris permet de modifier l'ordre des animes / manga mit en favoris ainsi que de les retirer de la liste des favoris.
* La page liste contient un CRUD sur les listes personnelles de l'utilisateur.


## Méthodologie

Pour pouvoir planifier correctement ce projet, j'ai décidé d'utilisé la méthode en 6 étapes, décrite ci-dessous :

![Méthode en 6 étapes](https://i.imgur.com/Zi6VG92.png)

### 1. S’informer

La première étape est utile pour pouvoir comprendre le projet dans son ensemble et comprendre toutes les fonctionnalisées nécessaires. Il est aussi indispensable de demander d’éclaircir tous les points flous de l’énoncé.

### 2. Planifier

Le fait de planifier le projet permet de séparer les tâches et de définir des priorités. ses dernières sont les suivantes : 🚫 *Bloquant*, 💥 *Critique*, ❗ *Important*, ❓ *Secondaire*.

Pour représenter le planning nous avons utilisé un diagramme de Gantt. Ce type de diagramme permet de visualiser très correctement la progression quotidienne ainsi que les différences entre les prévisions et le réel.

### 3. Décider

Cette partie nous permet de pouvoir se lancer dans la réalisation du projet. S’il nous reste des points en suspens, c’est le moment de prendre une décision et de se jeter à l’eau une bonne fois pour toute.  

### 4. Réaliser

Nous pouvons enfin nous lancer dans l’implémentation de toutes les fonctionnalités à développer ainsi que la rédaction de la documentation.

### 5. Contrôler

Pour valider cette étape, nous avons tester chacune des fonctionnalités indépendamment des autres pour correctement vérifier leur fonctionnement dans différents cas d’usage.

Une fois l’application terminée, nous avons pu tester son bon fonctionnement sur plusieurs navigateurs différents pour bien être sûre que tout fonctionne comme prévu dans n’importe quel cas d’utilisation.

### 6. Évaluer

Une fois toutes les étapes précédentes achevées, nous avons pu nous lancer dans ce qui peut sembler le plus complexe. Nous avons fait une rétrospective de tout ce que nous avons fait avec un regard critique afin de chercher des points sur lesquels nous pourront nous améliorer par la suite. Pour ce faire, nous avons une section dédiée dans le journal de bord répertoriant les problèmes rencontré ainsi que les solutions trouvées pour ces derniers. Une conclusion est aussi présente à la fin de ce rapport servant de bilan final au projet.



| Nom                            | S1 : Inscription à Animanga                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur non connecté, je peux me créer un compte afin de pouvoir accéder au site. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                                                                  |
| **Priorité**                   | 🚫 Bloquant                                                                                      |

| Nom                            | S2 : Connexion à Animanga                                    |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur non connecté, je peux me connecter afin de pouvoir accéder au site. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | 🚫 Bloquant                                                   |

| Nom                            | S3 : Importation des animes                                  |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux écraser les animes avec un nouveau set de données. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | 💥 Critique                                                   |

| Nom                            | S4 : Rechercher des animes                                   |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux effectué une recherche afin d'ajouter des animes dans mes listes personnelles ou de les mettre en tant que *favoris*. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | 💥 Critique                                                   |

| Nom                            | S5 : Affichage de la carte d'un anime                        |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux cliquer sur le titre d'un anime présent dans les résultats de ma présédente recherche afin d'accéder à ses informatinos. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | ❗ Important                                                  |

| Nom                            | S6 : Mise à jour d'un anime                                  |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux mettre à jour le statut, l'appartenance à une liste personnel ainsi que le statut de favoris d'un anime. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | ❗ Important                                                  |

| Nom                            | S7 : Affichage du profile                                    |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux avoir accès à ma page de profile afin de pourvoir voir les statistiques et favoris. Il est également possible de voir la page de profile d'autre utilisateur du site. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | ❗ Important                                                  |

| Nom                            | S8 : Affichage des listes                                    |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux avoir accès à ma page de listes afin de voir toutes mes listes et leur contenu. Il est également possible de voir les listes d'autre utilisateur du site. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | ❗ Important                                                  |

| Nom                            | S9 : Gestion des listes                                      |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux gérer mes propres listes pour en ajouter, en supprimer, ou modifier leur nom. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | ❗ Important                                                  |

| Nom                            | S10 : Affichage des favoris                                  |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux avoir accès à ma page favoris afin de voir tout mes favoris. Il est également possible de voir les favoris d'autre utilisateur du site. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | ❗ Important                                                  |

| Nom                            | S10 : Gestion des favoris                                    |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur connecté, je peux organiser l'ordre de mes favoris selon mes envies. |
| **Critère d'acceptation**      | ***Pas encore écris de tests\***                             |
| **Priorité**                   | ❗ Important                                                  |

| Nom                            | S11 : Affichage de la *landing page*                         |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant qu'utilisateur non connecté, je n'ai ni accès aux animes ni aux listes. La barre de navigation m'affiche un lien pour me connecter et un autre pour m'inscrire. |
| **Critère d'acceptation**      | ***Pas encore écris de tests***                              |
| **Priorité**                   | ❓ Secondaire                                                 |

| Nom                            | S12 : Utilisation d'un git                                   |
| ------------------------------ | ------------------------------------------------------------ |
| **Description (*user story*)** | En tant que développeur, je dois pouvoir faire du versionnage de code source et pouvoir accéder à un dépôt distant Github. |
| **Critère d'acceptation**      | Le dépôt git local est configurer correctement et le lien sur le dépôt distant à été bien fait. |
| **Priorité**                   | 🚫 Bloquant                                                   |