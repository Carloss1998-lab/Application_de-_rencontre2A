from PyInquirer import prompt, Validator, ValidationError
from dao.compte_dao import CompteDao
from service.compte_service import CompteService
from vue.abstract_vue import AbstractVue
from vue.bienvenue import Bienvenue
from vue.chiffrermotdepasse import ChiffrerMotDePasse


class PasswordValidator(Validator):
    def validate(self, document):
        ok = len(document.text) > 5
        if not ok:
            raise ValidationError(
                message='Votre mot de passe doit faire au moins 6 caractères',
                cursor_position=len(document.text))  # Move cursor to end


questions = [
    {
        'type': 'input',
        'name': 'pseudonyme',
        'message': 'Quel est votre pseudonyme ?',

    },
    {
        'type': 'password',
        'name': 'motdepasse',
        'message': 'Quel est votre mot de passe ?',
        'validate': PasswordValidator
    }
]

compte_service = CompteService()
bienvenue = Bienvenue()


class Authentification(AbstractVue):

    def display_info(self):
        # a remplacer
        with open('assets/error.txt', 'r', encoding="utf-8") as asset:
            print(asset.read())

    def make_choice(self, nbressai=2):

        answers = prompt(questions)
        answers['motdepasse'] = ChiffrerMotDePasse.hash_password(answers['motdepasse'], answers['pseudonyme'])

        if compte_service.verification(answers['pseudonyme'], answers['motdepasse']):
            print('Ce compte n\'existe pas ')
            nbressai = nbressai - 1
            if nbressai <= 0:
                print("Trop de tentative, veuillez réessayer plus tard")
            else:
                return self.make_choice(nbressai)


        else:

            print('Vous êtes enregistré')
            compte_dao = CompteDao()
            user = compte_dao.info_verification(answers['pseudonyme'], answers['motdepasse'])
            # print(user)
            AbstractVue.session.user = user
        return Bienvenue()
