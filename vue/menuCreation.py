from business_model.menu_general import MenuDisplay
from vue.compte_authentification import Authentification
from vue.compte_creation import CreationCompte


class menuCreation():

    def make_choice(self):
        menu = [' Inscription', 'Authentification ', 'Quitter']
        elmenu = MenuDisplay(menu)
        choix,long = elmenu.reponse()
        print(choix)
        print(long)
        while 1:
            if choix == 1:
                #print("cc")
                return Authentification()
            elif choix == 0:
                return CreationCompte()
            elif choix == long:
                break




