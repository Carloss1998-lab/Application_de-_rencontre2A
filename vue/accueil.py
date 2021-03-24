from vue.session import Session
from vue.compte_authentification import Authentification
from vue.compte_creation import CreationCompte
from vue.abstract_vue import AbstractVue
from PyInquirer import Separator, prompt


questions = [
    {
        'type': 'list',
        'name': 'authentification',
        'message': 'Bonjour',
        'choices': [
            'Me créer un compte',
            Separator(),
            'Me connecter',
            Separator(),
            'Quitter'
        ]
}
]

quest = [
    {
        'type': 'confirm',
        'message': 'Voulez-vous vraiment quitter?',
        'name': 'continue',
        'default': True,
    }
]
class Accueil(AbstractVue):

    def display_info(self):
        with open('assets/banner.txt', 'r', encoding="utf-8") as asset:
            print(asset.read())

    def make_choice(self):
        reponse = prompt(questions)
        if reponse['authentification'] == 'Me connecter':
            return Authentification()
        elif reponse['authentification'] == 'Me créer un compte':
            return CreationCompte()
        elif reponse['authentification'] == 'Quitter':
            rep = prompt(quest)
            if rep['continue'] == False:
                return Accueil.make_choice(self)
            else:
                pass

