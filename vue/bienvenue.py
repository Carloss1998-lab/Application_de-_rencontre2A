from vue.abstract_vue import AbstractVue
#from Messagerie.codebrut import main
from vue.menuPrincipal import menuPrincipal
from dao.messagerie_dao import MessagerieDao
from vue.menuonglet import MenuOnglet

class Bienvenue(AbstractVue):

    def display_info(self):
        print('Bienvenue {}, content de vous savoir parmi nous !'.format(
            AbstractVue.session.user.pseudo))

        # on démarre sur l'écran accueil
        current_vue = MenuOnglet()
        mess = MessagerieDao()

        # tant qu'on a un écran à afficher, on continue
        while current_vue:
            # on affiche une bordure pour séparer les vue
            with open('assets/border.txt', 'r', encoding="utf-8") as asset:
                print(asset.read())
            # les infos à afficher
            current_vue.display_info()
            # le choix que doit saisir l'utilisateur
            current_vue = current_vue.make_choice(mess.trouver_id_avec_pseudo(AbstractVue.session.user.pseudo))





