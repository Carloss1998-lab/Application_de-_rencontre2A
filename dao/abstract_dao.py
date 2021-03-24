
from dao.connection import get_connection


class AbstractDao:
    """Classe abstraite dont les DAO doivent hériter. Permet de gérer simplement la connection, et d'avoir des noms
    méthodes de base des DAO identique. Permet une meilleure lisibilité du code"""

    connection = get_connection()

    def find_by_id(self, id):
        """Va chercher une élément de la base grâce à son id et retourne l'objet python associé"""
        return NotImplementedError

    def find_all(self):
        """Retourne tous les éléments d'une table sous forme de liste d'objets python"""
        return NotImplementedError

    def update(self, business_object):
        """Met à jour la ligne en base de donnée associé à l'objet métier en paramètre"""
        return NotImplementedError

    def create(self, business_object):
        """Insère une ligne en base avec l'objet en paramètre. Retourne l'objet mise à jour avec son id de la base"""
        return NotImplementedError

    def delete(self, business_object):
        """Supprime la ligne en base représentant l'objet en paramètre"""
        return NotImplementedError
