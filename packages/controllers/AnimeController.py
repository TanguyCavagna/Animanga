"""Contient la classe de contrôle des animes

@author: Tanguy Cavagna
@copyright: Copyright 2020, TPI
@version: 1.0
@date: 2020-05-26
"""
import json
import pathlib
#import sys
#import os
from sqlite3 import Error as SqliteError
from datetime import datetime as dt
from random import randint

from .SqliteController import SqliteController
from .TypeController import TypeController
from .StatusController import StatusController
from .ListController import ListController
from ..models.Anime import Anime
from .logger import log

class AnimeController:
    """Controlleur d'un anime
    """

    #pylint: disable=too-many-return-statements
    @classmethod
    def override_local_with_json(cls, path: str) -> None:
        """Écrase toutes les données en base

            Arguments:
                path {string} -- Chemin du fichier json
        """
        with open(pathlib.Path(__file__).parent / path, 'r', encoding="utf8") as f:
            animes = json.load(f)

        try:
            # Mise en place des tables si elles ne sont pas présente et truncate tout ce qui est en lien direct avec la table 'anime'
            if not SqliteController().setup_type_table(): return False
            if not SqliteController().setup_status_table(): return False
            if not SqliteController().setup_anime_table(): return False
            if not SqliteController().setup_url_table(): return False
            if not SqliteController().setup_user_table(): return False
            if not SqliteController().setup_list_table(): return False
            if not SqliteController().setup_user_has_list_table(): return False
            if not SqliteController().setup_list_has_anime_table(): return False
            if not SqliteController().setup_user_has_favorite_table(): return False
            if not SqliteController().truncate_anime_related(): return False

            # Requêtes pour les insertions de nouvelles données
            sql_query_type = "INSERT INTO type(nameType, modificationDate) VALUES(?, ?)"
            sql_query_status = "INSERT INTO status(nameStatus, modificationDate) VALUES(?, ?)"
            sql_query_anime = "INSERT INTO anime(idAnime, title, type, episodes, status, picture, thumbnail, synonyms, modificationDate) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
            sql_query_anime_ft = "INSERT INTO anime_ft(idAnime, title) VALUES(?, ?)"
            sql_query_url = "INSERT INTO url(urlName, idAnime, isRelation, modificationDate) VALUES(?, ?, ?, ?)"

            # Tableaux ayant pour but de stocké les futures valeurs à mettre dans les table pour faire un insert_many
            values_type = []
            values_status = []
            values_anime = []
            values_anime_ft = []
            values_source = []
            values_relation = []

            current_time = dt.now().strftime('%Y-%m-%d %H:%M:%S')

            yield "Récupération des types et statuts"

            # Récupération des statuts et des types
            for anime in animes['data']:
                # Suppression de tout les OVA car souvent ayant un contenu innaproprié pour un TPI
                if anime['type'] == 'OVA':
                    continue
                
                # Ajout distinct des types
                if not any(anime['type'] in i for i in values_type):
                    values_type.append((
                        anime['type'],
                        current_time
                    ))

                # Ajout distinct des statuts
                if not any(anime['status'] in i for i in values_status):
                    values_status.append((
                        anime['status'],
                        current_time
                    ))

            yield "Insertion des types et status"
            SqliteController().execute_many(sql_query_type, values_type)
            SqliteController().execute_many(sql_query_status, values_status)

            yield "Récupération des animes et urls"
            types = TypeController().get_all_as_dict()
            status = StatusController().get_all_as_dict()

            # Reparcourir le fichier json pour extraire cette fois si les animes et leurs relations
            idAnime = 1
            for anime in animes['data']:
                # Suppression de tout les OVA car leur contenu est souvent innaproprié pour un TPI
                if anime['type'] == 'OVA':
                    continue

                values_anime.append((
                    idAnime,
                    anime['title'],
                    types[anime['type']],
                    anime['episodes'],
                    status[anime['status']],
                    anime['picture'],
                    anime['thumbnail'],
                    ','.join(anime['synonyms']) if len(anime['synonyms']) > 0 else None,
                    current_time
                ))

                values_anime_ft.append((
                    idAnime,
                    anime['title']
                ))

                for source in anime['sources']:
                    values_source.append((
                        source,
                        idAnime,
                        False,
                        current_time
                    ))

                for relation in anime['relations']:
                    values_relation.append((
                        relation,
                        idAnime,
                        True,
                        current_time
                    ))

                idAnime += 1

            yield "Insertion des animes et urls"
            SqliteController().execute_many(sql_query_anime, values_anime)
            SqliteController().execute_many(sql_query_anime_ft, values_anime_ft)
            SqliteController().execute_many(sql_query_url, values_source)
            SqliteController().execute_many(sql_query_url, values_relation)

            yield "redirect"
            return True
        except SqliteError as e:
            log(e)
            return False

    @classmethod
    def __encapsulate_animes(cls, raw_results: dict) -> [Anime]:
        """Encapsule les résultats d0une requete

            Arguments:
                raw_resutls {dict} -- Résultats provenant de `SqliteController.execute`
            
            Returns:
                [Anime] -- Liste d'anime encapsuler
        """
        return [
            Anime(result['idAnime'],
                  result['title'],
                  result['nameType'],
                  result['episodes'],
                  result['nameStatus'],
                  result['picture'],
                  result['thumbnail'],
                  result['synonyms']
            ) for result in raw_results
        ]

    @classmethod
    def __serialize_encapsulated_animes(cls, encapsulated_animes: list) -> [dict]:
        """Sérialize tout les animes contenu dans une liste d'anime encapsulé

            Arguments:
                encapsulated_animes {list} -- Liste des animes encapsulé

            Returns:
                [dict] -- Liste de tout les animes sérialisé
        """
        return [anime.serialize() for anime in encapsulated_animes]

    @classmethod
    def __get_count(cls) -> int:
        """Retourne le nombre d'anime présent en base

            Returns:
                int -- Nombre d'anime en base
        """
        try:
            sql_count = """SELECT COUNT(*) AS `Count` FROM anime"""

            count = SqliteController().execute(sql_count, fetch_mode=SqliteController.FETCH_ONE)['Count']

            return count
        except SqliteError as e:
            log(e)
            return None

    @classmethod
    def get_from_search_string(cls, search_string: str) -> [Anime]:
        """Retourne les animes concordant avec la chaine de recherche

            Arguments:
                search_string {str} -- Chaine de recherche
            
            Returns:
                [Anime] -- Liste des animes concordant
        """
        try:
            # Le join sur la table virtuelle est obligatoire pour réalisé des recherches fulltext
            sql_search = """SELECT anime.idAnime, anime.title, nameType, episodes, nameStatus, picture, thumbnail, synonyms
                            FROM anime
                            JOIN anime_ft ON anime.idAnime = anime_ft.idAnime
                            JOIN status ON anime.status = status.idStatus
                            JOIN type ON anime.type = type.idType
                            WHERE anime_ft.title MATCH ?
                            LIMIT 9"""

            results = SqliteController().execute(sql_search, values=(search_string,), fetch_mode=SqliteController.FETCH_ALL)

            encapsulated = cls.__encapsulate_animes(results)
            
            return cls.__serialize_encapsulated_animes(encapsulated)
        except SqliteError as e:
            log(e)
            return []

    @classmethod
    def get_relations_by_anime_id(cls, anime_id: int) -> [Anime]:
        """Retourne toutes les relations d'un anime

            Arguments:
                anime_id {int} -- Id de l'anime du quel nous voulons les relations
            
            Returns:
                [Anime] -- Liste de toutes les relations
        """
        try:
            # Cette requete est relativement complexe. Pour avoir toutes les relations d'un anime, voila comment elle procède :
            #   Récupérer toutes les url liée à un anime, récupérer tout les ids des animes ayant des urls référencé comme relation à l'anime principal
            #   et ne pas reprendre une seconde  fois l'anime principale. Ne reste plus qu'à récupérer les informations de ces animes
            sql_relations = """SELECT anime.idAnime, anime.title, nameType, episodes, nameStatus, picture, thumbnail, synonyms
                               FROM anime
                               JOIN status ON anime.status = status.idStatus
                               JOIN type ON anime.type = type.idType
                               WHERE idAnime IN (
                                   SELECT idAnime
                                   FROM url
                                   WHERE urlName IN (
                                       SELECT urlName
                                       FROM url
                                       WHERE idAnime = ?
                                   )
                                   AND isRelation = 1
                                   AND idAnime != ?
                               )"""

            results = SqliteController().execute(sql_relations, values=(anime_id, anime_id,), fetch_mode=SqliteController.FETCH_ALL)

            encapsulated = cls.__encapsulate_animes(results)
            
            return cls.__serialize_encapsulated_animes(encapsulated)
        except SqliteError as e:
            log(e)
            return []

    @classmethod
    def get_random_anime(cls) -> Anime:
        """Récupère un anime aléatoire

            Returns:
                Anime -- Anime tiré aléatoirement
        """
        try:
            sql_select = """SELECT anime.idAnime, anime.title, nameType, episodes, nameStatus, picture, thumbnail, synonyms
                            FROM anime
                            JOIN status ON anime.status = status.idStatus
                            JOIN type ON anime.type = type.idType
                            WHERE idAnime = ?"""

            random_anime_id = randint(1, cls.__get_count())
            
            results = SqliteController().execute(sql_select, values=(random_anime_id,), fetch_mode=SqliteController.FETCH_ONE)

            encapsulated = cls.__encapsulate_animes([results])
            
            return cls.__serialize_encapsulated_animes(encapsulated)[0]
        except SqliteError as e:
            log(e)
            return None

    @classmethod
    def is_anime_in_user_favorite(cls, user_id: int, anime_id: int) -> bool:
        """Retourne si l'anime est dans la liste des favoris de l'utilisateur

            Arguments:
                user_id {int} -- Id de l'utilisateur en question
                anime_id {int} -- Id de l'anime sur lequel tester si il est favoris

            Returns:
                bool -- Est-ce que l'anime est dans les favoris de l'utilisateur
        """
        try:
            sql_is_favorite = """SELECT COUNT(*) AS `Count`
                                 FROM user_has_favorite
                                 WHERE idUser = ?
                                 AND idAnime = ?"""

            results = SqliteController().execute(sql_is_favorite, values=(user_id,anime_id,), fetch_mode=SqliteController.FETCH_ONE)['Count']

            return bool(results == 1)
        except SqliteError as e:
            log(e)
            return False

    @classmethod
    def is_anime_in_list(cls, anime_id: int, list_id: int) -> bool:
        """Est-ce que l'anime est dans la liste

            Arguments:
                anime_id {int} -- Id de l'anime
                list_id {int} -- Id de la liste
            
            Returns:
                bool -- Est-ce que l'anime est dans la liste
        """
        try:
            sql_is_in_list = """SELECT COUNT(*) AS `Count`
                                FROM list_has_anime
                                WHERE idAnime = ?
                                AND idList = ?"""

            results = SqliteController().execute(sql_is_in_list, values=(anime_id,list_id,), fetch_mode=SqliteController.FETCH_ONE)['Count']

            return bool(results == 1)
        except SqliteError as e:
            log(e)
            return False

    @classmethod
    def set_anime_in_user_favorite(cls, user_id: int, anime_id: int) -> bool:
        """Met à jour l'état de favoris d'un anime pour un utiliateur

            Arguments:
                user_isd {int} -- Id de l'utilisateur
                anime_id {int} -- Id de l'anime
            
            Returns:
                bool -- État de favoris de l'anime
        """
        try:
            sql_delete_favorite = """DELETE FROM user_has_favorite
                                     WHERE idAnime = ?
                                     AND idUser = ?"""
            sql_get_last_order_id = """SELECT orderId
                                       FROM user_has_favorite
                                       WHERE idUser = ?
                                       ORDER BY orderId DESC
                                       LIMIT 1"""
            sql_add_favorite = "INSERT INTO user_has_favorite(idAnime, idUser, orderId, modificationDate) VALUES(?, ?, ?, ?)"

            if cls.is_anime_in_user_favorite(user_id, anime_id):
                SqliteController().execute(sql_delete_favorite, values=(anime_id,user_id,), fetch_mode=SqliteController.NO_FETCH)

                # Réattribué les orderId

                is_favorite = False
            else:
                last_order_id = SqliteController().execute(sql_get_last_order_id, values=(user_id,), fetch_mode=SqliteController.FETCH_ONE)
                last_order_id = int(last_order_id['orderId']) + 1 if last_order_id is not None else 1
                SqliteController().execute(sql_add_favorite, values=(anime_id,user_id,last_order_id,dt.now().strftime('%Y-%m-%d %H:%M:%S'),), fetch_mode=SqliteController.NO_FETCH)

                is_favorite = True
            
            return is_favorite
        except SqliteError as e:
            log(e)
            return False

    @classmethod
    def get_favorite_by_user_id(cls, user_id: int) -> [Anime]:
        """Récupère tout les favoris d'un utilisateur

            Arguments:
                user_id {int} -- Id de l'utilisateur

            Returns:
                [Anime] -- Liste de tout les favoris
        """
        try:
            sql_favorites = """SELECT anime.idAnime, anime.title, nameType, episodes, nameStatus, picture, thumbnail, synonyms
                               FROM anime
                               JOIN status ON anime.status = status.idStatus
                               JOIN type ON anime.type = type.idType
                               JOIN user_has_favorite ON anime.idAnime = user_has_favorite.idAnime
                               WHERE user_has_favorite.idUser = ?
                               ORDER BY orderId ASC"""

            results = SqliteController().execute(sql_favorites, values=(user_id,), fetch_mode=SqliteController.FETCH_ALL)

            encapsulated = cls.__encapsulate_animes(results)

            return cls.__serialize_encapsulated_animes(encapsulated)
        except SqliteError as e:
            log(e)
            return []

    @classmethod
    def set_anime_in_list(cls, anime_id: int, list_id: int) -> bool:
        """Met à jour l'appartenance d'un anime à une liste

            Arguments:
                anime_id {int} -- Id de l'anime
                list_id {int} -- Id de la liste
        """
        try:
            sql_delete_from_list = """DELETE FROM list_has_anime
                                      WHERE idAnime = ?
                                      AND idList = ?"""
            sql_add_to_list = """INSERT INTO list_has_anime(idAnime, idList, modificationDate)
                                 VALUES(?, ?, ?)"""
            
            if cls.is_anime_in_list(anime_id, list_id):
                SqliteController().execute(sql_delete_from_list, values=(anime_id,list_id,), fetch_mode=SqliteController.NO_FETCH)
                is_in_list = False
            else:
                SqliteController().execute(sql_add_to_list, values=(anime_id,list_id,dt.now().strftime('%Y-%m-%d %H:%M:%S'),), fetch_mode=SqliteController.NO_FETCH)
                is_in_list = True

            return is_in_list
        except SqliteError as e:
            log(e)
            return False

    @classmethod
    def delete_anime_status(cls, user_id: int, anime_id: int) -> bool:
        """Supprime le stats actuel d'un anime pour un utilisateur

            Arguments:
                user_id {int} -- Id de l'utilisateur
                anime_id {int} -- Id de l'anime

            Returns:
                bool -- État de la requete
        """
        try:
            sql_delete = """DELETE FROM list_has_anime
                            WHERE idList IN (?, ?, ?, ?)
                            AND idAnime = ?"""

            default_lists = ListController().get_defaults_for_user(user_id)
            in_clause = [l['id'] for l in default_lists] # Créer un tableau regroupant les ids des listes par défaut
            values = [] + in_clause # Fusionne les deux listes
            values.append(anime_id)

            SqliteController().execute(sql_delete, values=tuple(values), fetch_mode=SqliteController.NO_FETCH)

            return True
        except SqliteError as e:
            log(e)
            return False

    @classmethod
    def get_animes_in_list_for_user(cls, user_id: int, list_id: int, search_terms: str = None) -> [Anime]:
        """Récupère la liste de tout les animes d'une liste

            Arguments:
                user_id {int} -- Id de l'utilisateur
                list_id {int} -- Id de la liste
                search_terms {str} -- Chaine de caractères pour la recherche d'anime dans une liste
            Returns:
                [Anime] -- Liste de tous les animes trouvés
        """
        try:
            animes = {}

            sql_select = """SELECT list.idList, list.nameList, anime.idAnime, anime.title, nameType, list_has_anime.idList, anime.episodes, nameStatus, anime.picture, anime.thumbnail, anime.synonyms
                            FROM anime
                            JOIN anime_ft ON anime.idAnime = anime_ft.idAnime
                            JOIN list_has_anime ON list_has_anime.idAnime = anime.idAnime
                            JOIN user_has_list ON user_has_list.idList = list_has_anime.idList
                            JOIN list ON list.idList = list_has_anime.idList
                            JOIN type ON type.idType = anime.type
                            JOIN status ON status.idStatus = anime.status
                            WHERE user_has_list.idUser = ?"""
            
            if search_terms is not None and search_terms != "":
                sql_select += " AND anime_ft.title MATCH ?"

                if list_id is not None:
                    sql_select += " AND list_has_anime.idList = ?"
                    values = (user_id, search_terms, list_id,)
                else:
                    values = (user_id, search_terms,)
            elif list_id is not None:
                sql_select += " AND list_has_anime.idList = ?"
                values = (user_id, list_id,)
            else:
                values = (user_id,)
            
            sql_select += " ORDER BY list.idList"
            
            rows = SqliteController().execute(sql_select, values=values, fetch_mode=SqliteController.FETCH_ALL)

            # Ajoute les animes dans la bonne liste
            for row in rows:
                new_name = row['nameList']
                if new_name not in animes:
                    animes[new_name] = []
                animes[new_name].append(Anime(row['idAnime'], row['title'], row['nameType'], row['episodes'], row['nameStatus'], row['picture'], row['thumbnail'], row['synonyms']).serialize())

            return animes
        except SqliteError as e:
            log(e)
            return {}

    @classmethod
    def reorder_favorites(cls, user_id: int, ids: list) -> bool:
        """Met à jour l'ordre des animes

            Arguments:
                user_id {int} -- Id de l'utilisateur
                ids {list} -- Liste des ids des animes
        
            Returns:
                bool -- État de la mise à jour
        """
        try:
            sql_update = "UPDATE user_has_favorite SET orderId = ?, modificationDate = ? WHERE idAnime = ? AND idUser = ?"

            order_id = 1
            modification_date = dt.now().strftime('%Y-%m-%d %H:%M:%S')

            for anime_id in ids:
                SqliteController().execute(sql_update, values=(order_id, modification_date, anime_id, user_id,), fetch_mode=SqliteController.NO_FETCH)
                order_id += 1

            return True
        except SqliteError as e:
            log(e)
            return False 
