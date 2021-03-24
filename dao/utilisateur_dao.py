import psycopg2
from business_model.compte import Compte
from dao.abstract_dao import AbstractDao

class UtilisateurDao(AbstractDao):

    def create(self, utilisateur):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO utilisateur (self, nom, prenom, email, sexe, age, interesse_par, pays, ville,pseudo, motdepasse, photo_profil, photo_profil1,photo_profil2, description ) "
                "VALUES (%s, %s, %s, %i, %i,%s, %s, %s,%s, %s,%s, %s, %s,%s, ) RETURNING id_user;",

                (utilisateur.nom, utilisateur.prenom, utilisateur.email, utilisateur.sexe, utilisateur.age,
                 utilisateur.interesse_par, utilisateur.pays, utilisateur.ville,utilisateur.pseudo,utilisateur.motdepasse,
                 utilisateur.photo_profil, utilisateur.photo_profil1, utilisateur.photo_profil2,
                 utilisateur.description))



            utilisateur.id_user = cur.fetchone()[0]
            # la transaction est enregistrée en base
            AbstractDao.connection.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()

        return utilisateur

    def delete(self, utilisateur):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "delete from utilisateur where id_user=%s", (utilisateur.id_user,))

            # la transaction est enregistrée en base
            AbstractDao.connection.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()

    def find_by_id(self, id_user):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select id_user, nom, prenom from utilisateur where id_user=%s", (id_user,))

            found = cur.fetchone()
            if found:
                return Utilisateur(found[1], found[2], found[0])

            return None





