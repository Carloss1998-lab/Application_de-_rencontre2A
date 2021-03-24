from vue.abstract_vue import AbstractVue
from vue.bienvenue import Bienvenue
import regex
from vue.chiffrermotdepasse import ChiffrerMotDePasse
from service.compte_service import CompteService
from PyInquirer import Separator, prompt, Validator, ValidationError, style_from_dict, Token



class PasswordValidator(Validator):
    def validate(self, document):
        ok = len(document.text) > 5
        if not ok:
            raise ValidationError(
                message='Votre mot de passe doit faire au moins 6 caractères',
                cursor_position=len(document.text))  # Move cursor to end





custom_style_2 = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    #Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

class InterssValidator(Validator):
    def validate(self, document):

        try:
            int(document.text)
            assert  (int(document.text)==1 or int(document.text) ==2 or int(document.text) ==3)," Vous devriez choisir entre 1; 2 ; 3"
        except ValueError:
            raise ValidationError(
                message='Veuillez ecrire un nombre',

                cursor_position=len(document.text))  # Move cursor to end

class sexeValidator(Validator):
    def validate(self, document):

            try:
                   int(document.text)
                   assert  (int(document.text)==1 or int(document.text) ==2)," Vous devriez choisir entre 1 et 2"
            except ValueError:
                raise ValidationError(
                    message='Veuillez ecrire un nombre',

                    cursor_position=len(document.text))  # Move cursor to end

           # except AssertionError as msg:
            #    print(msg)

class EmailValidator(Validator):
    def validate(self, document):
        ok = regex.match("^[a-z0-9._-]+@[a-z0-9._-]+\.[(com|fr)]+", document.text)
        if not ok:
            raise ValidationError(
                message='Email invalide',
                cursor_position=len(document.text))  # Move cursor to end


questions = [

    ##
    {
        'type': 'input',
        'name': 'nom',
        'message': 'Quel est votre nom ?',

    },
    ##

    {
        'type': 'input',
        'name': 'prenom',
        'message': 'Quel est votre prenom ?',
    },

    ##

    {
        'type': 'input',
        'name': 'email',
        'message': 'Quel est votre email ?',
        'validate': EmailValidator,
    },

    ##


    {
        'type': 'input',
        'name': 'sexe',
        'message': 'Quel est votre sexe( 1= Masculin;, 2= Feminin ?',
        'validate': sexeValidator,
        'filter': lambda val: int(val)
    },

    {
        'type': 'input',
        'name': 'age',
        'message': 'Quel est votre age ?',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },


    {
        'type': 'input',
        'name': 'interessepar',
        'message': 'Vous êtes interessé par  ? (1= Homme, 2= Femme, 3= Homme et Femme ',
        'validate': InterssValidator,
        'filter': lambda val: int(val)
    },

    ##


    {
        'type': 'input',
        'name': 'pays',
        'message': 'Quel est votre pays ?',
    },

    ##
    {
        'type': 'input',
        'name': 'ville',
        'message': 'Quel est votre ville ?',
    },

    {
        'type': 'input',
        'name': 'pseudonyme',
        'message': 'Quel est votre pseudonyme ?',
    },


    {
        'type': 'password',
        'name': 'mot de passe',
        'message': 'Quel est votre mot de passe ?',
        'validate': PasswordValidator
    },

    {
        'type': 'input',
        'name': 'photo',
        'message': 'choisir photo de profil ?',
    },
    {
        'type': 'input',
        'name': 'photo1',
        'message': 'Ajouter photo ?',
    },

    {
        'type': 'input',
        'name': 'photo2',
        'message': 'Ajouter photo ?',
    },
    {
        'type': 'input',
        'name': 'description',
        'message': 'Ajouter une description à votre compte en moins de trois ligne: ',
    }
]


compte_service = CompteService()


class CreationCompte(AbstractVue):

    def make_choice(self):
        answers = prompt(questions, style=custom_style_2)
        answers['mot de passe'] = ChiffrerMotDePasse.hash_password(answers['mot de passe'],answers['pseudonyme'])
        if compte_service.pseudo_disponible(answers['pseudonyme'],answers['email']):
            user = compte_service.creer_compte(answers['nom'],answers['prenom'],answers['email'],answers['sexe'],
                answers['age'],answers['interessepar'],answers['pays'],answers['ville'],answers['pseudonyme'],
                answers['mot de passe'],answers['photo'],answers['photo1'],answers['photo2'],answers['description'])

            AbstractVue.session.user = user

            return Bienvenue()
        else:
            print('Le pseudo {} ou l\'email {} est déjà utilisé, merci d\'en choisir un autre ;) '.format(
                answers['pseudonyme'], answers['email']))
            return self.make_choice()
