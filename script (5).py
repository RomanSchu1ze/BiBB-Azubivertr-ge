#!/usr/bin/env python
# coding: utf-8

# ### BiBB Ausbildungsverträge

# In[6]:


# Bibliotheken laden
import numpy as np
import pandas as pd


# In[7]:


# Bereinigung der Daten
def clean_data(df):
    df.replace(".", np.nan, inplace=True)
    for col in df.columns:
        if col not in ["KldB", "Beruf", "Geschlecht"]:
            df[col] = df[col].astype("float64")
    return df


# In[8]:


# Auflistung der Bundesländer
Bundesländer = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern",
               "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen-Anhalt", "Sachsen", 
               "Schleswig-Holstein", "Thüringen"]


# In[9]:


# Relevante KldB´s
KldB = [
51522,
52202,
26112,
51412,
25102,
32232,
53112,
26312,
51622,
63302,
71302,
51312,
54112,
25212,
52522,
43102,
26302,
52132,
52122,
43412,
24232,
27212,
61312,
34212,
63312,
29302,
34232,
71522,
26252,
43112,
43312,
71402,
43232,
32112,
31212,
26122,
24412,
28242,
22212,
42202,
26222,
62272,
25222,
25252,
23422,
32202
]


# In[10]:


# leere Liste, um Ergebnisse zu speichern
list_of_df = []
# Da Datei mit mehreren Sheets, durch jedes Arbeitsblatt gehen
for Bundesland in Bundesländer:
    # Daten einlesen
    df = pd.read_excel("Rohdaten.xlsx", sheet_name=Bundesland, skiprows=2)
    # Relevante Zeilen und Spalten behalten
    df = df.iloc[1:, 1:]
    # Spaltennamen definieren
    columns = ["KldB", "Beruf", "Geschlecht", "2018", "2018 %", "2019", "2019 %", "2020", "2020 %"]
    # Spaltennamen anpassen
    df.columns = columns
    # fülle Missings
    df.loc[:,"KldB"].fillna(method="ffill", inplace=True)
    # fülle Missings
    df.loc[:,"Beruf"].fillna(method="ffill", inplace=True)
    # Bereinigung der Daten
    df = clean_data(df)
    # Bundesland als Spalte hinzufügen
    df["Bundesland"] = Bundesland
    # Dataframe der Liste hinzufügen
    list_of_df.append(df)


# In[11]:


# Zusammenführung der Daten
df = pd.concat(list_of_df)


# In[12]:


# Format Dataframe
df.shape


# In[13]:


# Datentypen
df.dtypes


# In[24]:


# Dataframe auf relevante Azubis kürzen
final = df[df.KldB.isin(KldB)]


# In[25]:


# Format des finalen Dataframes-> beinhaltet 46 individuelle Ausbildungsberufe
final.shape


# In[34]:


# Überprüfe Format
16*45*3


# In[27]:


# individuelle KldB Codes
final.KldB.unique()


# In[28]:


# individuelle gefilterte KldB
np.sort(KldB)


# In[29]:


# Abgleich,  es fehlt 42202 Umweltschutztechn. Assistent
print("Unique values in KldB that are not in the final dataframe:")
print(np.setdiff1d(np.sort(KldB), final.KldB.unique()))


# In[30]:


# Sortierung der Spalten
columns = ["Bundesland", "Beruf", "Geschlecht", "KldB", "2018", "2018 %", "2019", "2019 %", "2020", "2020 %"]
final = final[columns]


# In[31]:


# Anpssung der % Spalten
final["2018 %"] = final["2018 %"] / 100
final["2019 %"] = final["2019 %"] / 100
final["2020 %"] = final["2020 %"] / 100


# In[32]:


# erste fünf Zeilen
final.head()


# In[33]:


# als Excel speichern
final.to_excel("BiBB_Azubiverträge.xlsx", index=False)


# In[ ]:




