import psycopg2
import datetime
from business_model.like import Like
from dao.abstract_dao import AbstractDao

class LikeDao(AbstractDao):

    def create(self, like):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO liker (id_user1, date_like, id_user2)"
                "VALUES (%s, %s, %s);",
                (like.id_user1, like.date_like, like.id_user2))



            # la transaction est enregistrée en base
            AbstractDao.connection.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()

        return like

    def delete(self, like):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "delete from liker where id_user1=%s and id_user2=%s ", (like.id_user1,like.id_user2,))

            # la transaction est enregistrée en base
            AbstractDao.connection.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()

    def liste_des_likes(self, id_user1):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select utilisateur.pseudo from utilisateur where id_user In (select distinct liker.id_user2 from liker where liker.id_user1 = %s and type_like=FALSE )",(id_user1,)) # ne pas oublier la virguleapres id_user1 sinon l'expr est indexe
            found = list(cur.fetchall())

            if found:
                liste=list()
                for i in found :
                    liste.append(i[0])
                joinRequests = set(liste)
                return joinRequests

            return None



    def info_verification(self, id_user1,id_user2):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "select * from liker where id_user1=%s and id_user2=%s and type_like = FALSE ", (id_user1,id_user2))

            found = cur.fetchone()
            if found:
                #cur.execute(
                 #   "update liker set type_like = TRUE where id_user1=%s and id_user2=%s", (id_user2,id_user1))
                return Like(found[0],found[1], found[2], found[3])

            return None


    def llike_reciproque(self,id_user1,id_user2):
        with AbstractDao.connection.cursor() as cur:
            cur.execute(
                "update liker set type_like = %s where id_user1=%s and id_user2=%s ;", ("TRUE",id_user1,id_user2,))
            return None


    def like_reciproque(self,id_user1,id_user2):
        cur = AbstractDao.connection.cursor()
        try:
            cur.execute(
                "update liker set type_like = %s where id_user1=%s and id_user2=%s ;", ("TRUE",id_user1,id_user2,))

            # la transaction est enregistrée en base
            AbstractDao.connection.commit()
        except psycopg2.Error as error:
            # la transaction est annulée
            AbstractDao.connection.rollback()
            raise error
        finally:
            cur.close()

        return print("fin")


if __name__ == "__main__":
    li= LikeDao()
    #like=Like("2","2", datetime.datetime.now())
    print(float(1))
    li.like_reciproque("9","10")



