from datetime import datetime
from typing import List

from Domain.add_operation import AddOperation
from Domain.cascade_delete_operation import CascadeDeleteOperation
from Domain.delete_operation import DeleteOperation
from Domain.modify_operation import ModifyOperation
from Domain.rezervare import Rezervare
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from ViewModels.numar_rezervari_film_view_model \
    import NumarRezervariFilmViewModel


class RezervareService:
    def __init__(self, rezervare_repository: Repository,
                 film_repository: Repository,
                 card_client_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.__rezervare_repository = rezervare_repository
        self.__film_repository = film_repository
        self.__card_client_repository = card_client_repository
        self.__undo_redo_service = undo_redo_service

    def get_all(self):
        return self.__rezervare_repository.read()

    def add(self,
            id_rezervare,
            id_film,
            id_card_client,
            data_ora_rezervare
            ):

        if self.__film_repository.read(id_film) is None:
            raise KeyError("Nu exista niciun film cu id-ul dat!")
        if self.__card_client_repository.read(id_card_client) is None:
            raise KeyError("Nu exista niciun card"
                           " cu id-ul dat!")
        if self.__film_repository.read(id_film).in_program.lower() == "nu":
            raise Exception('Filmul nu este in program')

        rezervare = Rezervare(id_rezervare,
                              id_film,
                              id_card_client,
                              data_ora_rezervare)

        card_client = self.__card_client_repository.read(id_card_client)

        film = self.__film_repository.read(id_film)
        card_client.puncte_acumulate =\
            card_client.puncte_acumulate\
            + film.pret_bilet_film // 10
        self.__card_client_repository.modify(card_client)
        self.__rezervare_repository.add(rezervare)
        self.__undo_redo_service.add_undo_operation(
            AddOperation(self.__rezervare_repository, rezervare)
        )

        return card_client.puncte_acumulate

    def delete(self, id_rezervare):
        rezervare = self.__rezervare_repository.read(id_rezervare)
        rezervare_veche = self.__rezervare_repository.read(id_rezervare)
        id_card_client = rezervare.id_card_client
        id_film = rezervare.id_film
        film = self.__film_repository.read(id_film)
        card_client = self.__card_client_repository.read(id_card_client)
        card_client.puncte_acumulate =\
            card_client.puncte_acumulate\
            - film.pret_bilet_film // 10
        self.__card_client_repository.modify(card_client)
        self.__rezervare_repository.delete(id_rezervare)
        self.__undo_redo_service.add_undo_operation(
            DeleteOperation(self.__rezervare_repository,
                            rezervare_veche)
        )

    def modify(self,
               id_rezervare,
               id_film,
               id_card_client,
               data_ora_rezervare):
        if self.__film_repository.read(id_film) is None:
            raise KeyError("Nu exista niciun film cu id-ul dat!")
        if self.__card_client_repository.read(id_card_client) is None:
            raise KeyError("Nu exista niciun card cu id-ul dat")
        rezervare_veche = self.__rezervare_repository.read(id_rezervare)

        rezervare = Rezervare(id_rezervare,
                              id_film,
                              id_card_client,
                              data_ora_rezervare)

        card_client = self.__card_client_repository.read(id_card_client)
        id_film_vechi = self.__rezervare_repository.read(id_rezervare).id_film
        film_vechi = self.__film_repository.read(id_film_vechi)
        film = self.__film_repository.read(id_film)

        card_client.puncte_acumulate = \
            card_client.puncte_acumulate \
            - film_vechi.pret_bilet_film // 10\
            + film.pret_bilet_film // 10
        self.__card_client_repository.modify(card_client)
        self.__rezervare_repository.modify(rezervare)
        self.__undo_redo_service.add_undo_operation(
            ModifyOperation(self.__rezervare_repository,
                            rezervare_veche,
                            rezervare)
        )

        return card_client.puncte_acumulate

    def full_text_search(self, text) -> List:
        list_full_text = []

        filme = self.__film_repository.read()
        for film in filme:
            if text in str(film.id_entity) \
                    and film not in list_full_text:
                list_full_text.append(film)
            elif text in film.titlu_film \
                    and film not in list_full_text:
                list_full_text.append(film)
            elif text in str(film.an_aparitie_film) \
                    and film not in list_full_text:
                list_full_text.append(film)
            elif text in film.in_program \
                    and film not in list_full_text:
                list_full_text.append(film)
            elif text in str(film.pret_bilet_film) \
                    and film not in list_full_text:
                list_full_text.append(film)

        carduri = self.__card_client_repository.read()
        for card_client in carduri:
            if text in card_client.id_entity \
                    and card_client not in list_full_text:
                list_full_text.append(card_client)
            elif text in card_client.nume \
                    and card_client not in list_full_text:
                list_full_text.append(card_client)
            elif text in card_client.prenume \
                    and card_client not in list_full_text:
                list_full_text.append(card_client)
            elif text in card_client.cnp \
                    and card_client not in list_full_text:
                list_full_text.append(card_client)
            elif text in card_client.data_nastere \
                    and card_client not in list_full_text:
                list_full_text.append(card_client)
            elif text in card_client.data_inregistrare \
                    and card_client not in list_full_text:
                list_full_text.append(card_client)
            elif text in str(card_client.puncte_acumulate) \
                    and card_client not in list_full_text:
                list_full_text.append(card_client)

        return list_full_text

    def rezervare_intervarl_ore(self, timp_1, timp_2) -> List:
        rezervari_timp = []
        rezervari = self.__rezervare_repository.read()

        timp_1 = timp_1.time()
        timp_2 = timp_2.time()

        """
        for rezervare in rezervari:
            data_ora = rezervare.data_ora_rezervare
            ora = datetime.strptime(data_ora, "%Y-%m-%d %H:%M:%f").time()
            if timp_1 < ora and timp_2 > ora or timp_1 > ora and timp_2 < ora:
                rezervari_timp.append(rezervare)

        return rezervari_timp
        """

        return [rezervare
                for rezervare in rezervari
                if timp_1 < datetime.strptime(rezervare.data_ora_rezervare,
                                              "%Y-%m-%d %H:%M:%f").time()
                and timp_2 > datetime.strptime(rezervare.data_ora_rezervare,
                                               "%Y-%m-%d %H:%M:%f").time()
                or timp_1 > datetime.strptime(rezervare.data_ora_rezervare,
                                              "%Y-%m-%d %H:%M:%f").time()
                and timp_2 < datetime.strptime(rezervare.data_ora_rezervare,
                                               "%Y-%m-%d %H:%M:%f").time()]

    def odoneaza_dupa_rezervare(self) -> List:
        rezultat = []
        nr_aparitii = {}

        for film in self.__film_repository.read():
            nr_aparitii[film.id_entity] = 0

        for rezervare in self.__rezervare_repository.read():
            nr_aparitii[rezervare.id_film] += 1

        for id_film in nr_aparitii:
            rezultat.append(NumarRezervariFilmViewModel(
                self.__film_repository.read(id_film),
                nr_aparitii[id_film]
            ))

        """
        rezultat = (NumarRezervariFilmViewModel(
            self.__film_repository.read(id_film),
            nr_aparitii[id_film]) for id_film in nr_aparitii)
        """

        return sorted(rezultat,
                      key=lambda nr_ap: nr_ap.numar_rezervari, reverse=True)

    def stergere_rezervari_interval_zile(self, ziua_1, ziua_2):
        """
        for rezervare in self.__rezervare_repository.read():
            ziua_rezervare = int(rezervare.data_ora_rezervare
                                 .split(" ")[0].split('-')[2])

            if ziua_1 > ziua_rezervare and ziua_2 < ziua_rezervare \
                    or ziua_1 < ziua_rezervare and ziua_2 > ziua_rezervare:
                self.delete(rezervare.id_entity)
        """

        return [self.delete(rezervare.id_entity)
                for rezervare in self.__rezervare_repository.read()
                if ziua_1 > int(rezervare.data_ora_rezervare.
                                split(" ")[0].split('-')[2])
                and ziua_2 < int(rezervare.data_ora_rezervare.
                                 split(" ")[0].split('-')[2])
                or ziua_1 < int(rezervare.data_ora_rezervare.
                                split(" ")[0].split('-')[2])
                and ziua_2 > int(rezervare.data_ora_rezervare.
                                 split(" ")[0].split('-')[2])]

    def delete_cascada(self, id_film):
        cascade = []
        for rezervare in self.__rezervare_repository.read():
            if rezervare.id_film == id_film:
                cascade.append(rezervare)
                self.__rezervare_repository.delete(rezervare.id_entity)

        cascade.append(self.__film_repository.read(id_film))

        self.__undo_redo_service.add_undo_operation(
            CascadeDeleteOperation(self.__film_repository,
                                   self.__rezervare_repository,
                                   cascade)
        )

        """
        return [self.__rezervare_repository.delete(rezervare.id_entity)
                for rezervare in self.__rezervare_repository.read()
                if rezervare.id_film == id_film]
        """
