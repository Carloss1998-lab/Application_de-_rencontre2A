
class Messagerie:
    def __init__(self,contenu ,date_envoi, id_expediteur ,id_receveur , lu = True, id_message =None):
        self.contenu = contenu
        self.date_envoi = date_envoi
        self.id_expediteur = id_expediteur
        self.id_receveur = id_receveur
        self.id_message = id_message
        self.lu = lu

