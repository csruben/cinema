from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from Repository.repository_in_memory import RepositoryInMemory


def test_film_repostiroy():
    repo = RepositoryInMemory()
    repo.add(Film("1", "Titlu", 1200, 40.0, "Da"))
    assert len(repo.read()) == 1
    repo.modify(Film("1", "Titlumod", 1200, 40.0, "Nu"))
    assert repo.read("1").titlu_film == "Titlumod"
    assert repo.read("1").in_program == "Nu"
    repo.delete("1")
    assert len(repo.read()) == 0


def test_card_client_repository():
    repo = RepositoryInMemory()
    repo.add(CardClient("1",
                        "Dan",
                        "Pop",
                        "520",
                        "10/10/2010",
                        "11/20/2021",
                        0))
    assert len(repo.read()) == 1
    repo.modify(CardClient("1",
                           "Daniel",
                           "Popescu",
                           "0",
                           "10/10/2010",
                           "11/20/2021",
                           5))
    assert repo.read("1").prenume == "Popescu"
    assert repo.read("1").nume == "Daniel"
    assert repo.read("1").puncte_acumulate == 5
    assert repo.read("1").data_inregistrare == "11/20/2021"
    assert repo.read("1").cnp == "0"
    repo.delete("1")
    assert len(repo.read()) == 0


def test_rezervare_repository():
    repo = RepositoryInMemory()
    repo.add(Rezervare("1", "1", "1", "11/20/2021/20:15"))
    assert len(repo.read()) == 1
    repo.modify(Rezervare("1", "2", "2", "11/20/2021/20:15"))
    assert repo.read("1").id_film == "2"
    assert repo.read("1").id_card_client == "2"
    repo.delete("1")
    assert len(repo.read()) == 0
    try:
        repo.delete("42")
        assert False
    except Exception:
        assert True


def test_all_repository():
    test_rezervare_repository()
    test_film_repostiroy()
    test_card_client_repository()
