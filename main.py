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
comuni_giornaliero_path = "comuni_giornaliero_31luglio21.csv"

fileurl = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"

r = requests.get(fileurl, allow_redirects=True)

open('dpc-covid19-ita-andamento-nazionale.csv', 'wb').write(r.content)

lista_date = []
positivi = []
rapporto = []
terapia_intensiva_ = []
r_ricov_pos = []
casi_attivi = []
isolamento = []
r_terapia_ricov = []
r_guariti_positivi = []
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
j_r_dimessi_guariti_nuovi_positivi = []
j_r_dimessi_guariti_attualmente_positivi = []
j_r_deaths_positives = []
j_r_nuovi_positivi_usciti = []
j_intensive_variation = []

dimessi_guariti_prec = 0
deceduti_prec = 0
terapia_intensiva_prec = 0
isolamento_domiciliare_prec = 0
precedente = 0


def initMatrix():
    res = []
    for m in range(0, 13):
        tmp = []
        for d in range(0, 32):
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
    a_21 = initMatrix()
    a_15_18 = initMatrix()

    count = 0

    with codecs.open(comuni_giornaliero_path, encoding='utf-8',
                     errors='ignore') as csvfile2:
        reader = csv.reader(csvfile2, delimiter=',', quotechar='|')
        for row in reader:
            count += 1

            if count == 1:
                print(row[38])

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

                # print("Month: " + str(month))
                # print("Day: " + str(day))

                t_15 = int(row[36-1])
                t_16 = int(row[37-1])
                t_17 = int(row[38-1])
                t_18 = int(row[39-1])
                t_19 = int(row[40-1])
                if row[41-1] == 'n.d.':
                    t_20 = 0
                else:
                    t_20 = int(row[41-1])

                if row[42-1] == 'n.d.':
                    t_21 = 0
                else:
                    t_21 = int(row[42-1])

                a_15[month][day] += t_15
                a_16[month][day] += t_16
                a_17[month][day] += t_17
                a_18[month][day] += t_18
                a_19[month][day] += t_19
                a_20[month][day] += t_20
                a_21[month][day] += t_21

    for i in range(1, 13):
        for j in range(1, 32):
            # handle 29th of feb
            # only 2016 has 29th of feb
            if i == 2 and j == 29:
                a_15_18[i][j] = a_16[i][j]
            else:
                median = (a_15[i][j] + a_16[i][j] + a_17[i][j] + a_18[i][j])/4
                a_15_18[i][j] = median

    return a_15_18, a_21


#a_15_18, a_21 = generate_median_15_18()

#print("a_15_18=" + str(a_15_18))
#print("a_20=" + str(a_21))
# exit()

a_15_18 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2403.75, 2272.25, 2273.0, 2297.25, 2322.25, 2247.5, 2213.25, 2261.0, 2309.25, 2321.5, 2308.0, 2315.75, 2265.5, 2214.75, 2245.75, 2238.0, 2198.0, 2218.0, 2195.0, 2168.0, 2177.0, 2184.25, 2179.5, 2160.0, 2143.5, 2093.75, 2086.5, 2095.75, 2081.25, 2169.25, 2082.0], [0, 2194.0, 2131.25, 2089.0, 2058.5, 2045.5, 2060.25, 2049.75, 1989.25, 2014.5, 2022.0, 1997.5, 2002.25, 2028.25, 1989.0, 2029.25, 2022.0, 2013.25, 2005.0, 1947.5, 1928.75, 1977.75, 1992.75, 1982.5, 1960.25, 1935.0, 1946.5, 1922.5, 1944.25, 1770, 0.0, 0.0], [0, 1944.25, 1988.25, 1996.75, 1959.75, 1964.5, 1938.25, 1925.5, 1872.25, 1906.75, 1957.0, 1891.5, 1930.0, 1895.5, 1880.75, 1832.0, 1873.75, 1903.75, 1847.5, 1854.0, 1848.5, 1867.25, 1851.75, 1870.0, 1782.5, 1788.75, 1759.0, 1776.5, 1810.25, 1801.0, 1855.5, 1811.75], [0, 1838.25, 1740.25, 1795.5, 1768.25, 1792.25, 1765.5, 1729.0, 1738.75, 1725.25, 1755.25, 1753.75, 1755.0, 1767.25, 1769.5, 1744.25, 1697.75, 1735.0, 1695.0, 1685.25, 1671.75, 1693.25, 1682.25, 1727.5, 1671.5, 1645.5, 1679.25, 1743.0, 1687.0, 1658.0, 1620.0, 0.0], [0, 1642.25, 1704.5, 1680.0, 1657.75, 1696.25, 1688.0, 1698.5, 1667.0, 1654.0, 1636.0, 1617.0, 1638.0, 1679.75, 1595.25, 1615.0, 1580.0, 1613.75, 1644.25, 1612.25, 1576.5, 1587.5, 1600.25, 1588.0, 1607.75, 1615.0, 1615.0, 1615.5, 1609.25, 1650.0, 1625.25, 1600.0], [0, 1609.0, 1575.75, 1607.0, 1640.25, 1665.5, 1619.5, 1628.75, 1618.5, 1593.0, 1528.25, 1584.75, 1590.75, 1601.25, 1606.5, 1593.0, 1603.5, 1557.25, 1513.25, 1542.25, 1527.0, 1574.75, 1596.5, 1609.75, 1625.0, 1611.0, 1614.25,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          1591.25, 1570.5, 1542.0, 1576.5, 0.0], [0, 1594.0, 1593.5, 1649.75, 1636.25, 1655.75, 1670.5, 1696.25, 1757.75, 1676.25, 1675.0, 1712.75, 1706.75, 1699.0, 1653.25, 1667.5, 1649.25, 1623.5, 1631.75, 1706.5, 1731.0, 1744.5, 1739.0, 1784.75, 1707.75, 1672.5, 1671.0, 1622.5, 1592.25, 1636.25, 1650.25, 1647.75], [0, 1695.25, 1662.5, 1746.25, 1781.25, 1777.5, 1830.75, 1829.0, 1833.5, 1819.5, 1807.25, 1724.75, 1681.0, 1625.0, 1609.75, 1631.75, 1586.75, 1621.25, 1637.5, 1557.25, 1562.5, 1607.25, 1544.75, 1551.25, 1655.25, 1567.25, 1546.0, 1535.25, 1591.25, 1591.25, 1626.25, 1603.25], [0, 1631.25, 1521.25, 1505.75, 1512.5, 1584.0, 1538.75, 1552.75, 1532.5, 1496.0, 1505.0, 1518.25, 1543.75, 1547.0, 1570.75, 1610.25, 1570.0, 1559.5, 1541.25, 1547.5, 1523.25, 1570.25, 1558.75, 1515.75, 1546.5, 1539.25, 1558.0, 1562.25, 1588.75, 1610.5, 1607.0, 0.0], [0, 1645.75, 1603.25, 1641.5, 1610.0, 1649.5, 1655.25, 1661.5, 1647.75, 1677.25, 1641.75, 1685.25, 1648.0, 1699.25, 1715.0, 1722.75, 1681.0, 1683.5, 1721.5, 1730.5, 1697.25, 1664.25, 1638.75, 1644.0, 1656.25, 1747.75, 1710.5, 1707.0, 1681.25, 1736.25, 1678.0, 1596.0], [0, 1624.25, 1699.75, 1668.75, 1705.0, 1713.25, 1748.25, 1683.0, 1679.75, 1692.75, 1701.75, 1705.0, 1705.0, 1725.0, 1720.25, 1715.25, 1717.5, 1728.0, 1728.5, 1736.75, 1747.25, 1756.25, 1749.0, 1790.5, 1753.75, 1742.25, 1745.25, 1710.5, 1691.5, 1699.25, 1766.0, 0.0], [0, 1826.75, 1798.25, 1799.5, 1804.75, 1803.0, 1817.75, 1774.5, 1828.25, 1824.25, 1840.25, 1834.25, 1901.75, 1854.25, 1889.5, 1842.0, 1860.75, 1847.25, 1847.75, 1872.5, 1923.75, 1962.0, 1982.25, 1950.5, 1936.0, 1988.75, 1988.0, 2043.5, 2104.0, 2080.25, 2068.25, 2010.25]]

a_20 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1999, 2017, 2026, 1987, 1944, 2035, 1986, 1947, 2081, 2046, 1888, 1991, 2022, 2035, 1991, 1984, 2066, 1976, 1975, 1965, 1956, 2050, 2043, 2017, 2048, 1910, 2066, 2047, 1990, 1942, 1989], [0, 1960, 1906, 2021, 1980, 1845, 1952, 1908, 1935, 1896, 1925, 1992, 2045, 1976, 2013, 1898, 1792, 1901, 1915, 2017, 1860, 1875, 1810, 1879, 2072, 2003, 1993, 1871, 1954, 1876, 0, 0], [0, 1927, 2038, 2047, 1912, 2110, 2224, 2173, 2202, 2409, 2498, 2486, 2635, 2752, 2728, 2726, 2789, 2931, 3124, 3153, 3248, 3358, 3326, 3367, 3302, 3355, 3361, 3470, 3412, 3190, 3254, 2994], [0, 3054, 3018, 2926, 2850, 2805, 2806, 2780, 2775, 2618, 2690, 2692, 2588, 2633, 2536, 2401, 2260, 2336, 2337, 2254, 2334, 2145, 2075, 2060, 2031, 2083, 1997, 2011, 1961, 1935, 1818, 0], [0, 1856, 1783, 1792, 1812, 1816, 1906, 1810, 1798, 1748, 1714, 1710, 1713, 1723, 1733, 1757, 1644, 1696, 1759, 1683, 1650, 1557, 1603, 1630, 1565, 1616, 1620, 1509, 1597, 1573, 1588, 1479], [0, 1609, 1610, 1643, 1583, 1614, 1600, 1485, 1585, 1563, 1545, 1395, 1579, 1554, 1487, 1587, 1622, 1612, 1580, 1565, 1599, 1558, 1696,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             1707, 1742, 1755, 1747, 1724, 1699, 1785, 1759, 0], [0, 1825, 1867, 1835, 1694, 1631, 1714, 1630, 1554, 1672, 1727, 1591, 1596, 1560, 1518, 1628, 1600, 1565, 1503, 1549, 1610, 1658, 1717, 1612, 1715, 1574, 1507, 1628, 1636, 1739, 1824, 1943], [0, 1968, 1986, 1968, 1783, 1571, 1707, 1696, 1681, 1709, 1815, 1797, 1751, 1820, 1762, 1683, 1782, 1744, 1770, 1677, 1659, 1688, 1726, 1650, 1735, 1626, 1676, 1679, 1694, 1699, 1652, 1590], [0, 1595, 1589, 1568, 1611, 1647, 1662, 1619, 1580, 1675, 1725, 1670, 1736, 1622, 1779, 1723, 1807, 1582, 1669, 1656, 1605, 1659, 1625, 1592, 1607, 1617, 1522, 1557, 1640, 1691, 1696, 0], [0, 1710, 1816, 1831, 1633, 1867, 1700, 1703, 1731, 1733, 1764, 1748, 1831, 1636, 1799, 1913, 1844, 1851, 1872, 1997, 2012, 2105, 2090, 2153, 2046, 2144, 2129, 2220, 2197, 2159, 2288, 2339], [0, 2327, 2388, 2482, 2417, 2558, 2509, 2468, 2513, 2651, 2602, 2629, 2695, 2601, 2697, 2772, 2707, 2725, 2735, 2782, 2762, 2532, 2541, 2715, 2703, 2746, 2734, 2699, 2691, 2599, 2490, 0], [0, 2568, 2584, 2646, 2623, 2459, 2625, 2528, 2525, 2598, 2489, 2430, 2486, 2426, 2387, 2471, 2495, 2427, 2468, 2443, 2382, 2255, 2322, 2338, 2290, 2243, 2128, 2127, 2278, 2283, 2370, 2201]]

a_21 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2366, 2406, 2310, 2378, 2387, 2319, 2368, 2425, 2387, 2290, 2349, 2337, 2376, 2433, 2437, 2382, 2351, 2439, 2496, 2454, 2371, 2499, 2393, 2315, 2317, 2321, 2195, 2357, 2316, 2321, 2283], [0, 2279, 2249, 2190, 2241, 2223, 2155, 2086, 2056, 2108, 2013, 2069, 1992, 1930, 1949, 2002, 2065, 2179, 2189, 2144, 2158, 2017, 2039, 2031, 2002, 2018, 2086, 2082, 1970, 0, 0, 0], [0, 2116, 2028, 2141, 2046, 2108, 2124, 1976, 2139, 2126, 2150, 2109, 2225, 2211, 2056, 2185, 2092, 2227, 2220, 2278, 2165, 2166, 2202, 2250, 2301, 2249, 2348, 2249, 2142, 2284, 2235, 2326], [0, 2273, 2209, 2192, 2093, 2037, 2222, 2149, 2131, 2130, 2082, 2104, 2157, 2054, 2029, 1977, 1961, 2043, 2039, 2060, 2028, 2020, 2009, 2070, 1990, 1984, 2050, 1910, 1972, 1924, 1883, 0], [0, 1810, 1793, 1787, 1766, 1778, 1721, 1844, 1745, 1787, 1784, 1783, 1824, 1672, 1695, 1695, 1620,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           1731, 1731, 1645, 1696, 1740, 1620, 1646, 1810, 1707, 1635, 1682, 1647, 1697, 1479, 1570], [0, 1694, 1608, 1679, 1634, 1716, 1667, 1690, 1665, 1689, 1687, 1629, 1576, 1578, 1669, 1540, 1619, 1617, 1640, 1610, 1616, 1733, 1765, 1779, 1858, 1845, 1748, 1681, 1726, 1760, 1714, 0], [0, 1787, 1616, 1686, 1635, 1613, 1568, 1674, 1736, 1648, 1669, 1632, 1690, 1751, 1584, 1548, 1574, 1492, 1530, 1578, 1578, 1624, 1657, 1682, 1620, 1654, 1629, 1719, 1686, 1718, 1835, 1750], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

print(a_20[6][24])
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

            data = "new Date(" + tmp[0] + "," + tmp[1] + "," + tmp[2] + ")"

            ricoverati_con_sintomi = int(row[2])
            terapia_intensiva = int(row[3])
            terapia_intensiva_giornalieri = terapia_intensiva - terapia_intensiva_prec
            totale_ospedalizzati = int(row[4])
            isolamento_domiciliare = int(row[5])
            isolamento_domiciliare_giornalieri = isolamento_domiciliare - \
                isolamento_domiciliare_prec
            totale_positivi = int(row[6])
            variazione_totale_positivi = int(row[7])
            nuovi_positivi = int(row[8])
            dimessi_guariti = int(row[9])
            dimessi_guariti_giornalieri = dimessi_guariti - dimessi_guariti_prec
            decessi_giornalieri_15_18_media = a_15_18[mese][giorno]

            if (anno == 2020):
                decessi_giornalieri_totali_italia = a_20[mese][giorno]
            elif anno == 2021:
                decessi_giornalieri_totali_italia = a_21[mese][giorno]
            else:
                decessi_giornalieri_totali_italia = 0

            deceduti = int(row[10])
            deceduti_giornalieri = deceduti - deceduti_prec
            # casi_da_sospetto_diagnostico = int(row[11])
            # casi_da_screening = int(row[12])
            totale_casi = int(row[13])
            tamponi = int(row[14])
            # casi_testati = int(row[15])

            # OLD GRAPHS
            positivi.append(totale_positivi)
            rapporto.append(nuovi_positivi/(tamponi - precedente))
            r_ricov_pos.append(totale_ospedalizzati/totale_positivi)
            r_terapia_ricov.append(terapia_intensiva/ricoverati_con_sintomi)
            terapia_intensiva_.append(terapia_intensiva)
            r_guariti_positivi.append(
                dimessi_guariti_giornalieri/totale_positivi)
            r_guariti_nuovi_positivi.append(
                dimessi_guariti_giornalieri/nuovi_positivi)
            r_deceduti_positivi.append(deceduti/totale_casi)
            r_nuovipositivi_usciti.append(
                nuovi_positivi/(dimessi_guariti_giornalieri+deceduti_giornalieri))
            r_deceduticovid_deceduti_norm.append(
                deceduti_giornalieri/decessi_giornalieri_15_18_media)
            var_terapia_intensiva.append(terapia_intensiva_giornalieri)
            baseline.append(0)

            # NEW GRAPHS
            positivi_tamponi = round(
                (nuovi_positivi/(tamponi - precedente))*100, 2)

            j_r_positivi_tamponi.append(
                {"date": data, "r": positivi_tamponi, "positives": nuovi_positivi})

            ricoverati_positivi = round(
                (totale_ospedalizzati/totale_positivi)*100, 2)
            j_r_ricoverati_positivi.append(
                {"date": data, "value": ricoverati_positivi})

            terapia_ospedalizzati = round(
                terapia_intensiva/ricoverati_con_sintomi*100, 2)
            j_r_terapia_ospedalizzati.append(
                {"date": data, "value": terapia_ospedalizzati})

            decessi_20_decessi_15_18 = round(
                (decessi_giornalieri_totali_italia/decessi_giornalieri_15_18_media)*100, 2)
            j_r_decessi_20_decessi_15_18.append(
                {"date": data, "value": decessi_20_decessi_15_18})

            if decessi_giornalieri_totali_italia != 0:
                decessi_covid_decessi_20 = round(
                    (deceduti_giornalieri/decessi_giornalieri_totali_italia)*100, 2)
                j_r_decessi_covid_decessi_20.append(
                    {"date": data, "value": decessi_covid_decessi_20})
            else:
                j_r_decessi_covid_decessi_20.append({"date": data, "value": 0})

            dimessi_guariti_nuovi_positivi = round(
                (dimessi_guariti_giornalieri / nuovi_positivi)*100, 2)
            j_r_dimessi_guariti_nuovi_positivi.append(
                {"date": data, "value": dimessi_guariti_nuovi_positivi})

            dimessi_guariti_attualmente_positivi = round(
                (dimessi_guariti_giornalieri / totale_positivi)*100, 2)
            j_r_dimessi_guariti_attualmente_positivi.append(
                {"date": data, "value": dimessi_guariti_attualmente_positivi})

            deaths_positives = round((deceduti/totale_casi)*100, 2)
            j_r_deaths_positives.append(
                {"date": data, "value": deaths_positives})

            nuovi_positivi_usciti = round(
                (nuovi_positivi/(dimessi_guariti_giornalieri + deceduti_giornalieri)))
            j_r_nuovi_positivi_usciti.append(
                {"date": data, "value": nuovi_positivi_usciti})

            intensive_variation = terapia_intensiva - terapia_intensiva_prec
            j_intensive_variation.append(
                {"date": data, "value": intensive_variation})

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

f = open("js/datas/j_r_dimessi_guariti_nuovi_positivi.json", "w")
f.write(json.dumps(j_r_dimessi_guariti_nuovi_positivi))

f = open("js/datas/j_r_dimessi_guariti_attualmente_positivi.json", "w")
f.write(json.dumps(j_r_dimessi_guariti_attualmente_positivi))

f = open("js/datas/j_r_deaths_positives.json", "w")
f.write(json.dumps(j_r_deaths_positives))

f = open("js/datas/j_r_nuovi_positivi_usciti.json", "w")
f.write(json.dumps(j_r_nuovi_positivi_usciti))

f = open("js/datas/j_intensive_variation.json", "w")
f.write(json.dumps(j_intensive_variation))

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
