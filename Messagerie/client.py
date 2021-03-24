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
                    print("Vous n'avez pas de like")
                else:
                    print(" Veuillez patientez, demande en cours d'execution:")
                    for element in data:
                        print(element)
            else:
                print(response)
        elif msg == "/accepterLike":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/proceed":
                state["inputMessage"] = False
                print("Entrez le nom du concerne pour l'accepter: ")
                with state["inputCondition"]:
                    state["inputCondition"].wait()
                state["inputMessage"] = True
                serverSocket.send(bytes(state["userInput"], "utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))
            else:
                print(response)
        elif msg == "/seDeconnecter":
            serverSocket.send(bytes(".", "utf-8"))
            state["alive"] = False
            break
        elif msg == "/envoyerMessage":
            serverSocket.send(bytes(state["userInput"], "utf-8"))
            state["sendMessageLock"].release()
        elif msg == "/listeAmis":
            serverSocket.send(bytes(".", "utf-8"))
            data = pickle.loads(serverSocket.recv(1024))
            print("Tous vos contacts:")
            for element in data:
                print(element)
        elif msg == "/enLigne":
            serverSocket.send(bytes(".", "utf-8"))
            data = pickle.loads(serverSocket.recv(1024))
            print("Vos contact en ligne :")
            for element in data:
                print(element)
        elif msg == "/ProposezRendezVous":
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
        elif msg == "/DiscuterAvecChatbot":
            serverSocket.send(bytes(state["groupname"], "utf-8"))
            print(serverSocket.recv(1024).decode("utf-8"))
        elif msg == "/retirer":
            serverSocket.send(bytes(".", "utf-8"))
            response = serverSocket.recv(1024).decode("utf-8")
            if response == "/proceed":
                state["inputMessage"] = False
                print("Entrez le nom du concerne: ")
                with state["inputCondition"]:
                    state["inputCondition"].wait()
                state["inputMessage"] = True
                serverSocket.send(bytes(state["userInput"], "utf-8"))
                print(serverSocket.recv(1024).decode("utf-8"))
            else:
                print(response)
        elif msg == "/Seretirer":
            state["alive"] = False
            state["inputMessage"] = False
            print("Vous avez ete retire. touchez pour quitter.")
            break
        elif msg == "/envoyerFichier":
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
            serverSocket.send(b"/accepterLike")
        elif state["userInput"] == "/3":
            serverSocket.send(b"/seDeconnecter")
            break
        elif state["userInput"] == "/4":
            serverSocket.send(b"/listeAmis")
        elif state["userInput"] == "/5":
            serverSocket.send(b"/enLigne")
        elif state["userInput"] == "/6":
            serverSocket.send(b"/ProposezRendezVous")
        elif state["userInput"] == "/7":
            serverSocket.send(b"/DiscuterAvecChatbot")
        elif state["userInput"] == "/8":
            serverSocket.send(b"/retirer")
        elif state["userInput"] == "/9":
            serverSocket.send(b"/envoyerFichier")
        elif state["inputMessage"]:
            state["sendMessageLock"].acquire()
            serverSocket.send(b"/envoyerMessage")


def waitServerListen(serverSocket):
    while not state["alive"]:
        msg = serverSocket.recv(1024).decode("utf-8")
        if msg == "/accepted":
            state["alive"] = True
            print("Votre demande de match a ete accepte. Vous pouvez commencer une discussion.")
            break
        elif msg == "/attentedeDeconnecter":
            state["joinseDeconnecter"] = True
            break


def waitUserInput(serverSocket):
    while not state["alive"]:
        state["userInput"] = input()
        if state["userInput"] == "/1" and not state["alive"]:
            serverSocket.send(b"/attentedeDeconnecter")
            break


def main():
    if len(sys.argv) < 3:
        print("USAGE: python client.py <IP> <Port>")
        print("EXAMPLE: python client.py localhost 8000")
        return
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((sys.argv[1], int(sys.argv[2])))
    state["inputCondition"] = threading.Condition()
    state["sendMessageLock"] = threading.Lock()
    state["username"] = input("Bienvenue dans Application de rencontre! Veuillez entrez votre pseudo: ")
    state["groupname"] = input("Entrez un nom pour le liker ")
    state["alive"] = False
    state["joinseDeconnecter"] = False
    state["inputMessage"] = True
    serverSocket.send(bytes(state["username"], "utf-8"))
    serverSocket.recv(1024)
    serverSocket.send(bytes(state["groupname"], "utf-8"))
    response = serverSocket.recv(1024).decode("utf-8")
    if response == "/adminReady":
        print("Votre messagerie est prête", state["groupname"], ", vous pouvez discuter")
        state["alive"] = True
    elif response == "/ready":
        print("Vous pouvez discuter avec", state["groupname"])
        state["alive"] = True
    elif response == "/wait":
        print("Votre demande de match est encours de traitement")
        print("Vous pouvez:\n/1 -> se deconnecter\n")
    waitUserInputThread = threading.Thread(target=waitUserInput, args=(serverSocket,))
    waitServerListenThread = threading.Thread(target=waitServerListen, args=(serverSocket,))
    userInputThread = threading.Thread(target=userInput, args=(serverSocket,))
    serverListenThread = threading.Thread(target=serverListen, args=(serverSocket,))
    waitUserInputThread.start()
    waitServerListenThread.start()
    while True:
        if state["alive"] or state["joinseDeconnecter"]:
            break
    if state["alive"]:
        print("Commande disponible:\n/1 -> Voir les likes en attentes (Admins)\n/2 -> liker (Admin)\n/3 -> seDeconnecter\n/4 -> Voir mes contacts\n/5 -> Mes contacts en ligne\n/6 -> Proposez un RendezVous\n/7 -> Discuter avec le chatbot\n/8 -> Commencer\n/9 -> Envoyer un fichier\n Le clavier est actif, vous pouvez envoyez un message")
        waitUserInputThread.join()
        waitServerListenThread.join()
        userInputThread.start()
        serverListenThread.start()
    while True:
        if state["joinseDeconnecter"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()
            waitUserInputThread.join()
            waitServerListenThread.join()
            print("Deconnexion reussie.")
            break
        elif not state["alive"]:
            serverSocket.shutdown(socket.SHUT_RDWR)
            serverSocket.close()
            userInputThread.join()
            serverListenThread.join()
            print("Deconnexion reussie.")
            break


if __name__ == "__main__":
    main()
