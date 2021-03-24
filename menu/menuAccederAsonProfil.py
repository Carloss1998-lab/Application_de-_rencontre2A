from menu_general import MenuDisplay



if __name__ == "__main__":
    menu = [' Modifier le profil','Consulter le profil', 'Quitter']

    elmenu = MenuDisplay(menu)
    print('{}'.format(elmenu.reponse()))




