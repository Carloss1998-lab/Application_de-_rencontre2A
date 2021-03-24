import psycopg2
from business_model.messagerie import Messagerie
from business_model.compte import Compte
from dao.abstract_dao import AbstractDao

class MessagerieDao(AbstractDao):

    def create(self, messagerie):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO message (contenu ,date_envoi, id_expediteur ,id_receveur, lu )"
                "VALUES (%s, %s, %s, %s, %s ) RETURNING id_message;",

                (messagerie.contenu, messagerie.date_envoi, messagerie.id_expediteur, messagerie.id_receveur, messagerie.lu))



            messagerie.id_message = cur.fetchone()[0]
            # la transaction est enregistrée en base
            AbstractDao.connection.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()

        return messagerie

    def delete(self, messagerie):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "delete from messagerie where id_message =%s", (messagerie.id_message,))

            # la transaction est enregistrée en base
            AbstractDao.connection.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()


    def info_verification(self,id_receveur, id_expediteur):
        #ici, je veux verifier si l'utilisateur a déjà une fois communiqué avec le second utilsateur
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select * from message where (id_receveur =%s and id_expediteur=%s) or (id_receveur =%s and id_expediteur=%s)", (id_receveur,id_expediteur,id_expediteur,id_receveur))

            found = cur.fetchone()
            if found:

                print("Existe")
                return found
            return None



    def trouver_id_avec_pseudo(self, pseudo):

        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select id_user,  nom, prenom, email, sexe, age, interesse_par, pays, ville, pseudo,motdepasse,photo_profil, photo_profil1, photo_profil2, description from utilisateur where pseudo=%s", (pseudo,))

            found = cur.fetchone()
            if found:
                user = Compte(found[1],found[2],found[3],found[4],found[5],found[6],found[7],found[8],found[9],found[10],found[11], found[12],found[13], found[14], found[0])
                id_receveur = user.id_user
                return id_receveur


    def liste_des_messageries(self):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select distinct utilisateur.pseudo , utilisateur.pseudo from utilisateur ")
            found = cur.fetchall()

            if found:
                group = {} #transformation des résultats en dictionnaire.
                for k, v in found :
                    group[k] = v
                return group

            return None

    def mes_correspondants(self, id_user1):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select utilisateur.pseudo from utilisateur where id_user In (select distinct message.id_receveur from message where message.id_expediteur = %s and message.id_receveur != message.id_expediteur)",(id_user1,)) # ne pas oublier la virguleapres id_user1 sinon l'expr est indexe
            found = list(cur.fetchall())
            if found:
                liste=list()
                for i in found :
                    liste.append(i[0])
                joinRequests = set(liste)
                return joinRequests

            return None

    def messsage_non_lu(self, id_user1):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select utilisateur.pseudo,message.contenu from utilisateur left join message on message.id_expediteur = utilisateur.id_user where id_receveur= %s and message.lu = 'True'",(id_user1,)) # ne pas oublier la virguleapres id_user1 sinon l'expr est indexe
            found = list(cur.fetchall())
            if found:
                liste=[]
                for i in found :
                    liste[i[0]]= i[1]
                joinRequests = set(liste)
                return liste

            return None

if __name__=="__main__":
    cc = MessagerieDao()
    a = cc.messsage_non_lu(9)
    print(a)