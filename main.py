"""A command line version of Minesweeper"""
import random
import re
import time
from string import ascii_lowercase


class Siatka:
    """Jest to siatka ktora przetrzymuje informacje co znajduje sie na planszy."""

    rozmiar_siatki = 5
    numer_min = 2
    miny = []
    flagi = []
    plansza = []
    plansza_widoczna_dla_gracza = []

    def get_rozmiar_siatki(self):
        return self.rozmiar_siatki

    def get_numer_min(self):
        return self.numer_min

    # TODO: def __init__ for assignment of all variables

    def stworz_plansze(self, poczatkowa_komorka):
        pusta_siatka = [['0' for i in range(self.rozmiar_siatki)] for i in range(self.rozmiar_siatki)]

        self.ustaw_miny(poczatkowa_komorka)
        for i, j in self.miny:
            pusta_siatka[i][j] = 'X'

        self.plansza = self.pobierz_dystanse_do_min(pusta_siatka)

    def stworz_plansze_dla_gracza(self):
        self.plansza_widoczna_dla_gracza = [[' ' for i in range(self.rozmiar_siatki)] for i in
                                            range(self.rozmiar_siatki)]

    def pokaz_plansze(self, siatka):
        poziomo = '   ' + (4 * self.rozmiar_siatki * '-') + '-'

        # Wypisz litery u gory, np. 'a b c d e f g h i'
        najwyzsza_kolumna = '     '

        for i in ascii_lowercase[:self.rozmiar_siatki]:
            najwyzsza_kolumna = najwyzsza_kolumna + i + '   '

        print(najwyzsza_kolumna + '\n' + poziomo)

        # Wypisz liczby po lewej stronie siatki
        for idx, i in enumerate(siatka):
            rzad = '{0:2} |'.format(idx + 1)

            for j in i:
                rzad = rzad + ' ' + j + ' |'

            print(rzad + '\n' + poziomo)

        print('')

    def pobierz_losowa_komorke(self):
        a = random.randint(0, self.rozmiar_siatki - 1)
        b = random.randint(0, self.rozmiar_siatki - 1)

        return a, b

    def pobierz_sasiednie_komorki(self, numer_rzedu, numer_kolumny):
        sasiednie_komorki = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (numer_rzedu + i) < self.rozmiar_siatki and -1 < (numer_kolumny + j) < self.rozmiar_siatki:
                    sasiednie_komorki.append((numer_rzedu + i, numer_kolumny + j))

        return sasiednie_komorki

    def ustaw_miny(self, start):
        sasiednie_komorki = self.pobierz_sasiednie_komorki(*start)

        for i in range(self.numer_min):
            komorka = self.pobierz_losowa_komorke()
            while komorka == start or komorka in self.miny or komorka in sasiednie_komorki:
                komorka = self.pobierz_losowa_komorke()
            self.miny.append(komorka)

    def pobierz_dystanse_do_min(self, siatka):
        for numer_rzedu, rzad in enumerate(siatka):
            for numer_kolumny, komorka in enumerate(rzad):
                if komorka != 'X':
                    # Pobierz wartosci sasiednich komorek
                    wartosci = [siatka[r][c] for r, c in self.pobierz_sasiednie_komorki(numer_rzedu, numer_kolumny)]

                    # Policz jak wiele jest min
                    siatka[numer_rzedu][numer_kolumny] = str(wartosci.count('X'))

        return siatka

    def pokaz_komorki(self, numer_rzedu, numer_kolumny):
        # Wyjdz z funkcji jesli komorka jest juz pokazana
        if self.plansza_widoczna_dla_gracza[numer_rzedu][numer_kolumny] != ' ':
            return

        # Pokaz obecna komorke
        self.plansza_widoczna_dla_gracza[numer_rzedu][numer_kolumny] = self.plansza[numer_rzedu][numer_kolumny]

        # Pobierz sasiadow jesli komorka jest pusta
        if self.plansza[numer_rzedu][numer_kolumny] == '0':
            for rzad, kolumna in self.pobierz_sasiednie_komorki(numer_rzedu, numer_kolumny):
                # Powtorz funkcje dla kazdego sasiada ktory nie ma flagi
                if self.plansza_widoczna_dla_gracza[rzad][kolumna] != 'F':
                    self.pokaz_komorki(rzad, kolumna)


class Gra:
    """Klasa ktora zarzadza gra."""

    instrukcja = ("Wpisz kolumne a nastepnie numer rzedu (np. b1). "
                       "Aby postawic lub usunac flage, dodaj 'f' do komorki (np. b1f)")

    def parsuj_dane_wejsciowe(self, wejsciowy_string, rozmiar_siatki):
        komorka = ()
        flaga = False
        wiadomosc = "Niepoprawna komorka. " + self.instrukcja + '\n'

        wzorzec = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[rozmiar_siatki - 1])
        poprawny_string = re.match(wzorzec, wejsciowy_string)

        if wejsciowy_string == 'help':
            wiadomosc = self.instrukcja

        elif poprawny_string:
            numer_rzedu = int(poprawny_string.group(2)) - 1
            numer_kolumny = ascii_lowercase.index(poprawny_string.group(1))
            flaga = bool(poprawny_string.group(3))

            if -1 < numer_rzedu < rozmiar_siatki:
                komorka = (numer_rzedu, numer_kolumny)
                wiadomosc = ''

        return {'komorka': komorka, 'flaga': flaga, 'wiadomosc': wiadomosc}


    def zagraj(self):
        siatka = Siatka()
        siatka.stworz_plansze_dla_gracza()
        siatka.pokaz_plansze(siatka.plansza_widoczna_dla_gracza)

        print(self.instrukcja + " Wpisz 'help' aby pokazac ta wiadomosc ponownie.\n")
        start_czasu = time.time()

        while True:
            wpisane_dane = input('Podaj komorke: ')
            wynik = self.parsuj_dane_wejsciowe(wpisane_dane, siatka.rozmiar_siatki)

            wiadomosc = wynik['wiadomosc']
            komorka = wynik['komorka']

            if komorka:
                print('\n\n')
                numer_rzedu, numer_kolumny = komorka
                obecna_komorka = siatka.plansza_widoczna_dla_gracza[numer_rzedu][numer_kolumny]
                flaga = wynik['flaga']

                if not siatka.plansza:
                    # Utowrzy siatke z minami
                    siatka.stworz_plansze(komorka)

                if flaga:
                    # Dodaj flage jesli komorka jest pusta
                    if obecna_komorka == ' ':
                        siatka.plansza_widoczna_dla_gracza[numer_rzedu][numer_kolumny] = 'F'
                        siatka.flagi.append(komorka)
                    # Usun flage jesli flaga jest juz ustawiona
                    elif obecna_komorka == 'F':
                        siatka.plansza_widoczna_dla_gracza[numer_rzedu][numer_kolumny] = ' '
                        siatka.flagi.remove(komorka)
                    else:
                        wiadomosc = 'Nie mozna wstawic tu flagi'

                # Jesli jest tu flaga, pokaz wiadomosc
                elif komorka in siatka.flagi:
                    wiadomosc = 'Tu jest flaga'

                elif siatka.plansza[numer_rzedu][numer_kolumny] == 'X':
                    print('Przegrales.\n')
                    siatka.pokaz_plansze(siatka.plansza)
                    return

                elif obecna_komorka == ' ':
                    siatka.pokaz_komorki(numer_rzedu, numer_kolumny)

                else:
                    wiadomosc = "Ta komorka jest juz odkryta"

                if set(siatka.flagi) == set(siatka.miny):
                    minutes, seconds = divmod(int(time.time() - start_czasu), 60)
                    print(
                        'Wygrales! '
                        'Trwalo to {} minut and {} sekund.\n'.format(minutes,
                                                                          seconds))
                    siatka.pokaz_plansze(siatka.plansza)
                    return

            siatka.pokaz_plansze(siatka.plansza_widoczna_dla_gracza)
            print(wiadomosc)


gra = Gra()
gra.zagraj()
