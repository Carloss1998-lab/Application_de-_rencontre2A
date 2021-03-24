
class Compte:
    def __init__(self, nom, prenom, email, sexe, age, interesse_par, pays, ville,pseudo,motdepasse, photo_profil, photo_profil1, photo_profil2, description , id_user=None):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.sexe = sexe
        self.age = age
        self.interesse_par = interesse_par
        self.pays = pays
        self.ville = ville
        self.pseudo = pseudo
        self.motdepasse = motdepasse
        self.photo_profil = photo_profil
        self.photo_profil1 = photo_profil1
        self.photo_profil2 = photo_profil2
        self.description = description
        self.id_user = id_user

