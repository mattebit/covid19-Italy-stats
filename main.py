import csv
import matplotlib.pyplot as plt
import matplotlib.dates
import requests
import os
import codecs

filepath = "dpc-covid19-ita-andamento-nazionale.csv"
comuni_giornaliero_path = "data/comuni_giornaliero_dati_fino_31agosto.csv"

fileurl = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

r = requests.get(fileurl, allow_redirects=True)

open('dpc-covid19-ita-andamento-nazionale.csv', 'wb').write(r.content)

lista_date = []
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
decessi_giornalieri_15_18_media = []
baseline = []
r_deceduticovid_deceduti_norm = []

dimessi_guariti_prec = 0
deceduti_prec = 0
terapia_intensiva_prec = 0
isolamento_domiciliare_prec=0
precedente = 0

def generate_median_15_18():
    base_anno = []

    base_mese = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(0,13):
        base_anno.append(base_mese.copy())

    a_15 = base_anno.copy()
    a_16 = base_anno.copy()
    a_17 = base_anno.copy()
    a_18 = base_anno.copy()
    a_15_18 = []
    a_19 = base_anno.copy()
    a_20 = base_anno.copy()

    count = 0

    with codecs.open(comuni_giornaliero_path, encoding='utf-8',
                     errors='ignore') as csvfile2:
        reader = csv.reader(csvfile2, delimiter=',', quotechar='|')
        for row in reader:
            count += 1
            if count % 100000 == 0:
                print(count)

            if row[0] != 'REG':
                ge = row[8]
                month = 0
                day = 0
                if len(ge) == 3:
                    month = int(ge[0])
                    day = int(ge[1:3])
                else:
                    month = int(ge[0:2])
                    day = int(ge[2:4])

                #print("Month: " + str(month))
                #print("Day: " + str(day))

                t_15 = int(row[21])
                t_16 = int(row[22])
                t_17 = int(row[23])
                t_18 = int(row[24])
                t_19 = int(row[25])
                if row[26] == 'n.d.':
                    t_20 = 0
                else:
                    t_20 = int(row[26])


                a_15[month][day] += t_15
                a_16[month][day] += t_16
                a_17[month][day] += t_17
                a_18[month][day] += t_18
                a_19[month][day] += t_19
                a_20[month][day] += t_20

    for i in range(1,13):
        for j in range(1,32):
            median = (a_15[i][j] + a_16[i][j] + a_17[i][j] + a_18[i][j])/4
            if median != 0:
                a_15_18.append(median)


a_15_18 = [13595.0, 13152.0, 13125.0, 13120.0, 13233.0, 13015.0, 12859.0, 13101.0, 13447.0, 13449.0, 13241.0, 13342.0, 13155.0, 13082.0, 13070.0, 13111.0, 13054.0, 13024.0, 12897.0, 12793.0, 12845.0, 12896.0, 12961.0, 12844.0, 12774.0, 12415.0, 12635.0, 12691.0, 12429.0, 12841.0, 12527.0, 12991.0, 12776.0, 12593.0, 12421.0, 12238.0, 12373.0, 12188.0, 12060.0, 12078.0, 12104.0, 12250.0, 12200.0, 12205.0, 12121.0, 12066.0, 11998.0, 12000.0, 12164.0, 11952.0, 11699.0, 11850.0, 11829.0, 11847.0, 11817.0, 11799.0, 11792.0, 11655.0, 11812.0, 3632.0, 11857.0, 12043.0, 12056.0, 11794.0, 11974.0, 11856.0, 11850.0, 11711.0, 11943.0, 12196.0, 11957.0, 12261.0, 12274.0, 12121.0, 11999.0, 12142.0, 12316.0, 12343.0, 12307.0, 12424.0, 12619.0, 12477.0, 12647.0, 12222.0, 12448.0, 12122.0, 12361.0, 12444.0, 12119.0, 12388.0, 11850.0, 12190.0, 11788.0, 12022.0, 11820.0, 11692.0, 11523.0, 11431.0, 11396.0, 11264.0, 11517.0, 11373.0, 11293.0, 11410.0, 11242.0, 11089.0, 10689.0, 11009.0, 10909.0, 10727.0, 10721.0, 10632.0, 10463.0, 10750.0, 10435.0, 10360.0, 10469.0, 10559.0, 10292.0, 10162.0, 9873.0, 10071.0, 10302.0, 10194.0, 10044.0, 10196.0, 10197.0, 10195.0, 10213.0, 10020.0, 10001.0, 9840.0, 9885.0, 10025.0, 9747.0, 9853.0, 9614.0, 9863.0, 9969.0, 9690.0, 9596.0, 9492.0, 9660.0, 9614.0, 9707.0, 9739.0, 9654.0, 9604.0, 9640.0, 9682.0, 9709.0, 9397.0, 9655.0, 9616.0, 9823.0, 9927.0, 10054.0, 9812.0, 9659.0, 9757.0, 9642.0, 9403.0, 9473.0, 9668.0, 9527.0, 9608.0, 9625.0, 9688.0, 9493.0, 9280.0, 9348.0, 9303.0, 9473.0, 9596.0, 9695.0, 9900.0, 9866.0, 9875.0, 9925.0, 9915.0, 9871.0, 9808.0, 10039.0, 9957.0, 10159.0, 9949.0, 9953.0, 10129.0, 10065.0, 10373.0, 10148.0, 10081.0, 10060.0, 9977.0, 9920.0, 9584.0, 9830.0, 9714.0, 9629.0, 9528.0, 9908.0, 10115.0, 10163.0, 10236.0, 10364.0, 10200.0, 10057.0, 9934.0, 9875.0, 9630.0, 9821.0, 9907.0, 10010.0, 10306.0, 10132.0, 10415.0, 10479.0, 10240.0, 10532.0, 10536.0, 10585.0, 10587.0, 10628.0, 10324.0, 10119.0, 9993.0, 9801.0, 9709.0, 9566.0, 9666.0, 9809.0, 9363.0, 9463.0, 9741.0, 9473.0, 9397.0, 9736.0, 9259.0, 9336.0, 9282.0, 9552.0, 9544.0, 9558.0, 9507.0, 8006.0, 7686.0, 7533.0, 7555.0, 7825.0, 7589.0, 7647.0, 7603.0, 7512.0, 7495.0, 7677.0, 7769.0, 7816.0, 7885.0, 8035.0, 7912.0, 7910.0, 7784.0, 7768.0, 7560.0, 7733.0, 7722.0, 7620.0, 7684.0, 7767.0, 7848.0, 7802.0, 7950.0, 7999.0, 8050.0, 8196.0, 7961.0, 8123.0, 7946.0, 8104.0, 8222.0, 8226.0, 8180.0, 8351.0, 8281.0, 8396.0, 8223.0, 8427.0, 8521.0, 8529.0, 8436.0, 8383.0, 8511.0, 8496.0, 8445.0, 8335.0, 8232.0, 8292.0, 8350.0, 8703.0, 8422.0, 8509.0, 8252.0, 8595.0, 8310.0, 7993.0, 8121.0, 8437.0, 8263.0, 8517.0, 8594.0, 8653.0, 8387.0, 8393.0, 8415.0, 8476.0, 8570.0, 8551.0, 8598.0, 8607.0, 8615.0, 8615.0, 8633.0, 8603.0, 8683.0, 8721.0, 8732.0, 8714.0, 8870.0, 8693.0, 8725.0, 8796.0, 8607.0, 8582.0, 8473.0, 8668.0, 8899.0, 8891.0, 8976.0, 8910.0, 8887.0, 8971.0, 8718.0, 9048.0, 9114.0, 9186.0, 9128.0, 9419.0, 9278.0, 9366.0, 9120.0, 9335.0, 9282.0, 9266.0, 9297.0, 9556.0, 9689.0, 9741.0, 9494.0, 9466.0, 9736.0, 9697.0, 9997.0, 10208.0, 10164.0, 10017.0, 9807.0]

# Prima data 24/2
# giorni dall'1 gennaio al 24 febbraio: 55
count = 0
with open(filepath) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if (row[8] != 'nuovi_positivi'):
            data = row[0].split('T')[0]


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

            decessi_giornalieri_15_18_media = a_15_18[54 + count]

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
            r_deceduticovid_deceduti_norm.append(deceduti_giornalieri/decessi_giornalieri_15_18_media)
            var_terapia_intensiva.append(terapia_intensiva_giornalieri)
            baseline.append(0)

            #r_entrati_usciti_terapia.append( ((nuovi_positivi - isolamento_domiciliare_giornalieri)/(dimessi_guariti_giornalieri + deceduti_giornalieri)) )

            dimessi_guariti_prec = dimessi_guariti
            deceduti_prec = deceduti
            terapia_intensiva_prec = terapia_intensiva
            isolamento_domiciliare_prec = isolamento_domiciliare
            count += 1

#plt.plot(casi_attivi, 'y')
#plt.plot(terapia_intensiva_)

# Positivi / tamponi
plt.ylabel("daily positive / daily tests")
plt.xlabel("Day")
plt.plot(rapporto, 'r')
plt.savefig("imgs/r_positive_test.png")
plt.close()


# Ricoverati / Positivi
plt.ylabel("Actual rcovered / Actual positive")
plt.xlabel("Day")
plt.plot(r_ricov_pos, 'r')
plt.savefig("imgs/r_ricov_pos.png")
plt.close()

# Terapia intensiva / ospedalizzati
plt.ylabel("Intensive care / Hospitalized")
plt.xlabel("Day")
plt.plot(r_terapia_ricov, 'r')
plt.savefig("imgs/r_terapia_ricov.png")
plt.close()

# Guariti / positivi
plt.ylabel("Daily recovered / actual positive")
plt.xlabel("Day")
plt.plot(r_guariti_positivi, 'g')
plt.savefig("imgs/r_recovered_positive.png")
plt.close()

# Entrati / Usciti ospedalizzazione
#plt.ylabel("Daily entered / exited from Hospitalization")
#plt.xlabel("Day")
#plt.plot(r_entrati_usciti_terapia, 'g')
#plt.savefig("imgs/r_entered_exited_hosp.png")
#plt.close()

# Guariti / nuovi Positivi r_guariti_nuovi_positivi
plt.ylabel("Daily recovered / Daily new positives")
plt.xlabel("Day")
plt.plot(r_guariti_nuovi_positivi, 'g')
plt.savefig("imgs/r_recovered_new_positive.png")
plt.close()

# Deceduti / casi totale_casi
plt.ylabel("Deaths / total positives")
plt.xlabel("Day")
plt.plot(r_deceduti_positivi, 'r')
plt.savefig("imgs/r_dead_positives.png")
plt.close()

# Nuovi positivi / Dimessi + deceduti_prec
plt.ylabel("Daily New positives / Exited")
plt.xlabel("Day")
plt.plot(r_nuovipositivi_usciti, 'r')
plt.savefig("imgs/r_newpositive_recovereddeaths.png")
plt.close()

# Var terapia terapia_intensiva
plt.ylabel("Variation of intensive care")
plt.xlabel("Day")
plt.plot(var_terapia_intensiva, 'r')
plt.plot(baseline, 'b')
plt.savefig("imgs/var_terapia_intensiva.png")
plt.close()

# deceduti giornalieri covid / deceduti giornalieri in media 5 anni
plt.ylabel("Daily covid deaths / 5 year median daily deaths")
plt.xlabel("Day")
plt.plot(r_deceduticovid_deceduti_norm, 'r')
plt.savefig("imgs/r_deceduticovid_deceduti_norm.png")
plt.close()
