from datetime import date, datetime

from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(self,
                 film_service: FilmService,
                 card_client_service: CardClientService,
                 rezervare_service: RezervareService,
                 undo_redo_service: UndoRedoService):
        self.__film_service = film_service
        self.__card_client_service = card_client_service
        self.__rezervare_service = rezervare_service
        self.__undo_redo_service = undo_redo_service

    def run_menu(self):
        while True:
            print("1. CRUD Filme")
            print("2. CRUD Card Client")
            print("3. CRUD Rezervare")
            print("4. Cautare Full Text")
            print('5. Afișarea tuturor rezervărilor dintr-un'
                  ' interval de ore dat, indiferent de zi.')
            print('6. Afișarea filmelor ordonate descrescător'
                  ' după numărul de rezervări.')
            print('7. Afișarea cardurilor client ordonate'
                  ' descrescător după numărul de puncte de pe card.')
            print('8. Ștergerea tuturor rezervărilor'
                  ' dintr-un anumit interval de zile.')
            print('9. Incrementarea cu o valoare dată a punctelor '
                  'de pe toate cardurile a căror zi de naștere se'
                  ' află într-un interval dat.')
            print('u: Undo')
            print('r: Redo')
            print("X. Iesire")
            option = input('Dati optiunea: ')

            if option == "1":
                self.run_crud_filme_menu()
            elif option == "2":
                self.run_crud_card_client_menu()
            elif option == "3":
                self.run_crud_rezervare_menu()
            elif option == "4":
                self.run_cautare_full_text()
            elif option == "5":
                self.run_afisare_rezervari()
            elif option == "6":
                self.run_afisare_filme_ordonate()
            elif option == "7":
                self.run_afisare_card_client_ordonate_dupa_puncte()
            elif option == "8":
                self.run__stergere_rezervari_interval_zile()
            elif option == "9":
                self.run__incrementare_puncte_carduri()
            elif option == "u":
                self.__undo_redo_service.undo()
            elif option == "r":
                self.__undo_redo_service.redo()
            elif option.lower() == "x":
                break
            else:
                print('Optiune gresita! Reincercati')

# FILM
    def run_crud_filme_menu(self):
        while True:
            print('''
1. Adauga film
2. Sterge film
3. Modifica film
a. Afiseaza toate filmele
x. Iesire

            ''')
            option = input('Dati optiunea: ')

            if option == "1":
                self.ui_add_film()
            elif option == "2":
                self.ui_delete_film()
            elif option == "3":
                self.ui_modify_film()
            elif option == "a":
                self.show_all_filme()
            elif option == "x":
                break
            else:
                print('Optiune gresita! Reincercati')

    def ui_add_film(self):
        option = input('''
1. Adaugare manuala
2. Generare filme
Dati optiunea: ''')
        try:
            if option == '1':
                id_film = input('Dati id-ul filmului: ')
                titlu_film = input('Dati titlul filmului: ')
                an_aparitie_film = int(input('Dati anul aparitiei: '))
                pret_bilet = float(input('Dati pretul biletului: '))
                in_program = input('Este in program? (Da/Nu): ')
                self.__film_service.add(
                    id_film,
                    titlu_film, an_aparitie_film,
                    pret_bilet, in_program)
            elif option == '2':
                n = int(input("Dati nr de entitati cu valori random: :"))
                self.__film_service.generare_valori_random(n)
            else:
                raise ValueError('Optiune necunoscuta! ')
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def ui_delete_film(self):
        try:
            id_film = input('Dati id-ul filmului de sters: ')

            self.__rezervare_service.delete_cascada(id_film)
            self.__film_service.delete(id_film)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)

    def ui_modify_film(self):
        try:
            id_film = input('Dati noul id: ')
            titlu_film = input('Dati noul titlul: ')
            an_aparitie_film = int(input("Dati noul an: "))
            pret_bilet = float(input('Dati noul pret: '))
            in_program = input('Este in program? [Da/Nu] :')

            self.__film_service.modify(
                id_film,
                titlu_film, an_aparitie_film,
                pret_bilet, in_program)
        except KeyError as ke:
            print("Eroare de cheie", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)

    def show_all_filme(self):
        for film in self.__film_service.get_all():
            print(film)

# CARD CLIENT
    def run_crud_card_client_menu(self):
        while True:
            print('''
1. Adauga Card
2. Stergere Card
3. Modifica Card
a. Afiseaza toate cardurile
x. Iesire
                ''')
            option = input('Dati optiunea: ')
            if option == "1":
                self.ui_add_card_client()
            elif option == "2":
                self.ui_delete_card_client()
            elif option == "3":
                self.ui_modify_card_client()
            elif option == "a":
                self.show_all_carduri_client()
            elif option == "x":
                break
            else:
                print('Optiune gresita! Reincercati!')

    def ui_add_card_client(self):
        try:
            id_card_client = input('Dati id-ul: ')
            nume = input('Dati numele: ')
            prenume = input('Dati prenumele: ')
            cnp = input('Dati cnpul: ')
            data_inregistrare = str(date.today())
            my_string = str(input('Dati data nasterii: DD.MM.YYY): '))
            data_nastere = str(datetime.strptime(my_string, "%d.%m.%Y"))
            puncte_acumulate = 0
            self.__card_client_service.add(
                id_card_client, nume,
                prenume, cnp,
                data_nastere,
                data_inregistrare,
                puncte_acumulate
            )
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def ui_delete_card_client(self):
        try:
            id_card_client = input('Dati id-ul cardului de sters: ')

            self.__card_client_service.delete(id_card_client)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except Exception as e:
            print("Eroare: ", e)

    def ui_modify_card_client(self):
        try:
            id_card_client = input('Dati id-ul cardului de modificat: ')
            nume = input('Dati noul nume: ')
            prenume = input('Dati noul prenume: ')
            cnp = input('Dati noul CNP: ')
            data_inregistrare = str(date.today())
            my_string = str(input('Dati data nasterii: DD.MM.YYY): '))
            data_nastere = str(datetime.strptime(my_string, "%d.%m.%Y"))
            puncte_acumulate = 0
            self.__card_client_service.modify(
                id_card_client, nume,
                prenume, cnp,
                data_nastere,
                data_inregistrare,
                puncte_acumulate
            )
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def show_all_carduri_client(self):
        for card_client in self.__card_client_service.get_all():
            print(card_client)

# REZERVARE
    def run_crud_rezervare_menu(self):
        while True:
            print('''
1. Adauga rezervare
2. Sterge rezervare
3. Modifica rezervare
a. Afiseaza toate rezervarile
x. Exit
            ''')
            option = input('Dati optiunea: ')
            if option == "1":
                self.ui_add_rezervare()
            elif option == "2":
                self.ui_delete_rezervare()
            elif option == "3":
                self.ui_modify_rezervare()
            elif option == "a":
                self.show_all_rezervari()
            elif option == "x":
                break
            else:
                print('Optiune gresita! Reincercati!!')

    def ui_add_rezervare(self):
        try:
            id_rezervare = input('Dati id-ul rezervarii: ')
            id_film = input('Dati id-ul filmului: ')
            id_card_client = input('Dati id card client: ')
            my_string = str(input('Introduceti data (dd.mm.YYYY hh:mm: ): '))
            data_ora_rezervare =\
                str(datetime.strptime(my_string, "%d.%m.%Y %H:%M"))

            puncte = self.__rezervare_service.add(
                id_rezervare, id_film,
                id_card_client, data_ora_rezervare
            )

            print('Numar total puncte card: ', puncte)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def ui_delete_rezervare(self):
        try:
            id_rezervare = input("Dati id-ul rezervarii de sters: ")

            self.__rezervare_service.delete(id_rezervare)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def ui_modify_rezervare(self):
        try:
            id_rezervare = input('Dati id-ul rezervarii de modificat : ')
            id_film = input('Dati noul id al filmului: ')
            id_card_client = input('Dati noul id de card client: ')
            my_string = str(input('Enter date(dd.mm.YYYY hh:mm): '))
            data_ora_rezervare =\
                str(datetime.strptime(my_string, "%d.%m.%Y %H:%M"))

            puncte = self.__rezervare_service.modify(
                id_rezervare, id_film,
                id_card_client, data_ora_rezervare
            )
            print('Numar total puncte card: ', puncte)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def show_all_rezervari(self):
        for rezervare in self.__rezervare_service.get_all():
            print(rezervare)

    def run_cautare_full_text(self):
        try:
            text = input('Introducere text: ')
            self.show_all_full_text(
                self.__rezervare_service.full_text_search(text))
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def show_all_full_text(self, lst):
        try:
            for entitati in lst:
                print(entitati)
            if len(lst) == 0:
                print('Nu exista text')
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def run_afisare_rezervari(self):
        try:
            timp_1_input = input('Introduceti prima ora (%H:%M): ')
            timp_1 = datetime.strptime(timp_1_input, '%H:%M')
            timp_2_input = input('Intoduceti a doua ora (%H:%M): ')
            timp_2 = datetime\
                .strptime(timp_2_input, '%H:%M')
            rezervari = self.__rezervare_service\
                .rezervare_intervarl_ore(timp_1, timp_2)
            for rezervare in rezervari:
                print(rezervare)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def run_afisare_filme_ordonate(self):
        try:
            for film in self.__rezervare_service.odoneaza_dupa_rezervare():
                print(film)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def run_afisare_card_client_ordonate_dupa_puncte(self):
        try:
            for card_client in self\
                    .__card_client_service.ordonare_dupa_puncte():
                print(card_client)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def run__stergere_rezervari_interval_zile(self):
        try:
            ziua_1 = int(input('Introducere ziua 1: '))
            ziua_2 = int(input('Introducere ziua 2: '))
            self.__rezervare_service\
                .stergere_rezervari_interval_zile(ziua_1, ziua_2)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)

    def run__incrementare_puncte_carduri(self):
        try:
            ziua_1 = int(input('Introducere ziua 1: '))
            ziua_2 = int(input('Introducere ziua 2: '))
            puncte = int(input('Introduceti punctele: '))
            self.__card_client_service\
                .incrementare_puncte(ziua_1, ziua_2, puncte)
        except KeyError as ke:
            print("Eroare de cheie: ", ke)
        except ValueError as ve:
            print("Eroare de validare: ", ve)
        except Exception as e:
            print("Eroare: ", e)
