from Domain.film import Film
from Domain.film_error import FilmError


class FilmValidator:
    def validates(self, film: Film):
        errors = []
        if film.in_program.upper() not in ["DA", "NU"]:
            errors.append("Filmul poate sa fie sau sa nu fie in program"
                          "(Da sau Nu)")
        if len(errors) > 0:
            raise FilmError(errors)
