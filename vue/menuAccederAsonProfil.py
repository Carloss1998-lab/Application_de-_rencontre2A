from business_model.menu_general import MenuDisplay

if __name__ == "__main__":
    menu = [' Modifier le profil', 'Consulter le profil', 'Quitter']
    # MenuDisplay(menu)
    # elmenu(menu)

    elmenu = MenuDisplay(menu)
    print('{}'.format(elmenu.reponse()))

