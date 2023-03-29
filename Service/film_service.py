import string
import uuid
import random

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Domain.modify_operation import ModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class FilmService:
    def __init__(self,
                 film_repository: Repository,
                 film_validator: FilmValidator,
                 undo_redo_service: UndoRedoService):
        self.__film_repository = film_repository
        self.__film_validator = film_validator
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        return self.__film_repository.read()

    def add(self,
            id_film,
            titlu_film,
            an_aparitie_film,
            pret_bilet,
            in_program):
        film = Film(id_film,
                    titlu_film,
                    an_aparitie_film,
                    pret_bilet,
                    in_program)

        self.__film_validator.validates(film)

        if pret_bilet <= 0:
            raise ValueError('Pretul biletului trebuie sa fie pozitiv! ')

        self.__film_repository.add(film)
        self.__undo_redo_service.add_undo_operation(
            AddOperation(self.__film_repository, film))

    def delete(self, id_film):
        self.__film_repository.delete(id_film)

    def modify(self,
               id_film,
               titlu_film,
               an_aparitie_film,
               pret_bilet,
               in_program):
        film_vechi = self.__film_repository.read(id_film)
        film = Film(id_film,
                    titlu_film,
                    an_aparitie_film,
                    pret_bilet,
                    in_program)

        self.__film_validator.validates(film)

        if pret_bilet <= 0:
            raise ValueError('Pretul biletului trebuie sa fie pozitiv! ')

        self.__film_repository.modify(film)
        self.__undo_redo_service.add_undo_operation(
            ModifyOperation(self.__film_repository, film_vechi, film))

    def generare_valori_random(self, n):
        """
        genereaza n entitati de tipul film
        :param n: nr entitati
        :return: entitati random
        """
        """
        for num in range(0, n):
            id_film = uuid.uuid1()
            letters = string.ascii_letters
            titlu_film = ''.join(random.choice(
                letters) for i in range(10))
            an_aparitie_film = random.randint(1, 2021)
            pret_bilet = random.randint(1, 150)
            in_program = random.choice(["Da", "Nu"])
            self.add(
                id_film,
                titlu_film, an_aparitie_film,
                pret_bilet, in_program)
        """

        if n == 0:
            return 0
        elif n != 0:
            id_film = uuid.uuid1()
            letters = string.ascii_letters
            titlu_film = ''.join(random.choice(
                letters) for i in range(10))
            an_aparitie_film = random.randint(1, 2021)
            pret_bilet = random.randint(1, 150)
            in_program = random.choice(["Da", "Nu"])
            self.add(
                id_film,
                titlu_film, an_aparitie_film,
                pret_bilet, in_program)
            self.generare_valori_random(n-1)
