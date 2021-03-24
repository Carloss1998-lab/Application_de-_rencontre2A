from vue.abstract_vue import AbstractVue
from service.compte_service import CompteService
import conf.properties
import socket
import threading
import pickle
import sys

state = {}


def serverListen(serverSocket):
    while True:
        msg = serverSocket.recv(1024).decode("utf-8")
        if msg == "/MesDemandesMatch":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/EnvoyerDonner":
                serverSocket.send(b"/readyForData")
                data = pickle.loads(serverSocket.recv(1024))
                if data == set():
                    print("Vous n'avez pas de ")
                else:
                    print("Pending Requests:")
                    for element in data:
                        print(element)
            else:
                print(response)
        elif msg == "/approveRequest":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/proceed":
                state["inputMessage"] = False
                print("Veuillez entrer le nom pour liker: ")
                with state["inputCondition"]:
                    state["inputCondition"].wait()
                state["inputMessage"] = True
                serverSocket.send(bytes(state["userInput"], "utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))
            else:
                print(response)

        elif msg == "/choisirInterlocuteur":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/proceed":
                state["inputMessage"] = False
                print("Veuillez ecrire le nom de l'interlocuteur: ")
                with state["inputCondition"]:
                    state["inputCondition"].wait()
                state["inputMessage"] = True
                serverSocket.send(bytes(state["userInput"], "utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))
                state["inputMessage"] = True
            else:
                print(response)

        elif msg == "/messageNonLu":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/proceed":
                state["inputMessage"] = False
                print("Veuillez ecrire le nom de l'interlocuteur: ")
                with state["inputCondition"]:
                    state["inputCondition"].wait()
                state["inputMessage"] = True
                serverSocket.send(bytes(state["userInput"], "utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))
                state["inputMessage"] = True
            else:
                print(response)


        elif msg == "/disconnect":
            serverSocket.send(bytes(".", "utf-8"))
            state["alive"] = False
            break
        elif msg == "/messageSend":
            serverSocket.send(bytes(state["userInput"], "utf-8"))
            state["sendMessageLock"].release()
        elif msg == "/allMembers":
            serverSocket.send(bytes(".", "utf-8"))
            data = pickle.loads(serverSocket.recv(1024))
            print("All Group Members:")
            for element in data:
                print(element)
        elif msg == "/onlineMembers":
            serverSocket.send(bytes(".", "utf-8"))
            data = pickle.loads(serverSocket.recv(1024))
            print("Online Group Members:")
            for element in data:
                print(element)
        elif msg == "/changeAdmin":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/proceed":
                state["inputMessage"] = False
                print("Please enter the username of the new admin: ")
                with state["inputCondition"]:
                    state["inputCondition"].wait()
                state["inputMessage"] = True
                serverSocket.send(bytes(state["userInput"], "utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))
            else:
                print(response)
        elif msg == "/whoAdmin":
            serverSocket.send(bytes(state["groupname"], "utf-8"))
            print(serverSocket.recv(1024).decode("utf-8"))
        elif msg == "/kickMember":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/proceed":
                state["inputMessage"] = False
                print("Please enter the username to kick: ")
                with state["inputCondition"]:
                    state["inputCondition"].wait()
                state["inputMessage"] = True
                serverSocket.send(bytes(state["userInput"], "utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))
            else:
                print(response)
        elif msg == "/kicked":
            state["alive"] = False
            state["inputMessage"] = False
            print("Vous avez été retiré")
            break
        elif msg == "/fileTransfer":
            state["inputMessage"] = False
            print("Please enter the filename: ")
            with state["inputCondition"]:
                state["inputCondition"].wait()
            state["inputMessage"] = True
            filename = state["userInput"]
            try:
                f = open(filename, 'rb')
                f.close()
            except FileNotFoundError:
                print("The requested file does not exist.")
                serverSocket.send(bytes("~error~", "utf-8"))
                continue
            serverSocket.send(bytes(filename, "utf-8"))
            serverSocket.recv(1024)
            print("Uploading file to server...")
            with open(filename, 'rb') as f:
                data = f.read()
                dataLen = len(data)
                serverSocket.send(dataLen.to_bytes(4, 'big'))
                serverSocket.send(data)
            print(serverSocket.recv(1024).decode("utf-8"))
        elif msg == "/receiveFile":
            print("Receiving shared group file...")
            serverSocket.send(b"/sendFilename")
            filename = serverSocket.recv(1024).decode("utf-8")
            serverSocket.send(b"/sendFile")
            remaining = int.from_bytes(serverSocket.recv(4), 'big')
            f = open(filename, "wb")
            while remaining:
                data = serverSocket.recv(min(remaining, 4096))
                remaining -= len(data)
                f.write(data)
            f.close()
            print("Received file saved as", filename)
        else:
            print(msg)


def userInput(serverSocket):
    while state["alive"]:
        state["sendMessageLock"].acquire()
        state["userInput"] = input()
        state["sendMessageLock"].release()
        with state["inputCondition"]:
            state["inputCondition"].notify()
        if state["userInput"] == "/1":
            serverSocket.send(b"/MesDemandesMatch")
        elif state["userInput"] == "/2":
            serverSocket.send(b"/approveRequest")
        elif state["userInput"] == "/12":
            serverSocket.send(b"/choisirInterlocuteur")
        elif state["userInput"] == "/13":
            serverSocket.send(b"/messageNonLu")
        elif state["userInput"] == "/3":
            serverSocket.send(b"/disconnect")
            break
        elif state["userInput"] == "/4":
            serverSocket.send(b"/allMembers")
        elif state["userInput"] == "/5":
            serverSocket.send(b"/onlineMembers")
        elif state["userInput"] == "/6":
            serverSocket.send(b"/changeAdmin")
        elif state["userInput"] == "/7":
            serverSocket.send(b"/whoAdmin")
        elif state["userInput"] == "/8":
            serverSocket.send(b"/kickMember")
        elif state["userInput"] == "/9":
            serverSocket.send(b"/fileTransfer")
        elif state["inputMessage"]:
            state["sendMessageLock"].acquire()
            serverSocket.send(b"/messageSend")


def waitServerListen(serverSocket):
    while not state["alive"]:
        msg = serverSocket.recv(1024).decode("utf-8")
        if msg == "/accepted":
            state["alive"] = True
            print("Your join request has been approved. Press any key to begin chatting.")
            break
        elif msg == "/waitDisconnect":
            state["joinDisconnect"] = True
            break


def waitUserInput(serverSocket):
    while not state["alive"]:
        state["userInput"] = input()
        if state["userInput"] == "/1" and not state["alive"]:
            serverSocket.send(b"/waitDisconnect")
            break


def main():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSocket.connect((conf.properties.HOST, conf.properties.PORT))
    except socket.error:
        print("La tentative de connexion à l'adresse choisie a échoué.")
        sys.exit()
    state["inputCondition"] = threading.Condition()# on met en veille ce thread
    state["sendMessageLock"] = threading.Lock()# on le bloque jusqu'à la réactivation
    state["username"] = AbstractVue.session.user.pseudo
        # Effectuer un like
    state["groupname"] = input("Acceder à la messagerie de ? (Entrez le nom): ")

    compte_service = CompteService()
    if compte_service.pseudo_disponible(state["groupname"]):

        print('L\'utilisateur {} n\'existe pas, merci d\'en choisir un autre ;) '.format(state["groupname"]))

    else:
        print("L\'utilisateur existe")




    state["alive"] = False
    state["joinDisconnect"] = False
    state["inputMessage"] = True
    serverSocket.send(bytes(state["username"], "utf-8"))
    serverSocket.recv(1024)
    serverSocket.send(bytes(state["groupname"], "utf-8"))
    response = serverSocket.recv(1024).decode("utf-8")
    if response == "/adminReady":
        print("Vous êtes dans vontre messagerie ", state["groupname"], "vous en êtes l'administrateur.")
        state["alive"] = True
    elif response == "/ready":
        print("Vous avez rejoins la messagerie de ", state["groupname"])
        state["alive"] = True
    elif response == "/wait":
        print(" Votre like a été envoyé avec succès.")
        print("Pour vous deconnecter , tapez: /1 ")
    waitUserInputThread = threading.Thread(target=waitUserInput, args=(serverSocket,))
    waitServerListenThread = threading.Thread(target=waitServerListen, args=(serverSocket,))
    userInputThread = threading.Thread(target=userInput, args=(serverSocket,))
    serverListenThread = threading.Thread(target=serverListen, args=(serverSocket,))
    waitUserInputThread.start()
    waitServerListenThread.start()
    while True:
        if state["alive"] or state["joinDisconnect"]:
            break
    if state["alive"]:
        print("Menu Messagerie:\n/1 -> Voir mes likes (Admins)\n/2 -> Accepter like (Admin)\n/3 -> Se deconnecter\n/4 -> Voir mes correspondants\n/5 -> Qui est en ligne ?\n/6 -> Proposez un rdv(à faire) \n/7 -> Chatbot(à faire) \n/8 -> Bloquer un utilisateur\n/9 -> Envoyer un fichier \n \n Ecrivez pour envoyer de message")
        waitUserInputThread.join()
        waitServerListenThread.join()
        userInputThread.start()
        serverListenThread.start()
    while True:
        if state["joinDisconnect"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()
            waitUserInputThread.join()
            waitServerListenThread.join()
            print("Deconnecté de l'application.")
            break
        elif not state["alive"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()
            userInputThread.join()
            serverListenThread.join()
            print("Deconnecté de l'application.")
            break


if __name__ == "__main__":
    main()
