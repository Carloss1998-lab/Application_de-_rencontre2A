import socket
import threading
import pickle
import os
import sys

groups = {}
envoyerFichierCondition = threading.Condition()


class Group:
    def __init__(self, admin, client):
        self.admin = admin
        self.clients = {}
        self.offlineMessages = {}
        self.listeAmis = set()
        self.enLigne = set()
        self.joinRequests = set()
        self.waitClients = {}

        self.clients[admin] = client
        self.listeAmis.add(admin)
        self.enLigne.add(admin)

    def seDeconnecter(self, username):
        self.enLigne.remove(username)
        del self.clients[username]

    def connect(self, username, client):
        self.enLigne.add(username)
        self.clients[username] = client

    def sendMessage(self, message, username):
        for member in self.enLigne:
            if member != username:
                self.clients[member].send(bytes(username + ": " + message, "utf-8"))


## je creer une fonction demarrer discussion avec un individus

def pyconChat(client, username, groupname):
    while True:
        msg = client.recv(1024).decode("utf-8")
        if msg == "/MesDemandesMatch":
            client.send(b"/MesDemandesMatch")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/EnvoyerDonner")
                client.recv(1024)
                client.send(pickle.dumps(groups[groupname].joinRequests))
            else:
                client.send(b"Commande invalide.")
        elif msg == "/accepterLike":
            client.send(b"/accepterLike")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/proceed")
                usernameToApprove = client.recv(1024).decode("utf-8")
                if usernameToApprove in groups[groupname].joinRequests:
                    groups[groupname].joinRequests.remove(usernameToApprove)
                    groups[groupname].listeAmis.add(usernameToApprove)
                    if usernameToApprove in groups[groupname].waitClients:
                        groups[groupname].waitClients[usernameToApprove].send(b"/accepted")
                        groups[groupname].connect(usernameToApprove, groups[groupname].waitClients[usernameToApprove])
                        del groups[groupname].waitClients[usernameToApprove]
                    print("Match reussi:", usernameToApprove, "| Group:", groupname)
                    client.send(b"L'utilisateur est ajoute")
                else:
                    client.send(b"L'utilisateur ne vous a pas encore like")
            else:
                client.send(b"Commande invalide.")
        elif msg == "/seDeconnecter":
            client.send(b"/seDeconnecter")
            client.recv(1024).decode("utf-8")
            groups[groupname].seDeconnecter(username)
            print("Utilisateur deconnecter:", username, "| Group:", groupname)
            break
        elif msg == "/envoyerMessage":
            client.send(b"/envoyerMessage")
            message = client.recv(1024).decode("utf-8")
            groups[groupname].sendMessage(message, username)
        elif msg == "/attentedeDeconnecter":
            client.send(b"/attentedeDeconnecter")
            del groups[groupname].waitClients[username]
            print("Waiting Client:", username, "seDeconnecter")
            break
        elif msg == "/listeAmis":
            client.send(b"/listeAmis")
            client.recv(1024).decode("utf-8")
            client.send(pickle.dumps(groups[groupname].listeAmis))
        elif msg == "/enLigne":
            client.send(b"/enLigne")
            client.recv(1024).decode("utf-8")
            client.send(pickle.dumps(groups[groupname].enLigne))
        elif msg == "/ProposezRendezVous":
            client.send(b"/ProposezRendezVous")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/proceed")
                newAdminUsername = client.recv(1024).decode("utf-8")
                if newAdminUsername in groups[groupname].listeAmis:
                    groups[groupname].admin = newAdminUsername
                    print("New Admin:", newAdminUsername, "| Group:", groupname)
                    client.send(b"Your adminship is now transferred to the specified user.")
                else:
                    client.send(b"The user is not a member of this group.")
            else:
                client.send(b"You're not an admin.")
        elif msg == "/DiscuterAvecChatbot":
            client.send(b"/DiscuterAvecChatbot")
            groupname = client.recv(1024).decode("utf-8")
            client.send(bytes("Admin: " + groups[groupname].admin, "utf-8"))
        elif msg == "/retirer":
            client.send(b"/retirer")
            client.recv(1024).decode("utf-8")
            if username == groups[groupname].admin:
                client.send(b"/proceed")
                usernameToKick = client.recv(1024).decode("utf-8")
                if usernameToKick in groups[groupname].listeAmis:
                    groups[groupname].listeAmis.remove(usernameToKick)
                    if usernameToKick in groups[groupname].enLigne:
                        groups[groupname].clients[usernameToKick].send(b"/Seretirer")
                        groups[groupname].enLigne.remove(usernameToKick)
                        del groups[groupname].clients[usernameToKick]
                    print("User Removed:", usernameToKick, "| Group:", groupname)
                    client.send(b"L'utilisateur est retire")
                else:
                    client.send(b"L'utilisateur ne fait pas partie de votre messagerie")
            else:
                client.send(b"Commande invalide.")
        elif msg == "/envoyerFichier":
            client.send(b"/envoyerFichier")
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
            for member in groups[groupname].enLigne:
                if member != username:
                    memberClient = groups[groupname].clients[member]
                    memberClient.send(b"/receiveFile")
                    with envoyerFichierCondition:
                        envoyerFichierCondition.wait()
                    memberClient.send(bytes(filename, "utf-8"))
                    with envoyerFichierCondition:
                        envoyerFichierCondition.wait()
                    with open(filename, 'rb') as f:
                        data = f.read()
                        dataLen = len(data)
                        memberClient.send(dataLen.to_bytes(4, 'big'))
                        memberClient.send(data)
            client.send(bytes(filename + " successfully sent to all online group members.", "utf-8"))
            print("File sent", filename, "| Group: ", groupname)
            os.remove(filename)
        elif msg == "/sendFilename" or msg == "/sendFile":
            with envoyerFichierCondition:
                envoyerFichierCondition.notify()
        else:
            print("UNIDENTIFIED COMMAND:", msg)


def handshake(client):
    username = client.recv(1024).decode("utf-8")
    client.send(b"/sendGroupname")
    groupname = client.recv(1024).decode("utf-8")
    if groupname in groups:
        if username in groups[groupname].listeAmis:
            groups[groupname].connect(username, client)
            client.send(b"/ready")
            print("User Connected:", username, "| Group:", groupname)
        else:
            groups[groupname].joinRequests.add(username)
            groups[groupname].waitClients[username] = client

            groups[groupname].sendMessage(username + " has requested to join the group.", "Application de rencontre")
            client.send(b"/wait")
            print("Join Request:", username, "| Group:", groupname)
        threading.Thread(target=pyconChat, args=(client, username, groupname,)).start()
    else:
        groups[groupname] = Group(username, client)
        threading.Thread(target=pyconChat, args=(client, username, groupname,)).start()
        client.send(b"/adminReady")
        print("New Group:", groupname, "| Admin:", username)


def main():
    if len(sys.argv) < 3:
        print("USAGE: python server.py <IP> <Port>")
        print("EXAMPLE: python server.py localhost 8000")
        return
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind((sys.argv[1], int(sys.argv[2])))
    listenSocket.listen(10)
    print("Application de rencontre en cours d'exécution")
    while True:
        client, _ = listenSocket.accept()
        threading.Thread(target=handshake, args=(client,)).start()


if __name__ == "__main__":
    main()
