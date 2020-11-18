import csv
import matplotlib.pyplot as plt
import matplotlib.dates
import requests
import os
import codecs
import json
import math
from datetime import datetime

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
decessi_giornalieri_totali_italia = []

j_r_positivi_tamponi = []
j_r_ricoverati_positivi = []
j_r_terapia_ospedalizzati = []
j_r_decessi_20_decessi_15_18 = []
j_r_decessi_covid_decessi_20 = []

dimessi_guariti_prec = 0
deceduti_prec = 0
terapia_intensiva_prec = 0
isolamento_domiciliare_prec=0
precedente = 0

def initMatrix():
    res = []
    for m in range(0,13):
        tmp = []
        for d in range(0,32):
            tmp.append(0)
        res.append(tmp)
    return res

def generate_median_15_18():
    a_15 = initMatrix()
    a_16 = initMatrix()
    a_17 = initMatrix()
    a_18 = initMatrix()
    a_19 = initMatrix()
    a_20 = initMatrix()
    a_15_18 = initMatrix()

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
            #handle 29th of feb
            # only 2016 has 29th of feb
            if i == 2 and j == 29:
                a_15_18[i][j] = a_16[i][j]
            else:
                median = (a_15[i][j] + a_16[i][j] + a_17[i][j] + a_18[i][j])/4
                a_15_18[i][j] = median
    
    return a_15_18, a_20

#a_15_18, a_20 = generate_median_15_18()
#print(a_15_18)
#print(a_20)

a_15_18 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2403.75, 2272.25, 2273.0, 2297.25, 2322.25, 2247.5, 2213.25, 2261.0, 2309.25, 2321.5, 2308.0, 2315.75, 2265.5, 2214.75, 2245.75, 2238.0, 2198.0, 2218.0, 2195.0, 2168.0, 2177.0, 2184.25, 2179.5, 2160.0, 2143.5, 2093.75, 2086.5, 2095.75, 2081.25, 2169.25, 2082.0], [0, 2194.0, 2131.25, 2089.0, 2058.5, 2045.5, 2060.25, 2049.75, 1989.25, 2014.5, 2022.0, 1997.5, 2002.25, 2028.25, 1989.0, 2029.25, 2022.0, 2013.25, 2005.0, 1947.5, 1928.75, 1977.75, 1992.75, 1982.5, 1960.25, 1935.0, 1946.5, 1922.5, 1944.25, 1770, 0.0, 0.0], [0, 1944.25, 1988.25, 1996.75, 1959.75, 1964.5, 1938.25, 1925.5, 1872.25, 1906.75, 1957.0, 1891.5, 1930.0, 1895.5, 1880.75, 1832.0, 1873.75, 1903.75, 1847.5, 1854.0, 1848.5, 1867.25, 1851.75, 1870.0, 1782.5, 1788.75, 1759.0, 1776.5, 1810.25, 1801.0, 1855.5, 1811.75], [0, 1838.25, 1740.25, 1795.5, 1768.25, 1792.25, 1765.5, 1729.0, 1738.75, 1725.25, 1755.25, 1753.75, 1755.0, 1767.25, 1769.5, 1744.25, 1697.75, 1735.0, 1695.0, 1685.25, 1671.75, 1693.25, 1682.25, 1727.5, 1671.5, 1645.5, 1679.25, 1743.0, 1687.0, 1658.0, 1620.0, 0.0], [0, 1642.25, 1704.5, 1680.0, 1657.75, 1696.25, 1688.0, 1698.5, 1667.0, 1654.0, 1636.0, 1617.0, 1638.0, 1679.75, 1595.25, 1615.0, 1580.0, 1613.75, 1644.25, 1612.25, 1576.5, 1587.5, 1600.25, 1588.0, 1607.75, 1615.0, 1615.0, 1615.5, 1609.25, 1650.0, 1625.25, 1600.0], [0, 1609.0, 1575.75, 1607.0, 1640.25, 1665.5, 1619.5, 1628.75, 1618.5, 1593.0, 1528.25, 1584.75, 1590.75, 1601.25, 1606.5, 1593.0, 1603.5, 1557.25, 1513.25, 1542.25, 1527.0, 1574.75, 1596.5, 1609.75, 1625.0, 1611.0, 1614.25, 1591.25, 1570.5, 1542.0, 1576.5, 0.0], [0, 1594.0, 1593.5, 1649.75, 1636.25, 1655.75, 1670.5, 1696.25, 1757.75, 1676.25, 1675.0, 1712.75, 1706.75, 1699.0, 1653.25, 1667.5, 1649.25, 1623.5, 1631.75, 1706.5, 1731.0, 1744.5, 1739.0, 1784.75, 1707.75, 1672.5, 1671.0, 1622.5, 1592.25, 1636.25, 1650.25, 1647.75], [0, 1695.25, 1662.5, 1746.25, 1781.25, 1777.5, 1830.75, 1829.0, 1833.5, 1819.5, 1807.25, 1724.75, 1681.0, 1625.0, 1609.75, 1631.75, 1586.75, 1621.25, 1637.5, 1557.25, 1562.5, 1607.25, 1544.75, 1551.25, 1655.25, 1567.25, 1546.0, 1535.25, 1591.25, 1591.25, 1626.25, 1603.25], [0, 1631.25, 1521.25, 1505.75, 1512.5, 1584.0, 1538.75, 1552.75, 1532.5, 1496.0, 1505.0, 1518.25, 1543.75, 1547.0, 1570.75, 1610.25, 1570.0, 1559.5, 1541.25, 1547.5, 1523.25, 1570.25, 1558.75, 1515.75, 1546.5, 1539.25, 1558.0, 1562.25, 1588.75, 1610.5, 1607.0, 0.0], [0, 1645.75, 1603.25, 1641.5, 1610.0, 1649.5, 1655.25, 1661.5, 1647.75, 1677.25, 1641.75, 1685.25, 1648.0, 1699.25, 1715.0, 1722.75, 1681.0, 1683.5, 1721.5, 1730.5, 1697.25, 1664.25, 1638.75, 1644.0, 1656.25, 1747.75, 1710.5, 1707.0, 1681.25, 1736.25, 1678.0, 1596.0], [0, 1624.25, 1699.75, 1668.75, 1705.0, 1713.25, 1748.25, 1683.0, 1679.75, 1692.75, 1701.75, 1705.0, 1705.0, 1725.0, 1720.25, 1715.25, 1717.5, 1728.0, 1728.5, 1736.75, 1747.25, 1756.25, 1749.0, 1790.5, 1753.75, 1742.25, 1745.25, 1710.5, 1691.5, 1699.25, 1766.0, 0.0], [0, 1826.75, 1798.25, 1799.5, 1804.75, 1803.0, 1817.75, 1774.5, 1828.25, 1824.25, 1840.25, 1834.25, 1901.75, 1854.25, 1889.5, 1842.0, 1860.75, 1847.25, 1847.75, 1872.5, 1923.75, 1962.0, 1982.25, 1950.5, 1936.0, 1988.75, 1988.0, 2043.5, 2104.0, 2080.25, 2068.25, 2010.25]]
a_20 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1958, 1958, 1985, 1944, 1921, 2001, 1959, 1916, 2047, 2015, 1867, 1958, 1992, 2005, 1958, 1954, 2040, 1952, 1951, 1936, 1929, 2020, 2027, 1994, 2017, 1886, 2039, 2024, 1969, 1917, 1962], [0, 1921, 1883, 1995, 1962, 1818, 1928, 1880, 1914, 1874, 1899, 1964, 2018, 1944, 1988, 1872, 1772, 1884, 1896, 1998, 1842, 1850, 1801, 1864, 2055, 1984, 1974, 1854, 1932, 1862, 0, 0], [0, 1906, 2019, 2030, 1897, 2085, 2207, 2157, 2182, 2393, 2480, 2461, 2614, 2731, 2707, 2711, 2770, 2903, 3101, 3124, 3222, 3334, 3299, 3339, 3279, 3330, 3334, 3435, 3380, 3162, 3225, 2969], [0, 3024, 2992, 2899, 2825, 2782, 2766, 2748, 2745, 2588, 2668, 2661, 2560, 2598, 2509, 2380, 2240, 2307, 2320, 2231, 2318, 2124, 2055, 2038, 2005, 2071, 1982, 1994, 1944, 1921, 1798, 0], [0, 1835, 1769, 1773, 1791, 1798, 1891, 1795, 1775, 1719, 1695, 1694, 1689, 1697, 1712, 1739, 1622, 1682, 1735, 1661, 1631, 1536, 1575, 1606, 1547, 1596, 1592, 1494, 1579, 1541, 1561, 1461], [0, 1585, 1593, 1627, 1554, 1592, 1579, 1462, 1569, 1540, 1522, 1369, 1547, 1536, 1464, 1545, 1595, 1589, 1556, 1540, 1574, 1530, 1663, 1678, 1716, 1719, 1711, 1684, 1666, 1754, 1721, 0], [0, 1792, 1819, 1795, 1666, 1593, 1684, 1594, 1523, 1638, 1698, 1567, 1571, 1522, 1484, 1593, 1557, 1534, 1468, 1498, 1577, 1625, 1671, 1568, 1680, 1525, 1479, 1591, 1599, 1688, 1775, 1888], [0, 1902, 1923, 1907, 1735, 1517, 1656, 1639, 1627, 1636, 1741, 1732, 1687, 1758, 1698, 1621, 1713, 1666, 1692, 1613, 1586, 1612, 1646, 1588, 1634, 1525, 1578, 1569, 1592, 1590, 1552, 1498], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Prima data 24/2
# giorni dall'1 gennaio al 24 febbraio: 55
count = 0
with open(filepath) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if (row[8] != 'nuovi_positivi'):
            data = row[0].split('T')[0]
            tmp = data.split('-')
            giorno = int(tmp[2])
            mese = int(tmp[1])
            anno = int(tmp[0])

            data = "new Date(" + tmp[0] + "," + tmp[1] + "," + tmp[2] +")"

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
            decessi_giornalieri_15_18_media = a_15_18[mese][giorno]
            decessi_giornalieri_totali_italia = a_20[mese][giorno]

            deceduti = int(row[10])
            deceduti_giornalieri = deceduti - deceduti_prec
            #casi_da_sospetto_diagnostico = int(row[11])
            #casi_da_screening = int(row[12])
            totale_casi = int(row[13])
            tamponi = int(row[14])
            #casi_testati = int(row[15])

            # OLD GRAPHS
            positivi.append(totale_positivi)
            rapporto.append(nuovi_positivi/(tamponi - precedente))
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

            # NEW GRAPHS
            positivi_tamponi = round( (nuovi_positivi/(tamponi - precedente))*100, 2)
            
            j_r_positivi_tamponi.append({"date": data, "r": positivi_tamponi, "positives": nuovi_positivi})

            ricoverati_positivi = round((totale_ospedalizzati/totale_positivi)*100 ,2)
            j_r_ricoverati_positivi.append({"date": data, "value": ricoverati_positivi})

            terapia_ospedalizzati = round(terapia_intensiva/ricoverati_con_sintomi*100, 2)
            j_r_terapia_ospedalizzati.append({"date": data, "value": terapia_ospedalizzati})

            decessi_20_decessi_15_18 = round( (decessi_giornalieri_totali_italia/decessi_giornalieri_15_18_media)*100, 2 )
            j_r_decessi_20_decessi_15_18.append({"date": data, "value": decessi_20_decessi_15_18})

            if decessi_giornalieri_totali_italia != 0:
                decessi_covid_decessi_20 = round( (deceduti_giornalieri/decessi_giornalieri_totali_italia)*100, 2 )
                j_r_decessi_covid_decessi_20.append({"date": data, "value": decessi_covid_decessi_20})
            else:
                j_r_decessi_covid_decessi_20.append({"date": data, "value": 0})

            dimessi_guariti_prec = dimessi_guariti
            deceduti_prec = deceduti
            terapia_intensiva_prec = terapia_intensiva
            isolamento_domiciliare_prec = isolamento_domiciliare
            count += 1
            precedente = int(row[14])

# Writes data' jsons for graphs
f = open("js/datas/j_r_positivi_tamponi.json", "w")
f.write(json.dumps(j_r_positivi_tamponi))

f = open("js/datas/j_r_ricoverati_positivi.json", "w")
f.write(json.dumps(j_r_ricoverati_positivi))

f = open("js/datas/j_r_terapia_ospedalizzati.json", "w")
f.write(json.dumps(j_r_terapia_ospedalizzati))

f = open("js/datas/j_r_decessi_20_decessi_15_18.json", "w")
f.write(json.dumps(j_r_decessi_20_decessi_15_18))

f = open("js/datas/j_r_decessi_covid_decessi_20.json", "w")
f.write(json.dumps(j_r_decessi_covid_decessi_20))

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
plt.ylabel("Daily entered / exited from Hospitalization")
plt.xlabel("Day")
plt.plot(r_entrati_usciti_terapia, 'g')
plt.savefig("imgs/r_entered_exited_hosp.png")
plt.close()

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
