import psycopg2
from business_model.compte import Compte
from dao.abstract_dao import AbstractDao

class CompteDao(AbstractDao):

    def create(self, utilisateur):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO utilisateur (nom, prenom, email, sexe, age, interesse_par, pays, ville,pseudo, motdepasse, photo_profil, photo_profil1,photo_profil2, description )"
                "VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s ) RETURNING id_user;",

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
                return Compte(found[1], found[2], found[0])

            return None



    def find_by_pseudo(self, pseudo,email= None):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select id_user,  nom, prenom, email, sexe, age, interesse_par, pays, ville, pseudo,motdepasse,photo_profil, photo_profil1, photo_profil2, description from utilisateur where pseudo=%s or email=%s", (pseudo,email,))

            found = cur.fetchone()
            if found:
                return Compte(found[1],found[2],found[3],found[4],found[5],found[6],found[7],found[8],found[9],found[10],found[11], found[12],found[13], found[14], found[0])

            return None


    def info_verification(self,pseudo,motdepass):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select id_user,  nom, prenom, email, sexe, age, interesse_par, pays, ville, pseudo,motdepasse,photo_profil, photo_profil1, photo_profil2, description from utilisateur where pseudo=%s and motdepasse=%s", (pseudo,motdepass,))

            found = cur.fetchone()
            if found:
                compte = Compte(found[1],found[2],found[3],found[4],found[5],found[6],found[7],found[8],found[9],found[10],found[11], found[12],found[13], found[14], found[0])
                return compte
            #return None


    def Voirprofil(self,motdepass):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select  nom, prenom, email, sexe, age, interesse_par, pays, ville, pseudo,photo_profil, photo_profil1, photo_profil2, description from utilisateur where id_user=%s", (motdepass,))

            found = list(cur.fetchone())
            libelle= ["nom", "prenom", "email", "sexe", "age", "interesse_par", "pays", "ville","pseudo","photo_profil", "photo_profil1", "photo_profil2", "description"]

            for i in range(len(found)):
                print("___________________________________________________")
                print('|{0:15}| : |{1:30}|\n '.format(libelle[i], found[i]))

            print("__________________________________________________")

    def modifier(self, utilisateur):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "UPDATE utilisateur nom =%s , prenom =%s, email=%s, sexe=%s, age=%s, interesse_par=%s, pays=%s, ville=%s,pseudo=%s, motdepasse%s=, photo_profil=%s, photo_profil1=%s,photo_profil2=%s, description=%s where id_user =%s )"
                "VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s ) RETURNING id_user;",

                (utilisateur.nom, utilisateur.prenom, utilisateur.email, utilisateur.sexe, utilisateur.age,
                 utilisateur.interesse_par, utilisateur.pays, utilisateur.ville,utilisateur.pseudo,utilisateur.motdepasse,
                 utilisateur.photo_profil, utilisateur.photo_profil1, utilisateur.photo_profil2,
                 utilisateur.description, utilisateur.id_user))


        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()

        return utilisateur

            #return None
