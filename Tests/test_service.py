from datetime import datetime

from Domain.card_client import CardClient
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Repository.repository_in_memory import RepositoryInMemory
from Service import undo_redo_service
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService


def test_film_service():
    film_validator = FilmValidator()
    film_repository = RepositoryInMemory()
    undo_redo_service = UndoRedoService()
    film_service = FilmService(film_repository,
                               film_validator,
                               undo_redo_service)
    film_service.add("1", "Titlu", 1200, 40.0, "Da")
    assert len(film_service.get_all()) == 1
    film_service.modify("1", "TitluMod", 1200, 40.0, "Da")
    assert len(film_service.get_all()) == 1
    film_service.delete("1")
    assert len(film_service.get_all()) == 0


def test_card_client_service():
    card_client_repository = RepositoryInMemory()
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            undo_redo_service)
    card_client_service.add("1",
                            "Dan",
                            "Pop",
                            "520",
                            "10/10/2010",
                            "11/20/2021",
                            0)
    assert len(card_client_service.get_all()) == 1
    card_client_service.delete("1")
    assert len(card_client_service.get_all()) == 0


def test_rezervare_service():
    rezervare_repository = RepositoryInMemory()
    film_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    undo_redo_service = UndoRedoService()
    rezervare_service = RezervareService(rezervare_repository,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    film = Film("1", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("1",
                             "Dan",
                             "Pop",
                             "520",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("1", "1", "1", "11/20/2021/20:15")
    assert len(rezervare_service.get_all()) == 1
    rezervare_service.delete("1")
    assert len(rezervare_service.get_all()) == 0


def test_full_text_search():
    lst = []
    rezervare_repository = RepositoryInMemory()
    film_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    undo_redo_service = UndoRedoService()
    rezervare_service = RezervareService(rezervare_repository,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    film = Film("1", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("1",
                             "Dan",
                             "Pop",
                             "520",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("1", "1", "1", "11/20/2021/20:15")
    lst = rezervare_service.full_text_search("1")
    assert len(lst) == 2
    assert lst[0] == Film("1", "Titlu", 1200, 40.0, "Da")
    assert lst[1] == CardClient("1",
                                "Dan",
                                "Pop",
                                "520",
                                "10/10/2010",
                                "11/20/2021",
                                4)


def test_incrementare_puncte():
    card_client_repository = RepositoryInMemory()
    undo_redo_service = UndoRedoService()
    card_client_service = CardClientService(card_client_repository,
                                            undo_redo_service)
    card_client_service.add("1",
                            "Dan",
                            "Pop",
                            "520",
                            "10-10-2010",
                            "11-20-2021",
                            0)
    card_client_service.add("2",
                            "Dan",
                            "Pop",
                            "520",
                            "10-20-2010",
                            "11-20-2021",
                            0)
    card_client_service.incrementare_puncte(1, 9, 100)
    assert card_client_repository.read("1").puncte_acumulate == 0
    assert card_client_repository.read("2").puncte_acumulate == 0


def test_rezervare_interval_ore():
    rezervare_repository = RepositoryInMemory()
    film_repository = RepositoryInMemory()
    card_client_repository = RepositoryInMemory()
    rezervare_service = RezervareService(rezervare_repository,
                                         film_repository,
                                         card_client_repository)
    film = Film("1", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("1",
                             "Dan",
                             "Pop",
                             "520",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("1", "1", "1", "11/20/2021/20:15")
    rezervare_service = \
        RezervareService(rezervare_repository,
                         film_repository,
                         card_client_repository)

    film = Film("2", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("2",
                             "Dan",
                             "Pop",
                             "520",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("2", "2", "2", "11/20/2021/20:15")
    timp_1_input = '15:30'
    timp_1 = datetime.strptime(timp_1_input, '%H:%M')
    timp_2_input = '12:20'
    timp_2 = datetime \
        .strptime(timp_2_input, '%H:%M')
    lst = rezervare_service.rezervare_intervarl_ore(timp_1, timp_2)
    assert len(lst) == 1


def test_odoneaza_dupa_rezervare():
    rezervare_repository = RepositoryInMemory()
    film_repository = RepositoryInMemory()
    undo_redo_service = UndoRedoService()
    card_client_repository = RepositoryInMemory()
    rezervare_service = RezervareService(rezervare_repository,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    film = Film("1", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("1",
                             "Dan",
                             "Pop",
                             "52001",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("1", "1", "1", "11/20/2021/20:15")
    rezervare_service = RezervareService(rezervare_repository,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)

    film = Film("2", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("2",
                             "Dan",
                             "Pop",
                             "520",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("2", "2", "2", "11/20/2021/20:15")

    card_client = CardClient("3",
                             "Dan",
                             "Pop",
                             "5200",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("3", "1", "1", "11/20/2021/20:15")

    lst = rezervare_service.odoneaza_dupa_rezervare()
    assert len(lst) == 2
    assert lst[1].numar_rezervari == 1
    assert lst[0].numar_rezervari == 2
    assert lst[0].film == Film("1", "Titlu", 1200, 40.0, "Da")
    assert lst[1].film == Film("2", "Titlu", 1200, 40.0, "Da")


def test_stergere_rezervari_interval_zile():
    rezervare_repository = RepositoryInMemory()
    film_repository = RepositoryInMemory()
    undo_redo_service = UndoRedoService()
    card_client_repository = RepositoryInMemory()
    rezervare_service = RezervareService(rezervare_repository,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)
    film = Film("1", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("1",
                             "Dan",
                             "Pop",
                             "52001",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("1", "1", "1", "11-29-2021 20:15")
    rezervare_service = RezervareService(rezervare_repository,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)

    film = Film("2", "Titlu", 1200, 40.0, "Da")
    film_repository.add(film)
    card_client = CardClient("2",
                             "Dan",
                             "Pop",
                             "520",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("2", "2", "2", "11-15-2021 20:15")

    card_client = CardClient("3",
                             "Dan",
                             "Pop",
                             "5200",
                             "10/10/2010",
                             "11/20/2021",
                             0)
    card_client_repository.add(card_client)
    rezervare_service.add("3", "1", "1", "11-21-2021 20:15")
    assert len(rezervare_service.get_all()) == 3
    rezervare_service.stergere_rezervari_interval_zile(1, 11)
    assert len(rezervare_service.get_all()) == 3


def test_all_service():
    test_film_service()
    test_card_client_service()
    test_rezervare_service()
    test_full_text_search()
    test_incrementare_puncte()
    test_odoneaza_dupa_rezervare()
    test_stergere_rezervari_interval_zile()
