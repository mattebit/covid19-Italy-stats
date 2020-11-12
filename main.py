import csv
import matplotlib.pyplot as plt
import matplotlib.dates
import requests
import os

filepath = "dpc-covid19-ita-andamento-nazionale.csv"

fileurl = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

r = requests.get(fileurl, allow_redirects=True)

#open('dpc-covid19-ita-andamento-nazionale.csv', 'wb').write(r.content)

positivi =[]
rapporto = []
terapia_intensiva_ = []
r_ricov_pos =[]
casi_attivi = []
isolamento = []
r_terapia_ricov = []
r_guariti_positivi =[]
r_entrati_usciti_terapia = []

dimessi_guariti_prec = 0
deceduti_prec = 0
terapia_intensiva_prec = 0
isolamento_domiciliare_prec=0
precedente = 0

with open(filepath) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if (row[8] != 'nuovi_positivi'):
            data = row[0]
            ricoverati_con_sintomi = int(row[2])

            terapia_intensiva = int(row[3])
            terapia_intensiva_giornalieri = terapia_intensiva - terapia_intensiva_prec

            totale_ospedalizzati = int(row[4])
            isolamento_domiciliare = int(row[5])
            isolamento_domiciliare_giornalieri = isolamento_domiciliare - isolamento_domiciliare_prec
            totale_positivi = int(row[6])
            variazione_totale_positivi = int(row[7])
            nuovi_positivi = int(row[8])

            dimessi_guariti = int(row[9])
            dimessi_guariti_giornalieri = dimessi_guariti - dimessi_guariti_prec

            deceduti = int(row[10])
            deceduti_giornalieri = deceduti - deceduti_prec
            #casi_da_sospetto_diagnostico = int(row[11])
            #casi_da_screening = int(row[12])
            totale_casi = int(row[13])
            tamponi = int(row[14])
            #casi_testati = int(row[15])

            positivi.append(totale_positivi)
            rapporto.append(nuovi_positivi/(tamponi - precedente))
            precedente = int(row[14])
            r_ricov_pos.append(totale_ospedalizzati/totale_positivi)
            r_terapia_ricov.append(terapia_intensiva/ricoverati_con_sintomi)
            terapia_intensiva_.append(terapia_intensiva)
            r_guariti_positivi.append(dimessi_guariti_giornalieri/totale_positivi)

            r_entrati_usciti_terapia.append( ((nuovi_positivi - isolamento_domiciliare_giornalieri)/(dimessi_guariti_giornalieri + deceduti_giornalieri)) )

            dimessi_guariti_prec = dimessi_guariti
            deceduti_prec = deceduti
            terapia_intensiva_prec = terapia_intensiva
            isolamento_domiciliare_prec = isolamento_domiciliare


#plt.plot(r_terapia_ricov, 'r')
#plt.plot(r_guariti_positivi, 'g')
#plt.plot(casi_attivi, 'y')
#plt.plot(terapia_intensiva_)

#plt.plot(r_entrati_usciti_terapia, 'r')

# Positivi / tamponi
plt.ylabel("Positive / tests")
plt.xlabel("Time")
plt.plot(rapporto, 'r')
plt.savefig("imgs/r_positive_test.png")
plt.close()


# Ricoverati / Positivi
plt.ylabel("Recovered / positive")
plt.xlabel("Time")
plt.plot(r_ricov_pos, 'r')
plt.savefig("imgs/r_ricov_pos.png")
plt.close()
