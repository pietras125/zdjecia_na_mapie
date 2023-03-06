import gmplot
import os
import exifread

class OknoPokazNaMapie():
    def __init__(self):
        self.fig = ''

    def konwertuj_string_gps(self, koordynaty, kierunek):
        wynik_gps = koordynaty.replace("[","")
        wynik_gps = wynik_gps.replace("]","")
        wynik_gps = wynik_gps.replace(" ","")
        wynik_gps = wynik_gps.split(",")
        z = int(wynik_gps[2].split("/")[0]) / int(wynik_gps[2].split("/")[1])
        wynik_gps = float(int(wynik_gps[0]) + int(wynik_gps[1]) / 60 + float(z) / 3600)
        if kierunek == "S" or kierunek == "W":
            wynik_gps = -wynik_gps
        return wynik_gps

    def wyswietlOkno(self):
        apikey = 'AIzaSyDqiW0FCCjzKETvysnbSk6qP5Tn86QipZo' # (your API key here)
        gmap = gmplot.GoogleMapPlotter(52.56758077989136, 19.00991579556161, 7, apikey=apikey)
        lista_plikow = os.listdir('pliki')
        for plik in lista_plikow:
            if plik.endswith('.jpg') or plik.endswith('.JPG'):
                wlasciwosci_exif = exifread.process_file(open("pliki\\"+plik, 'rb'),stop_tag='GPS GPSLongitude')
                surowy_latitude = f"{wlasciwosci_exif['GPS GPSLatitude'].printable}"  
                surowy_latitude_kierunek = f"{wlasciwosci_exif['GPS GPSLatitudeRef'].printable}"
                surowy_longitude = f"{wlasciwosci_exif['GPS GPSLongitude'].printable}"
                surowy_longitude_kierunek = f"{wlasciwosci_exif['GPS GPSLongitude'].printable}"
                latitude_gotowy = self.konwertuj_string_gps(surowy_latitude, surowy_latitude_kierunek)
                longitude_gotowy = self.konwertuj_string_gps(surowy_longitude, surowy_longitude_kierunek)
                opis = f"{str(plik)}\\n{str(latitude_gotowy)}\\n{str(longitude_gotowy)}"
                opishtml = f"{str(plik)}<br>{str(latitude_gotowy)}<br>{str(longitude_gotowy)}"
                gmap.marker(float(latitude_gotowy), float(longitude_gotowy), "red", title=opis, info_window=opishtml)
        gmap.draw('map.html')
        os.system('map.html')

if __name__ == "__main__":
    okno_pokaz_na_mapie = OknoPokazNaMapie()
    okno_pokaz_na_mapie.wyswietlOkno()