"""A command line version of Minesweeper"""
import random
import re
import time
from string import ascii_lowercase


class Siatka:
    'Klasa zarzadza gra. Jest to siatka ktora przetrzymuje informacje co znajduje sie na planszy'

    rozmiar_siatki = 9
    #miny = []
    numer_min = 10
    #sasiednie_komorki = []

    def get_rozmiar_siatki(self):
        return self.rozmiar_siatki

    def get_numer_min(self):
        return self.numer_min

    # TODO: def __init__ for assignment of all variables

    def Ustaw_Siatke(self, start):
        pusta_siatka = [['0' for i in range(self.rozmiar_siatki)] for i in range(self.rozmiar_siatki)]

        miny = self.pobierz_miny(pusta_siatka, start, self.numer_min)

        for i, j in miny:
            pusta_siatka[i][j] = 'X'

        siatka = self.pobierz_numery(pusta_siatka)

        return (siatka, miny)

    # TODO: convert siatka -> self (if possible)
    def Pokaz_Siatke(self, siatka):
        rozmiar_siatki = len(siatka)

        poziomo = '   ' + (4 * rozmiar_siatki * '-') + '-'

        # Wypisz litery u gory 'a b c d e f g h i'
        najwyzsza_kolumna = '     '

        for i in ascii_lowercase[:rozmiar_siatki]:
            najwyzsza_kolumna = najwyzsza_kolumna + i + '   '

        print(najwyzsza_kolumna + '\n' + poziomo)

        # Wypisz liczby po lewej stronie siatki
        for idx, i in enumerate(siatka):
            rzad = '{0:2} |'.format(idx + 1)

            for j in i:
                rzad = rzad + ' ' + j + ' |'

            print(rzad + '\n' + poziomo)

        print('')

    # TODO: convert siatka -> self (if possible)
    def pobierz_losowa_komorke(self, siatka):
        rozmiar_siatki = len(siatka)

        a = random.randint(0, rozmiar_siatki - 1)
        b = random.randint(0, rozmiar_siatki - 1)

        return (a, b)

    def pobierz_sasiadow(self, siatka, numer_rzedu, numer_kolumny):
        rozmiar_siatki = len(siatka)
        sasiednie_komorki = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif -1 < (numer_rzedu + i) < rozmiar_siatki and -1 < (numer_kolumny + j) < rozmiar_siatki:
                    sasiednie_komorki.append((numer_rzedu + i, numer_kolumny + j))

        return sasiednie_komorki

    def pobierz_miny(self, siatka, start, liczba_min):
        miny = []
        sasiednie_komorki = self.pobierz_sasiadow(siatka, *start)

        for i in range(liczba_min):
            komorka = self.pobierz_losowa_komorke(siatka)
            while komorka == start or komorka in miny or komorka in sasiednie_komorki:
                komorka = self.pobierz_losowa_komorke(siatka)
            miny.append(komorka)

        return miny

    def pobierz_numery(self, siatka):
        for numer_rzedu, rzad in enumerate(siatka):
            for numer_kolumny, komorka in enumerate(rzad):
                if komorka != 'X':
                    # Pobierz wartosci sasiednich komorek
                    wartosci = [siatka[r][c] for r, c in self.pobierz_sasiadow(siatka,
                                                                        numer_rzedu, numer_kolumny)]

                    # Policz jak wiele jest min
                    siatka[numer_rzedu][numer_kolumny] = str(wartosci.count('X'))

        return siatka


    def pokaz_komorki(self, siatka, obecna_siatka, numer_rzedu, numer_kolumny):
        # Wyjdz z funkcji jesli komorka jest juz pokazana
        if obecna_siatka[numer_rzedu][numer_kolumny] != ' ':
            return

        # Pokaz obecna komorke
        obecna_siatka[numer_rzedu][numer_kolumny] = siatka[numer_rzedu][numer_kolumny]

        # Pobierz sasiadow jesli komorka jest pusta
        if siatka[numer_rzedu][numer_kolumny] == '0':
            for r, c in self.pobierz_sasiadow(siatka, numer_rzedu, numer_kolumny):
                # Powtorz funkcje dla kazdego sasiada ktory nie ma flagi
                if obecna_siatka[r][c] != 'F':
                    self.pokaz_komorki(siatka, obecna_siatka, r, c)


class Gra:
    'Klasa ktora zarzadza gra.'

    def zagraj_ponownie(self):
        wybor = input('Zagrasz ponownie? (y/n): ')

        return wybor.lower() == 'y'


    def parsuj_dane_wejsciowe(self, wejsciowy_string, rozmiar_siatki, pomocna_wiadomosc):
        komorka = ()
        flaga = False
        wiadomosc = "Niepoprawna komorka. " + pomocna_wiadomosc

        wzorzec = r'([a-{}])([0-9]+)(f?)'.format(ascii_lowercase[rozmiar_siatki - 1])
        poprawny_string = re.match(wzorzec, wejsciowy_string)

        if wejsciowy_string == 'help':
            wiadomosc = pomocna_wiadomosc

        elif poprawny_string:
            numer_rzedu = int(poprawny_string.group(2)) - 1
            numer_kolumny = ascii_lowercase.index(poprawny_string.group(1))
            flaga = bool(poprawny_string.group(3))

            if -1 < numer_rzedu < rozmiar_siatki:
                komorka = (numer_rzedu, numer_kolumny)
                wiadomosc = ''

        return {'komorka': komorka, 'flaga': flaga, 'wiadomosc': wiadomosc}


    def zagraj(self):
        siatka_obiekt = Siatka()

        rozmiar_siatki = siatka_obiekt.get_rozmiar_siatki()
        numer_min = siatka_obiekt.get_numer_min()

        obecna_siatka = [[' ' for i in range(rozmiar_siatki)] for i in range(rozmiar_siatki)]

        siatka = []
        flagi = []
        start_czasu = 0

        pomocna_wiadomosc = ("Wpisz kolumne a nastepnie numer rzedu (np. b1). "
                       "Aby postawic lub usunac flage, dodaj 'f' do komorki (np. b1f)")

        siatka_obiekt.Pokaz_Siatke(obecna_siatka)
        print(pomocna_wiadomosc + " Wpisz 'help' aby pokazac ta wiadomosc ponownie.\n")

        while True:
            pozostalo_min = numer_min - len(flagi)
            komenda_popros = input('Podaj komorke ({} min zostalo): '.format(pozostalo_min))

            wynik = self.parsuj_dane_wejsciowe(komenda_popros, rozmiar_siatki, pomocna_wiadomosc + '\n')

            wiadomosc = wynik['wiadomosc']
            komorka = wynik['komorka']

            if komorka:
                print('\n\n')
                numer_rzedu, numer_kolumny = komorka
                obecna_komorka = obecna_siatka[numer_rzedu][numer_kolumny]
                flaga = wynik['flaga']

                if not siatka:
                    siatka, miny = siatka_obiekt.Ustaw_Siatke(komorka)
                if not start_czasu:
                    start_czasu = time.time()

                if flaga:
                    # Dodaj flage jesli komorka jest pusta
                    if obecna_komorka == ' ':
                        obecna_siatka[numer_rzedu][numer_kolumny] = 'F'
                        flagi.append(komorka)
                    # Usun flage jesli flaga jest juz ustawiona
                    elif obecna_komorka == 'F':
                        obecna_siatka[numer_rzedu][numer_kolumny] = ' '
                        flagi.remove(komorka)
                    else:
                        wiadomosc = 'Nie mozna wstawic tu flagi'

                # Jesli jest tu flaga, pokaz wiadomosc
                elif komorka in flagi:
                    wiadomosc = 'Tu jest flaga'

                elif siatka[numer_rzedu][numer_kolumny] == 'X':
                    print('Przegrales.\n')
                    siatka_obiekt.Pokaz_Siatke(siatka)
                    if self.zagraj_ponownie():
                        self.zagraj()
                    return

                elif obecna_komorka == ' ':
                    siatka_obiekt.pokaz_komorki(siatka, obecna_siatka, numer_rzedu, numer_kolumny)

                else:
                    wiadomosc = "Ta komorka jest juz odkryta"

                if set(flagi) == set(miny):
                    minutes, seconds = divmod(int(time.time() - start_czasu), 60)
                    print(
                        'Wygales! '
                        'Trwalo to {} minut and {} sekund.\n'.format(minutes,
                                                                          seconds))
                    siatka_obiekt.Pokaz_Siatke(siatka)
                    if self.zagraj_ponownie():
                        self.zagraj()
                    return

            siatka_obiekt.Pokaz_Siatke(obecna_siatka)
            print(wiadomosc)


gra = Gra()
gra.zagraj()