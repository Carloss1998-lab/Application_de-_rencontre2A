from vue.abstract_vue import AbstractVue
from PyInquirer import Separator, prompt
from dao.compte_dao import CompteDao


questions = [
    {
        'type': 'list',
        'name': 'menu2',
        'message': 'Bonjour',
        'choices': [
            'Accéder à son profil',
            Separator(),
            'Accéder à la messagerie',
            Separator(),
            'Accéder onglet des matchs',
            Separator(),
            'Se déconnecter',
            Separator(),
            'Supprimer son compte',

        ]
    }
]

compte = CompteDao()

class MenuOnglet(AbstractVue):

    def display_info(self):
        with open('assets/banner.txt', 'r', encoding="utf-8") as asset:
            print(asset.read())

    def make_choice(self,id_user):
        reponse = prompt(questions)
        if reponse['menu2'] == 'Accéder à son profil':
            return compte.Voirprofil(id_user)
        elif reponse['menu2'] == 'Accéder à la messagerie':
            pass
        elif reponse['menu2'] == 'Accéder onglet des matchs':
            pass
        elif reponse['menu2'] == 'Se déconnecter':
            pass
        elif reponse['menu2'] == 'Supprimer son compte':
            pass

