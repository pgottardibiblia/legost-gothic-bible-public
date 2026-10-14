#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

# --- FUNZIONE PER SOSTITUIRE GLI SPAZI NEGLI ELEMENTI RACCHIUSI TRA PARENTESI CON TRATTINI BASSI '_'

def from_space_to_line(file_input):
    """
    Individua le unità parentetiche.
    Dopodiché, sostituisce gli spazi all'interno con dei trattini bassi '_'.
    Infine, salva il testo come file di testo.
    
    :param file_input: Percorso del file di input (.txt)
    """
    
    import re

    # Carica il documento
    with open(file_input, 'r', encoding='UTF-8') as f:
        text = f.read()
    
    # Suddivide il testo in righe
    text_lines = text.splitlines()
    fixed_text = [] 
    
    # Per ogni rigo, identifica i metadati tra parentesi quadre
    for line in text_lines:
        new_line = []
        while "[" in line:
            metadati = re.findall(r'\[.*?\]', line)
            if metadati:
                sub_metadato = metadati[0]
                # Aggiungi la parte prima del metadato
                precedente_metadato = line.split(sub_metadato)[0]
                new_line.append(precedente_metadato)
                #Ridefinisci la parte restante del rigo come rigo da considerare
                line = line[len(precedente_metadato + sub_metadato):]
                
                #Correzione se presenti metadati nidificati
                openings = 0
                closures = 0
                for c in sub_metadato:
                    if c == "[":
                        openings = openings+1
                    elif c == "]":
                        closures = closures+1
                while openings>closures:
                    da_considerare = line.split("]")[0] + "]"
                    for c in da_considerare:
                        if c == "[":
                            openings = openings+1
                        elif c == "]":
                            closures = closures+1
                    line = line[len(line.split("]")[0] + "]"):]
                    sub_metadato = sub_metadato + da_considerare
                
                #Sostituzione degli spazi con i trattini bassi    
                sub_metadato = re.sub(" ", "_", sub_metadato)
                new_line.append(sub_metadato)
            else:
                break
        
        # Aggiungi il resto del rigo
        new_line.append(line)
        
        # Ricomposizione del rigo corretto
        fixed_text.append(''.join(new_line))

    # Salva il documento modificato in .txt
    with open(file_input[:-4] + " corretto.txt", 'w', encoding="UTF-8") as txt_out:
        txt_out.write('\n'.join(fixed_text))
    
    # Comunica la fine dell'operazione
    print(f"Documento salvato in: {file_input[:-4]} corretto.txt")
