from dataclasses import dataclass

from Domain.film import Film


@dataclass
class NumarRezervariFilmViewModel():
    film: Film
    numar_rezervari: int

    def __str__(self):
        return f'Filmul  {self.film} are {self.numar_rezervari} rezervari]'
