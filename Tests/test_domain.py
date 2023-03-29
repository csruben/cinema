from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare


def test_film():
    film = Film("1", "Titlu", 1200, 40.0, "Da")
    assert film.id_entity == "1"
    assert film.titlu_film == "Titlu"
    assert film.pret_bilet_film == 40.0
    assert film.an_aparitie_film == 1200
    assert film.in_program == "Da"


def test_card_client():
    card_client = CardClient("1",
                             "Dan",
                             "Pop",
                             "520",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    assert card_client.id_entity == "1"
    assert card_client.nume == "Dan"
    assert card_client.prenume == "Pop"
    assert card_client.cnp == "520"
    assert card_client.data_nastere == "10/10/2010"
    assert card_client.data_inregistrare == "11/20/2021"
    assert card_client.puncte_acumulate == 0


def test_rezervare():
    rezervare = Rezervare("1", "1", "1", "11/20/2021/20:15")
    assert rezervare.id_entity == "1"
    assert rezervare.id_film == "1"
    assert rezervare.id_card_client == "1"
    assert rezervare.data_ora_rezervare == "11/20/2021/20:15"


def test_all_domain():
    test_rezervare()
    test_film()
    test_card_client()
