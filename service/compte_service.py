from dao.compte_dao import CompteDao
from dao.like_dao import LikeDao
from business_model.compte import Compte
from business_model.like import Like
from dao.messagerie_dao import MessagerieDao


class CompteService:
    compte_dao = CompteDao()
    like_dao = LikeDao()
    messagerie_dao = MessagerieDao()

    def pseudo_disponible(self, pseudo, email= None):
        return not(CompteService.compte_dao.find_by_pseudo(pseudo,email))

    def creer_compte(self, nom, prenom, email, sexe, age, interesse_par, pays, ville,pseudo,motdepasse, photo_profil, photo_profil1, photo_profil2, description):
        compte = Compte( nom, prenom, email, sexe, age, interesse_par, pays, ville,pseudo,motdepasse, photo_profil, photo_profil1, photo_profil2, description)
        return CompteService.compte_dao.create(compte)

    def creer_like(self,id_user1,id_user2, date_like):
        like = Like(self,id_user1,id_user2, date_like)
        return CompteService.like_dao.create(like)

    def modifier_like(self,id_user1,id_user2):
        like = Like(self,id_user1,id_user2)
        return CompteService.like_dao.create(like)

    def verification(self, pseudo, motdepasse):
        return not(CompteService.compte_dao.info_verification(pseudo,motdepasse))

    def like_disponible(self, id_receveur, id_expediteur):
        return not(CompteService.like_dao.info_verification(id_receveur, id_expediteur))

    def verification_match_deja(self, id_receveur, id_expediteur):
        return not(CompteService.messagerie_dao.info_verification(id_receveur, id_expediteur))

