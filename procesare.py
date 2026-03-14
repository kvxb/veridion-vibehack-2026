import pandas as pd
import json
import ast

def parse_stringified_dict(val):
    """
    Unele câmpuri (ex: address) sunt salvate ca string-uri ce conțin dicționare.
    Funcția asta le transformă înapoi în dicționare reale de Python.
    """
    if pd.isna(val):
        return {}
    if isinstance(val, dict):
        return val
    try:
        # Folosim literal_eval pentru a citi string-uri formatate ca dict
        return ast.literal_eval(val)
    except:
        return {}

def main():
    print("Începem citirea și procesarea datelor...")
    
    # 1. Citim fișierul original (format JSON Lines)
    data = []
    with open('companies.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    # Încărcăm totul într-un tabel de lucru (DataFrame)
    df = pd.DataFrame(data)

    # 2. Generăm ID-ul Unic (Cheia care vă unește sistemele)
    # Va arăta așa: COMP_00001, COMP_00002 etc.
    df['company_id'] = ['COMP_' + str(i).zfill(5) for i in range(1, len(df) + 1)]

    # 3. Parsăm coloanele ascunse și extragem exact ce ai tu nevoie
    df['address_dict'] = df['address'].apply(parse_stringified_dict)
    df['naics_dict'] = df['primary_naics'].apply(parse_stringified_dict)

    df['country_code'] = df['address_dict'].apply(lambda x: x.get('country_code'))
    df['region_name'] = df['address_dict'].apply(lambda x: x.get('region_name'))
    df['town'] = df['address_dict'].apply(lambda x: x.get('town'))
    df['primary_naics_code'] = df['naics_dict'].apply(lambda x: x.get('code'))

    # 4. Curățăm datele numerice pentru baza TA de date
    # Folosim 'Int64' care suportă valori <NA> (adică NULL-uri perfecte pentru baza de date)
    df['year_founded'] = pd.to_numeric(df['year_founded'], errors='coerce').astype('Int64')
    df['employee_count'] = pd.to_numeric(df['employee_count'], errors='coerce').astype('Int64')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce') # Rămâne float pt sume mari

    # Selectăm strict coloanele tale (fără descrieri greoaie)
    tabular_columns = [
        'company_id', 'operational_name', 'website', 'year_founded', 
        'employee_count', 'revenue', 'country_code', 'region_name', 
        'town', 'primary_naics_code', 'is_public'
    ]
    df_tabular = df[tabular_columns]

    # Salvăm fișierul tău
    df_tabular.to_csv('date_structurate_pentru_tine.csv', index=False)
    print("✅ Salvat: date_structurate_pentru_tine.csv (Pentru Hard Filters)")

    # 5. Pregătim datele semantice pentru PRIETENUL TĂU
    def build_semantic_text(row):
        parts = []
        if pd.notna(row.get('description')):
            parts.append(f"Description: {row['description']}")
        if isinstance(row.get('business_model'), list):
            parts.append(f"Business model: {', '.join(row['business_model'])}.")
        if isinstance(row.get('target_markets'), list):
            parts.append(f"Target markets: {', '.join(row['target_markets'])}.")
        if isinstance(row.get('core_offerings'), list):
            parts.append(f"Core offerings: {', '.join(row['core_offerings'])}.")
        
        return " | ".join(parts)

    df['semantic_text'] = df.apply(build_semantic_text, axis=1)

    # El are nevoie doar de ID și Textul pentru vectorizare
    df_semantic = df[['company_id', 'semantic_text']]

    # Salvăm fișierul lui (JSON Lines e formatul preferat pentru sisteme AI/Vectoriale)
    df_semantic.to_json('date_semantice_pentru_el.json', orient='records', lines=True)
    print("✅ Salvat: date_semantice_pentru_el.json (Pentru AI / Embeddings)")

if __name__ == "__main__":
    main()