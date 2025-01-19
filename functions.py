import pandas as pd
import re


def extrai_ID(link):
    padrao = r"(.*?/d/)([^/]+)/edit"
    correspondencia = re.search(padrao, link)
    if correspondencia:
        antes_do_id = correspondencia.group(1)
        id_planilha = correspondencia.group(2)
        return antes_do_id, id_planilha
    else:
        return None, None

def le_sheets(link):
    docs_link, id = extrai_ID(link)
    df = pd.read_csv(f"{docs_link}{id}/export?format=csv")
    return df

le_sheets("https://docs.google.com/spreadsheets/d/1b5v4makJSmBwjxz7qk1uwJyDwQ04mN7tm3-dbumcpYQ/edit?gid=328103558#gid=328103558")