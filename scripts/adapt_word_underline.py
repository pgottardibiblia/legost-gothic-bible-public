#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

    

# --- FUNZIONE PER ADATTARE LE SOTTOLINEATURE NEL FILE WORD IN MARKDOWN '[un.:]'

def adapt_word_underline(file_input, file_output):
    """
    Rimuove la sottolineatura dagli spazi in un documento Word.
    Dopodiché, aggiunge il testo "[un.:" prima di ogni porzione di testo sottolineata
    in un documento Word e il testo "]" alla fine della porzione di testo.
    Quindi, converte il testo in stringa e corregge gli errori di conversione relativi alle parole sottolineate e interrotte dalla fine del rigo
    Infine, salva il testo come file di testo.
    
    :param file_input: Percorso del file di input (.docx)
    :param file_output: Percorso del file di output (.txt)
    """
    
    from docx import Document
    import re
    
    # Carica il documento
    doc = Document(file_input)
    
    # Itera su tutti i paragrafi del documento
    for paragraph in doc.paragraphs:
        # Crea una lista per i nuovi "run"
        nuovi_runs = []
        for run in paragraph.runs:
            if run.underline:  # Se il testo è sottolineato
                run.underline = False
                testo_sottolineato = str(run.text)
                testo_sottolineato = testo_sottolineato.split(" ")
                for n, elem in enumerate(testo_sottolineato):
                    if elem != "":
                        # Aggiungi il prefisso "[un.:"
                        nuovi_runs.append("[un.:")
                        # Aggiungi il testo originale
                        nuovi_runs.append(elem)
                        # Aggiungi il suffisso "]"
                        nuovi_runs.append("]")
                    # Aggiungi spazio
                    nuovi_runs.append(" ")
                nuovi_runs = nuovi_runs[:-1]
            else:
                nuovi_runs.append(run.text)

        # Ricostruisci il paragrafo con i nuovi "run"
        paragraph.clear()  # Rimuovi i contenuti originali del paragrafo
        for testo in nuovi_runs:
            nuovo_run = paragraph.add_run(testo)

    #Converti il docx in una stringa
    txt_text = ""
    for paragraph in doc.paragraphs:
        txt_text = txt_text + paragraph.text + "\n"
    
    #Correggi quando il tratto delle parole interrotte dalla fine del rigo non è nella parentesi quadra    
    re.sub("] -", "]-", txt_text)
    
    # Salva il documento modificato in .txt
    with open(file_output, 'w', encoding="UTF-8") as txt_out:
        txt_out.write(txt_text)
    
    #Comunica la fine dell'operazione
    print(f"Documento salvato in: {file_output}")
