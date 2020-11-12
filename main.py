import csv
import matplotlib.pyplot as plt
import matplotlib.dates
import requests
import os

filepath = "dpc-covid19-ita-andamento-nazionale.csv"

fileurl = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

r = requests.get(fileurl, allow_redirects=True)

open('dpc-covid19-ita-andamento-nazionale.csv', 'wb').write(r.content)

positivi =[]
rapporto = []
terapia_intensiva_ = []
r_ricov_pos =[]
casi_attivi = []
isolamento = []
r_terapia_ricov = []
r_guariti_positivi =[]
r_entrati_usciti_terapia = []
r_guariti_nuovi_positivi = []
r_deceduti_positivi = []
r_nuovipositivi_usciti = []
var_terapia_intensiva = []
baseline = []

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
            r_guariti_nuovi_positivi.append(dimessi_guariti_giornalieri/nuovi_positivi)
            r_deceduti_positivi.append(deceduti/totale_casi)
            r_nuovipositivi_usciti.append(nuovi_positivi/(dimessi_guariti_giornalieri+deceduti_giornalieri))
            var_terapia_intensiva.append(terapia_intensiva_giornalieri)
            baseline.append(0)

            #r_entrati_usciti_terapia.append( ((nuovi_positivi - isolamento_domiciliare_giornalieri)/(dimessi_guariti_giornalieri + deceduti_giornalieri)) )

            dimessi_guariti_prec = dimessi_guariti
            deceduti_prec = deceduti
            terapia_intensiva_prec = terapia_intensiva
            isolamento_domiciliare_prec = isolamento_domiciliare


#plt.plot(casi_attivi, 'y')
#plt.plot(terapia_intensiva_)

# Positivi / tamponi
plt.ylabel("daily positive / daily tests")
plt.xlabel("Time")
plt.plot(rapporto, 'r')
plt.savefig("imgs/r_positive_test.png")
plt.close()


# Ricoverati / Positivi
plt.ylabel("Actual rcovered / Actual positive")
plt.xlabel("Time")
plt.plot(r_ricov_pos, 'r')
plt.savefig("imgs/r_ricov_pos.png")
plt.close()

# Terapia intensiva / ospedalizzati
plt.ylabel("Intensive care / Hospitalized")
plt.xlabel("Time")
plt.plot(r_terapia_ricov, 'r')
plt.savefig("imgs/r_terapia_ricov.png")
plt.close()

# Guariti / positivi
plt.ylabel("Daily recovered / actual positive")
plt.xlabel("Time")
plt.plot(r_guariti_positivi, 'g')
plt.savefig("imgs/r_recovered_positive.png")
plt.close()

# Entrati / Usciti ospedalizzazione
#plt.ylabel("Daily entered / exited from Hospitalization")
#plt.xlabel("Time")
#plt.plot(r_entrati_usciti_terapia, 'g')
#plt.savefig("imgs/r_entered_exited_hosp.png")
#plt.close()

# Guariti / nuovi Positivi r_guariti_nuovi_positivi
plt.ylabel("Daily recovered / Daily new positives")
plt.xlabel("Time")
plt.plot(r_guariti_nuovi_positivi, 'g')
plt.savefig("imgs/r_recovered_new_positive.png")
plt.close()

# Deceduti / casi totale_casi
plt.ylabel("Deaths / total positives")
plt.xlabel("Time")
plt.plot(r_deceduti_positivi, 'r')
plt.savefig("imgs/r_dead_positives.png")
plt.close()

# Nuovi positivi / Dimessi + deceduti_prec
plt.ylabel("Daily New positives / Exited")
plt.xlabel("Time")
plt.plot(r_nuovipositivi_usciti, 'r')
plt.savefig("imgs/r_newpositive_recovereddeaths.png")
plt.close()

# Var terapia terapia_intensiva
plt.ylabel("Variation of intensive care")
plt.xlabel("Time")
plt.plot(var_terapia_intensiva, 'r')
plt.plot(baseline, 'b')
plt.savefig("imgs/var_terapia_intensiva.png")
plt.close()
