
from vue.accueil import Accueil
from vue.menuCreation import menuCreation

if __name__ == '__main__':

    # on démarre sur l'écran accueil
    current_vue = Accueil()

    # tant qu'on a un écran à afficher, on continue
    while current_vue:
        # on affiche une bordure pour séparer les vue
        # le choix que doit saisir l'utilisateur
        current_vue = current_vue.make_choice()


    with open('assets/cat.txt', 'r', encoding="utf-8") as asset:
        print(asset.read())
