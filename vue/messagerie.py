from dao.abstract_dao import AbstractDao


def info_verification(self,id_receveur):
    #ici, je veux verifier si l'utilisateur a déjà une fois communiqué avec le second utilsateur
    with AbstractDao.connection.cursor() as cur:
        cur.execute(
            "select * from message where id_receveur =%s and motdepasse=%s", (id_receveur,))

        found = cur.fetchone()
        if found:
            print("")

        return None
