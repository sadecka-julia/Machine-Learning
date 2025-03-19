import pandas as pd
import pysrt
import matplotlib.pyplot as plt
import seaborn as sns
# import seaborn.objects as so
import numpy as np
from collections import Counter

# Wyświetlenie danych w tabeli
path = "D:\\STUDIA\\Cyberka\\Magisterka_1\\Uczenie_maszynowe\\Lab_2\\data\\Star.Trek.Picard.S01E01.PROPER.WEBRip.x264-ION10.srt"
f = pysrt.open(path, encoding='cp1250') # Trzeba zmienić kodowanie, bo inaczej wyskakuje błąd

data = []
for sub in f:
    data.append({
        "Indeks": sub.index,
        "Czas startu": str(sub.start),
        "Czas końca": str(sub.end),
        "t": str(sub.end - sub.start),   # Zad 2. Dodatkowe linie
        "l": len(sub.text),
        "n": sub.text.count('\n')+1,
        "Tekst": sub.text.replace('\n', ' ')
    })

df = pd.DataFrame(data)
# print(df.to_string(index=False)) # Żeby dwa razy się indeks nie wyświetlał
# print(df.tail)
df["Czas startu"] = pd.to_datetime(df["Czas startu"], format="%H:%M:%S,%f")
df["Czas końca"] = pd.to_datetime(df["Czas końca"], format="%H:%M:%S,%f")
df["t"] = pd.to_timedelta(df["t"])
df["t"] = df["t"].dt.total_seconds()

# Statystki
'''
statystyki = df[["t", "l", "n"]].describe()
df["t"].mean()  # Średnia
df["t"].median()  # Mediana
df["t"].min()  # Minimum
df["t"].max()  # Maksimum
df["t"].std()  # Odchylenie standardowe
df["l"].var()  # Wariancja
df["t"].mode()  # Dominanta (najczęstsza wartość)
df["t"].count()  # Liczba niepustych wartości
df["t"].nunique()  # Liczba unikalnych wartości
df["t"].value_counts()  # Ile razy występują różne wartości
'''
# Grupowanie
'''
grupa_t = df.groupby(pd.cut(df["t"], bins=5)).agg({"l": ["mean", "median", "min", "max"], "n": ["mean", "median", "min", "max"]})  # dzieli na 5 przedziałów czasowych
grupa_n = df.groupby("n").agg({"t": ["mean", "median", "min", "max"], "l": ["mean", "median", "min", "max"]})
print(grupa_t)
print(grupa_n)
'''
# raport w Latexu
'''
with open("raport.tex", "w", encoding="utf-8") as f:
    f.write(statystyki.to_latex())
    f.write("\n\n Grupowanie po czasie trwania\n")
    f.write(grupa_t.to_latex())
    f.write("\n\n Grupowanie po liczbie linii\n")
    f.write(grupa_n.to_latex())
'''
# Wykres czasu trwania
'''
plt.figure(figsize=(10,5))
sns.scatterplot(x=df["Czas startu"], y=df["Czas końca"], alpha=0.7)
plt.xlabel("Czas startu napisu")
plt.ylabel("Czas końca napisu")
plt.title("Wykres czasu trwania")
plt.show(block=True)
'''

# Histogram czasu trwania napisów z podziałem na n
'''
plt.figure(figsize=(10,5))
sns.histplot(df, x="t", hue="n")
plt.show(block=True)
'''

# Histogram liczby znaków w napisach z podziałem na n
'''
plt.figure(figsize=(10, 5))
sns.histplot(df, x="l", hue="n", bins=30, kde=True, palette="coolwarm", alpha=0.6)
# Opisy osi i tytuł
plt.xlabel("Liczba znaków w napisach")
plt.ylabel("Liczba wystąpień")
plt.title("Histogram liczby znaków w napisach z podziałem na liczbę linii (n)")

plt.show()
'''

# Boxplot t z podziałem na n
'''
plt.figure(figsize=(10, 5))
sns.boxplot(x="n", y="t", data=df, palette="coolwarm")

# Opisy osi i tytuł
plt.xlabel("Liczba linii w napisie (n)")
plt.ylabel("Czas trwania napisów (sekundy)")
plt.title("Boxplot czasu trwania napisów z podziałem na liczbę linii (n)")

plt.show()
'''

# Scatter plot z l na osi X i t na osi Y. Dodatkowo, pokoloruj punkty według n.
'''
plt.figure(figsize=(10, 5))
sns.scatterplot(x="l", y="t", hue="n", data=df)
plt.xlabel("Liczba liter w napisie")
plt.ylabel("Czas trwania napisów (sekundy)")
plt.title("Scatter plot l na t")
plt.show()
'''

# wykres łącznego rozkładu t i l. Dodatkowo mapę hexbin i zapisać wykres do pdf
'''
sns.jointplot(data=df, x="t", y="l", kind="kde", fill=True, cmap="coolwarm")
# podajemy data, x, y, kind="kde" - wygląda jak mapa, fill, że wypełniona, cmap - kolorki mapy
plt.xlabel("t")
plt.ylabel("l")
plt.title("wykres łącznego rozkładu t i l")
plt.show()


plt.hexbin(df['t'], df['l'], gridsize=(15, 15))
plt.savefig("hexbin.pdf") # musi być przed show
plt.show()
'''
# Wygładź funkcję l(t) i zaprezentuj ją na wykresie.
# robi się to za pomocą funkcji sns.regplot, albo lowess
'''
plt.figure(figsize=(10, 5))
sns.regplot(x=df["t"], y=df["l"], lowess=True, scatter_kws={"alpha":0.3}, line_kws={"color":"red"})

plt.xlabel("Czas trwania napisu (t) [s]")
plt.ylabel("Liczba znaków (l)")
plt.title("Regresja wygładzona dla l(t)")

plt.show()
'''
# Oblicz zliczenia liter w jednostce czasu (np. litery na sekundę).
print(df['l']/df['t'])
plt.figure(figsize=(10, 5))
sns.histplot(df['l']/df['t'], bins=30, kde=True, color="purple")

plt.xlabel("Litery na sekundę")
plt.ylabel("Liczba wystąpień")
plt.title("Histogram liczby liter na sekundę")

plt.show()
# Oblicz rozkład częstości występowania poszczególnych liter w napisach.
caly_dubbing = " ".join(df["Tekst"])
litery_counter = Counter(caly_dubbing)
print(litery_counter)

litery_df = pd.DataFrame(litery_counter.items(), columns=["Litera", "Liczba"])
litery_df = litery_df.sort_values(by="Liczba", ascending=False)

# Wykres słupkowy częstości liter
plt.figure(figsize=(12, 6))
sns.barplot(x=litery_df["Litera"], y=litery_df["Liczba"], palette="magma")

plt.xlabel("Litera")
plt.ylabel("Częstość")
plt.title("Rozkład częstości występowania liter w napisach")
plt.xticks(rotation=45)  # Obrót etykiet dla czytelności

plt.show()

# Stwórz wykres łącznego rozkładu dwóch kolejnych liter w napisach.

