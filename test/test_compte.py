from service.compte_service import CompteService
from dao.compte_dao import CompteDao

compte_service = CompteService()
compte_dao = CompteDao()


def test_creer_compte():
    #GIVEN
    pseudo_test = 'TestPseudo'
    mdp_test = 'MotDePassePseudo'

    #WHEN
    compte = compte_service.creer_compte(pseudo_test, mdp_test)

    #THEN
    if compte.id:
        compte_dao.delete(compte)
    assert compte.id and compte.id > 0


def test_valid_pseudo_connu():
    #GIVEN
    pseudo_test = 'TestPseudo'
    mdp_test = 'MotDePassePseudo'

    #WHEN
    compte = compte_service.creer_compte(pseudo_test, mdp_test)
    dispo = compte_service.pseudo_disponible(pseudo_test)
    #THEN
    compte_dao.delete(compte)
    assert not(dispo)


def test_valid_pseudo_inconnu():
    #GIVEN
    pseudo_test = 'PseudoFantaisiste'
    
    #WHEN
    dispo = compte_service.pseudo_disponible(pseudo_test)

    #THEN
    assert dispo
