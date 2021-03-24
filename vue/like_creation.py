from vue.abstract_vue import AbstractVue
from vue.bienvenue import Bienvenue
import regex
from vue.chiffrermotdepasse import ChiffrerMotDePasse
from service.compte_service import CompteService
from PyInquirer import Separator, prompt, Validator, ValidationError, style_from_dict, Token

compte_service = CompteService()


class CreationLike(AbstractVue):

    def make_choice(self):
        #answers = prompt(questions, style=custom_style_2)
        #answers['mot de passe'] = ChiffrerMotDePasse.hash_password(answers['mot de passe'],answers['pseudonyme'])
        if compte_service.like_disponible(answers['pseudonyme'],answers['email']):
            user = compte_service.creer_like(answers['nom'],answers['prenom'],answers['email'],answers['sexe'],
                answers['age'],answers['interessepar'],answers['pays'],answers['ville'],answers['pseudonyme'],
                answers['mot de passe'],answers['photo'],answers['photo1'],answers['photo2'],answers['description'])

            AbstractVue.session.user = user

            return Bienvenue()
        else:
            print('Le pseudo {} ou l\'email {} est déjà utilisé, merci d\'en choisir un autre ;) '.format(
                answers['pseudonyme'], answers['email']))
            return self.make_choice()
