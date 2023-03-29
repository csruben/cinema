from Domain.film_validator import FilmValidator
from Repository.repository_json import RepositoryJson
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from Tests.test_all import test_all
from UI.console import Console


def main():
    film_repository_json = RepositoryJson("filme.json")
    film_validator = FilmValidator()

    undo_redo_service = UndoRedoService()

    film_service = FilmService(film_repository_json,
                               film_validator, undo_redo_service)

    card_client_repository_json = RepositoryJson("carduri.json")
    card_client_service = CardClientService(card_client_repository_json,
                                            undo_redo_service)

    rezervare_repository_json = RepositoryJson("rezervari.json")
    rezervare_service = RezervareService(
        rezervare_repository_json,
        film_repository_json,
        card_client_repository_json,
        undo_redo_service
    )

    console = Console(film_service, card_client_service,
                      rezervare_service, undo_redo_service)

    console.run_menu()


if __name__ == '__main__':
    test_all()
    main()
