from typing import List

from Domain.add_operation import AddOperation
from Domain.card_client import CardClient
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from utils import my_sorted


class CardClientService:
    def __init__(self, card_client_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.__card_client_repository = card_client_repository
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        return self.__card_client_repository.read()

    def add(self,
            id_card_client,
            nume,
            prenume,
            cnp,
            data_nastere,
            data_inregistrare,
            puncte_acumulate):

        card_client = CardClient(id_card_client,
                                 nume,
                                 prenume,
                                 cnp,
                                 data_nastere,
                                 data_inregistrare,
                                 puncte_acumulate)

        if self.__card_client_repository.read(cnp) is not None:
            raise ValueError("CNP-ul trebuie sa fie unic")

        self.__card_client_repository.add(card_client)
        self.__undo_redo_service.add_undo_operation(
            AddOperation(self.__card_client_repository, card_client))

    def delete(self, id_card_client):
        card_sters = self.__card_client_repository.read(id_card_client)
        self.__card_client_repository.delete(id_card_client)
        self.__undo_redo_service.add_undo_operation(
            DeleteOperation(self.__card_client_repository,
                            card_sters)
        )

    def modify(self,
               id_card_client,
               nume,
               prenume,
               cnp,
               data_nastere,
               data_inregistrare,
               puncte_acumulate):

        card_client_vechi = self.__card_client_repository.read(id_card_client)

        card_client = CardClient(
            id_card_client,
            nume,
            prenume,
            cnp,
            data_nastere,
            data_inregistrare,
            puncte_acumulate)
        if self.__card_client_repository.read(id_card_client).cnp != \
                cnp and self.__card_client_repository.read(cnp) \
                is not None:
            raise ValueError("CNP-ul trebuie sa fie unic")

        self.__card_client_repository.modify(card_client)
        self.__undo_redo_service.add_undo_operation(
            ModifyOperation(self.__card_client_repository,
                            card_client_vechi,
                            card_client)
        )

    def ordonare_dupa_puncte(self) -> List:
        return my_sorted(self.__card_client_repository.read(),
                         key=lambda card_client: card_client.puncte_acumulate,
                         reverse=True)

    def incrementare_puncte(self, ziua_1, ziua_2, puncte):
        for card_client in self.__card_client_repository.read():
            ziua_nastere = \
                int(card_client.data_nastere.split(" ")[0].split("-")[2])
            if ziua_1 < ziua_nastere and ziua_2 > ziua_nastere or\
                    ziua_1 < ziua_nastere and ziua_2 > ziua_nastere:
                card_client.puncte_acumulate \
                    = card_client.puncte_acumulate + puncte
                self.modify(
                    card_client.id_entity,
                    card_client.nume,
                    card_client.prenume,
                    card_client.cnp,
                    card_client.data_nastere,
                    card_client.data_inregistrare,
                    card_client.puncte_acumulate)
