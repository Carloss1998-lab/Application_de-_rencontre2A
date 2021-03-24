import socket
import threading
import pickle
import os
import sys
import conf.properties
from service.compte_service import CompteService
from business_model.compte import Compte
from dao.abstract_dao import AbstractDao
from dao.like_dao import LikeDao
from dao.messagerie_dao import MessagerieDao
from business_model.like import Like
from business_model.messagerie import Messagerie
import datetime



msg = MessagerieDao()
#groups = msg.liste_des_messageries()
groups = {}
groupeinterlocuteur = {}
fileTransferCondition = threading.Condition()


class Group:
    def __init__(self, admin, client):
        self.admin = admin
        self.clients = {}
        self.offlineMessages = {}
        self.allMembers = set()
        self.onlineMembers = set()
        self.joinRequests = set()
        self.waitClients = {}

        self.clients[admin] = client
        self.allMembers.add(admin)
        self.onlineMembers.add(admin)

    def disconnect(self, username):
        self.onlineMembers.remove(username)
        del self.clients[username]

    def connect(self, username, client):
        self.onlineMembers.add(username)
        self.clients[username] = client

    def sendMessage(self, message, username, groupname):
        messageriedao = MessagerieDao()
        if groupeinterlocuteur[username] == "":
            print("Veuillez choisir votre interlocuteur /12")
        else:
            for key in groupeinterlocuteur:
                #print(self.clients)
                if key == username:
                    if groupeinterlocuteur[key] in groups[groupname].onlineMembers :
                        #print(groupeinterlocuteur[key])
                        try:
                            self.clients[groupeinterlocuteur[key]].send(bytes(username + ": " + message, "utf-8"))
                        except:
                            pass
                        messge=Messagerie(message,datetime.datetime.now(), messageriedao.trouver_id_avec_pseudo(groupeinterlocuteur[key]),messageriedao.trouver_id_avec_pseudo(username))
                        messageriedao.create(messge)
                    else:
                        print("cc")
                        messge=Messagerie(message,datetime.datetime.now(), messageriedao.trouver_id_avec_pseudo(groupeinterlocuteur[key]),messageriedao.trouver_id_avec_pseudo(username),"False")
                        messageriedao.create(messge)


    def likeNotification(self, message, username):
        for member in self.onlineMembers:
            print(member)
            if member == self.admin:
                self.clients[member].send(bytes(username + ": " + message, "utf-8"))





## je créer une fonction demarrer discussion avec un individus

def application(client, username, groupname):
    while True:
        msg = client.recv(1024).decode("utf-8")
        if msg == "/MesDemandesMatch":
            client.send(b"/MesDemandesMatch")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/EnvoyerDonner")
                client.recv(1024)

                # actualiser la liste des likes non validés
                likedao= LikeDao()
                messageriedao = MessagerieDao()
                liste_des_likes_base =[]
                liste_des_likes_base = likedao.liste_des_likes(messageriedao.trouver_id_avec_pseudo(username))

                try:

                    for i in liste_des_likes_base :

                        groups[groupname].joinRequests.add(i)
                        client.send(pickle.dumps(groups[groupname].joinRequests))
                except :

                    print("Vous n\'avez pas de like")




            else:
                client.send(b"You're not an admin.")
        elif msg == "/approveRequest":
            client.send(b"/approveRequest")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/proceed")
                usernameToApprove = client.recv(1024).decode("utf-8")
                if usernameToApprove in groups[groupname].joinRequests:
                    groups[groupname].joinRequests.remove(usernameToApprove)


                    #like=Like(messageriedao.trouver_id_avec_pseudo(groupname),messageriedao.trouver_id_avec_pseudo(username), datetime.datetime.now())

                    likedao.like_reciproque(messageriedao.trouver_id_avec_pseudo(username), messageriedao.trouver_id_avec_pseudo(usernameToApprove))
                    messageDebienvenue = " Hello World"
                    messge=Messagerie(messageDebienvenue,datetime.datetime.now(), messageriedao.trouver_id_avec_pseudo(username), messageriedao.trouver_id_avec_pseudo(usernameToApprove))
                    messageriedao.create(messge)

                    groups[groupname].allMembers.add(usernameToApprove)
                    if usernameToApprove in groups[groupname].waitClients:
                        groups[groupname].waitClients[usernameToApprove].send(b"/accepted")
                        groups[groupname].connect(usernameToApprove, groups[groupname].waitClients[usernameToApprove])
                        del groups[groupname].waitClients[usernameToApprove]
                    print("Member Approved:", usernameToApprove, "| Group:", groupname)
                    client.send(b"User has been apython maindded to the group.")
                else:
                    client.send(b"The user has not requested to join.")
            else:
                client.send(b"You're not an admin.")

        elif msg == "/choisirInterlocuteur":
            client.send(b"/choisirInterlocuteur")
            client.recv(1024).decode("utf-8")
            client.send(b"/proceed")
            interlocuteur = client.recv(1024).decode("utf-8")
            if interlocuteur in groups[groupname].allMembers:
                try:
                    del groupeinterlocuteur[username]
                except KeyError:
                    print("La clé n'existe pas encore")

                groupeinterlocuteur[username]= interlocuteur
                client.send(b"succes.")
            else:
                client.send(b"L'utilisateur ne peut pas interagir avec vous.")



        elif msg == "/disconnect":
            client.send(b"/disconnect")
            client.recv(1024).decode("utf-8")
            groups[groupname].disconnect(username)
            print("User Disconnected:", username, "| Group:", groupname)
            break
        elif msg == "/messageSend":
            client.send(b"/messageSend")
            message = client.recv(1024).decode("utf-8")
            groups[groupname].sendMessage(message, username, groupname)
        elif msg == "/waitDisconnect":
            client.send(b"/waitDisconnect")
            del groups[groupname].waitClients[username]
            print("Waiting Client:", username, "Disconnected")
            break
        elif msg == "/allMembers":
            client.send(b"/allMembers")
            client.recv(1024).decode("utf-8")
            client.send(pickle.dumps(groups[groupname].allMembers))
        elif msg == "/onlineMembers":
            client.send(b"/onlineMembers")
            client.recv(1024).decode("utf-8")
            client.send(pickle.dumps(groups[groupname].onlineMembers))
        elif msg == "/changeAdmin":
            client.send(b"/changeAdmin")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/proceed")
                newAdminUsername = client.recv(1024).decode("utf-8")
                if newAdminUsername in groups[groupname].allMembers:
                    groups[groupname].admin = newAdminUsername
                    print("New Admin:", newAdminUsername, "| Group:", groupname)
                    client.send(b"Your adminship is now transferred to the specified user.")
                else:
                    client.send(b"The user is not a member of this group.")
            else:
                client.send(b"You're not an admin.")
        elif msg == "/whoAdmin":
            client.send(b"/whoAdmin")
            groupname = client.recv(1024).decode("utf-8")
            client.send(bytes("Admin: " + groups[groupname].admin, "utf-8"))
        elif msg == "/kickMember":
            client.send(b"/kickMember")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/proceed")
                usernameToKick = client.recv(1024).decode("utf-8")
                if usernameToKick in groups[groupname].allMembers:
                    groups[groupname].allMembers.remove(usernameToKick)
                    if usernameToKick in groups[groupname].onlineMembers:
                        groups[groupname].clients[usernameToKick].send(b"/kicked")
                        groups[groupname].onlineMembers.remove(usernameToKick)
                        del groups[groupname].clients[usernameToKick]
                    print("User Removed:", usernameToKick, "| Group:", groupname)
                    client.send(b"The specified user is removed from the group.")
                else:
                    client.send(b"The user is not a member of this group.")
            else:
                client.send(b"You're not an admin.")
        elif msg == "/fileTransfer":
            client.send(b"/fileTransfer")
            filename = client.recv(1024).decode("utf-8")
            if filename == "~error~":
                continue
            client.send(b"/sendFile")
            remaining = int.from_bytes(client.recv(4), 'big')
            f = open(filename, "wb")
            while remaining:
                data = client.recv(min(remaining, 4096))
                remaining -= len(data)
                f.write(data)
            f.close()
            print("File received:", filename, "| User:", username, "| Group:", groupname)
            for member in groups[groupname].onlineMembers:
                if member != username:
                    memberClient = groups[groupname].clients[member]
                    memberClient.send(b"/receiveFile")
                    with fileTransferCondition:
                        fileTransferCondition.wait()
                    memberClient.send(bytes(filename, "utf-8"))
                    with fileTransferCondition:
                        fileTransferCondition.wait()
                    with open(filename, 'rb') as f:
                        data = f.read()
                        dataLen = len(data)
                        memberClient.send(dataLen.to_bytes(4, 'big'))
                        memberClient.send(data)
            client.send(bytes(filename + " successfully sent to all online group members.", "utf-8"))
            print("File sent", filename, "| Group: ", groupname)
            os.remove(filename)
        elif msg == "/sendFilename" or msg == "/sendFile":
            with fileTransferCondition:
                fileTransferCondition.notify()
        else:
            print("UNIDENTIFIED COMMAND:", msg)


def handshake(client):

    username = client.recv(1024).decode("utf-8")
    client.send(b"/sendGroupname")
    groupname = client.recv(1024).decode("utf-8")
    likedao= LikeDao()
    groupeinterlocuteur[username] = ""

    # Verifier s'il y a dejà eu interaction
    compte_service = CompteService()
    messageriedao = MessagerieDao()

    if groupname in groups:
        if compte_service.verification_match_deja(messageriedao.trouver_id_avec_pseudo(username), messageriedao.trouver_id_avec_pseudo(groupname)):
            print('Pas encore d\'interaction ')
            # j'ecris le code de demande de like
            if compte_service.like_disponible(messageriedao.trouver_id_avec_pseudo(username), messageriedao.trouver_id_avec_pseudo(groupname)):
                like=Like(messageriedao.trouver_id_avec_pseudo(groupname),messageriedao.trouver_id_avec_pseudo(username), datetime.datetime.now())
                likedao.create(like)

                groups[groupname].waitClients[username] = client
                groups[groupname].likeNotification(username + " vous a liké.", "Application")
                client.send(b"/wait")
                print("Join Request:", username, "| Group:", groupname)
            else:
                print(" Il y a déja un like pour les deux users")
                #compte_service.modifier_like(messageriedao.trouver_id_avec_pseudo(username),messageriedao.trouver_id_avec_pseudo(groupname),                           answers['age'],answers['interessepar'],answers['pays'],answers['ville'],answers['pseudonyme'],
               #                         datetime.datetime.now())
        else:
            print("il y a eu interaction ")
            client.send(b"/ready")
            print("User Connected:", username, "| Group:", groupname)
            groups[groupname].connect(username,client)
        threading.Thread(target=application, args=(client, username, groupname,)).start()
    else:
        groups[groupname] = Group(username, client)
        # il faut initialiser self.allMembers = set()
        #         self.onlineMembers = set()
        #         self.joinRequests = set()
        #allMembers =

        #J'actualise la liste de tous les membres
        liste_des_correspondants_base = messageriedao.mes_correspondants(messageriedao.trouver_id_avec_pseudo(username))
        try:
            for i in liste_des_correspondants_base :
                groups[groupname].allMembers.add(i)
        except :
            pass

        #groups[groupname].waitClients[username] = client
        threading.Thread(target=application, args=(client, username, groupname,)).start()
        client.send(b"/adminReady")
        print("New Group:", username, "| Admin:", username)

        #liste_des_likes_base = likedao.liste_des_likes(messageriedao.trouver_id_avec_pseudo(username))

        #for i in liste_des_likes_base :
         #   groups[groupname].joinRequests.add(i)




def main():
    # On demmarrera le serveur au démarrage de l'application
    # apres l'authentification d'unutilisateur, il se place en tant que cleint sur le serveur.
    # de sa session, on peut recuperrer toutes les informations le concernant.
    # Initialisation du serveur - Mise en place du socket :
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        listenSocket.bind((conf.properties.HOST, conf.properties.PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()
    print("Serveur prêt, en attente de requêtes ...")
    listenSocket.listen(10)
    while True:
        client, _ = listenSocket.accept()
        threading.Thread(target=handshake, args=(client,)).start()


if __name__ == "__main__":
    main()
