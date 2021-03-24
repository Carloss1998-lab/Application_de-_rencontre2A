from business_model.menu_general import MenuDisplay
from dao.compte_dao import CompteDao


compte = CompteDao()

class menuPrincipal():

    def make_choice(self,id_user):
        menu = [' Accéder à son profil', 'Accéder à la méssagerie ', 'Accéder à l\'onglet des matchs', 'Se déconnecter',
                'Supprimer son compte', 'Quitter']
        elmenu = MenuDisplay(menu)
        choix,long = elmenu.reponse()
        while 1:
            if choix == 0:
                return compte.Voirprofil(id_user)
            elif choix == 1:
                pass
            elif choix == 2:
                pass
            elif choix == 3:
                pass
            elif choix == 4 :
                pass
            elif choix == long:
                break

