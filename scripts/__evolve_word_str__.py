#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

from __conversione_posizione__ import __conversione_posizione__


# --- SUBFUNZIONE PER EDITING TEI XML DI SINGOLI VOCABOLI IN FORMATO STRINGA ---
# --- (funziona relatamente al sistema di trascrizione da me adottato) ---
# --- (produce un output lista composta da stringa in markup, tipo di elemento e se la parola è interrotta dalla fine del rigo o della pagina)

def __evolve_word_str__(word_text, n_token, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro):
    import re
    import xml.etree.ElementTree as ET
    
    parola_o_punto_o_numero_segmento = "parola"
    parola_spezzata_fra_righi = False
    xml_id_data = "{}_".format(ID_testimone) + "{}" + "_{}_{}_{}".format(n_foglio, n_rigo_per_foglio, n_token)
    tachigrafie = ['i(esu)s', 'i(es)u', 'i(esu)a', 'i(es)ua', 'ï(esu)s', 'i(esu)is', 'i(es)uis', 
                   'f(rauj)in', 'f(rauj)ins', 'f(rauj)a', 'f(rauj)an', 'f(rauja)n', 
                   'g(u)þ', 'g(u)þ(i)s', 'g(u)þa', 'g(u)þblostreis', 
                   'x(ristu)s', 'x(rist)u', 'x(rist)aus']

    #Composti occasionali
    if "~" in word_text:
        parola_o_punto_o_numero_segmento = "segmento"
        testo_segmentato = ""
        segmento = word_text.split("~")
        for s in segmento:
            testo_segmentato = testo_segmentato + "<w rend='{}'>".format(inchiostro) + s + "</w>"
        word_text = testo_segmentato
    
    #Numerali
    if "[num.:" in word_text:
        parola_o_punto_o_numero_segmento = "numero"
        word_text = word_text[len("[num.:"):-1]
        
    #Ricerca delle parentesi quadre '[]' come segnali di metadati e ostituzione delle stringhe di metadati con stringhe TEI-compliant
    while "[" in word_text:

        #Legature
        if "[leg.:" in word_text:
            sub_metadato = re.findall(r'\[leg\.:.*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            #Correzione se presenti metadati nidificati
            while len([c for c in sub_metadato if c=='[']) > len([c for c in sub_metadato if c==']']):
                da_considerare = seguente_metadato.split("]")[0] + "]"
                seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                sub_metadato = sub_metadato + da_considerare

            sub_metadato = sub_metadato[len("[leg.:"):-1]
            metadato = "<g ref='#{}lig'/>".format(sub_metadato)
            word_text = precedente_metadato + metadato + seguente_metadato

        #Lacuna data da rottura della carta, senza congettura proposta
        elif "[†]" in word_text:
            sub_metadato = re.findall(r'\[†\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            metadato = "<gap unit='char' extent='undefined'/>"
            word_text = precedente_metadato + metadato + seguente_metadato
        
        #Lacuna data da rottura della carta, con congettura proposta
        elif "[†;" in word_text:
            sub_metadato = re.findall(r'\[†;e\..*?;r\..*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            #Correzione se presenti metadati nidificati
            while len([c for c in sub_metadato if c=='[']) > len([c for c in sub_metadato if c==']']):
                da_considerare = seguente_metadato.split("]")[0] + "]"
                seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                sub_metadato = sub_metadato + da_considerare

            sub_metadato = sub_metadato[len("[†;"):-1]
            testo_emendato = sub_metadato.split(";")[0][len("e."):]         #Si assume che il testo emendato sia puro testo
            responsabili = sub_metadato.split(";")[1][len("r."):]         #Si assume che il testo emendato sia puro testo
            responsabili = re.sub(r'<.*?>', '', responsabili)
            metadato = "<gap unit='char' extent='{}'/><supplied resp='{}' xml:id='{}'>".format(len(testo_emendato), responsabili, xml_id_data.format('em')) + testo_emendato + "</supplied>"
            word_text = precedente_metadato + metadato + seguente_metadato

        #Aggiunta nell'interlinea o in fine rigo
        elif "[add.:" in word_text:
            print(word_text)
            sub_metadato = re.findall(r'\[add\.:.*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            #Correzione se presenti metadati nidificati
            while len([c for c in sub_metadato if c=='[']) > len([c for c in sub_metadato if c==']']):
                da_considerare = seguente_metadato.split("]")[0] + "]"
                seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                sub_metadato = sub_metadato + da_considerare

            sub_metadato = sub_metadato[len("[add.:"):-1]
            attributo_metadato = __conversione_posizione__(sub_metadato.split(";")[0][len("p."):])
            testo_metadato = ';'.join(sub_metadato.split(";")[1:])
            lista_metadati = []
            for w in testo_metadato.split("_"):
                sub_text_metadato = __evolve_word_str__(w, n_token, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)[0]
                lista_metadati.append(sub_text_metadato)
            metadato = "<add place='{}' xml:id='{}'>".format(attributo_metadato, xml_id_data.format('add'))
            for stm in lista_metadati:
                metadato = metadato + stm
            metadato = metadato + "</add>"
            word_text = precedente_metadato + metadato + seguente_metadato
        
        #Rasura
        elif "[r.:" in word_text:
            sub_metadato = re.findall(r'\[r\.:.*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            #Correzione se presenti metadati nidificati
            while len([c for c in sub_metadato if c=='[']) > len([c for c in sub_metadato if c==']']):
                da_considerare = seguente_metadato.split("]")[0] + "]"
                seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                sub_metadato = sub_metadato + da_considerare
            
            sub_metadato = sub_metadato[len("[r.:"):-1]
            lista_metadati = []
            for w in sub_metadato.split("_"):
                sub_text_metadato = __evolve_word_str__(w, n_token, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)[0]
                lista_metadati.append(sub_text_metadato)
            metadato = "<del rend='erasure' xml:id='{}'>".format(xml_id_data.format('del'))
            for stm in lista_metadati:
                metadato = metadato + stm
            metadato = metadato + "</del>"
            word_text = precedente_metadato + metadato + seguente_metadato
                
        #Lettere di modulo minore
        elif "[small:" in word_text:
            sub_metadato = re.findall(r'\[small:.*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            #Correzione se presenti metadati nidificati
            while len([c for c in sub_metadato if c=='[']) > len([c for c in sub_metadato if c==']']):
                da_considerare = seguente_metadato.split("]")[0] + "]"
                seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                sub_metadato = sub_metadato + da_considerare
            
            sub_metadato = sub_metadato[len("[small:"):-1]
            testo_metadato = __evolve_word_str__(sub_metadato, n_token, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)[0]
            metadato = "<hi rend='small' xml:id='{}'>".format(xml_id_data.format('small')) + testo_metadato + "</hi>"
            word_text = precedente_metadato + metadato + seguente_metadato
        
        #Correzioni
        elif "[corr.:" in word_text:
            sub_metadato = re.findall(r'\[corr\.:.*?;.*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            #Correzione se presenti metadati nidificati
            while len([c for c in sub_metadato if c=='[']) > len([c for c in sub_metadato if c==']']):
                da_considerare = seguente_metadato.split("]")[0] + "]"
                seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                sub_metadato = sub_metadato + da_considerare   

            sub_metadato = sub_metadato[len("[corr.:"):-1]
            sub_metadati_nidificati = re.findall(r'\[.*?\]', sub_metadato)
            for smn in sub_metadati_nidificati:
                metadato_nidificato = __evolve_word_str__(smn, n_token, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)[0]
                sm = ""
                for e in sub_metadato.split(smn):
                    sm = sm + e + metadato_nidificato
                sub_metadato = sm[:-len(metadato_nidificato)]

            pre_correzione = sub_metadato.split(";")[0]
            post_correzione = sub_metadato.split(";")[1]
            metadato = "<subst xml:id='{}'><del rend='erasure'>".format(xml_id_data.format('corr')) + pre_correzione + "</del><add rend='overwritten'>" + post_correzione + "</add></subst>"
            word_text = precedente_metadato + metadato + seguente_metadato

        #Emendazioni
        elif "[em.:" in word_text:
            print(word_text)
            sub_metadato = re.findall(r'\[em\.:c\..*?;e\..*?;r\..*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            sub_metadato = sub_metadato[len("[em.:"):-1]
            testo_codice = sub_metadato.split(';e.')[0][len('c.'):]
            testo_codice = __evolve_word_str__(testo_codice, n_token, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)[0]
            testo_emendato = re.findall(r';e\..*?;r\.', sub_metadato)[0][len(';e.'):-len(';r.')]
            responsabili = sub_metadato.split(';r.')[1]
            metadato = "<choice xml:id='{}'><sic>".format(xml_id_data.format('em')) + testo_codice + "</sic><corr resp='{}'>".format(responsabili) + testo_emendato + "</corr></choice>"
            word_text = precedente_metadato + metadato + seguente_metadato

        #Luogo poco leggibile
        elif "[un.:" in word_text:
            sub_metadato = re.findall(r'\[un\.:.*?\]', word_text)[0]
            precedente_metadato = word_text.split(sub_metadato)[0]
            seguente_metadato = word_text[len(precedente_metadato+sub_metadato):]
            
            #Correzione se presenti metadati nidificati
            while len([c for c in sub_metadato if c=='[']) > len([c for c in sub_metadato if c==']']):
                da_considerare = seguente_metadato.split("]")[0] + "]"
                seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                sub_metadato = sub_metadato + da_considerare  

            sub_metadato = sub_metadato[len("[un.:"):-1]
            testo_metadato = __evolve_word_str__(sub_metadato, n_token, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)[0]
            metadato = "<unclear reason='damage' xml:id='{}'>".format(xml_id_data.format('un')) + testo_metadato + "</unclear>"
            word_text = precedente_metadato + metadato + seguente_metadato

    #Parola spezzata fra righi
    metadato = re.sub(r'<sic.*?<\/sic>', '', word_text)
    metadato = re.sub(r'<del.*?<\/del>', '', metadato)
    metadato = re.sub(r'<.*?>', '', metadato)
    if "-" in metadato:
        parola_spezzata_fra_righi = True
        word_text = re.sub('-', '', word_text)


    #Abbreviazioni
    while "(" in word_text:
        pure_word_text = re.sub(r'<sic.*?<\/sic>', '', word_text)
        pure_word_text = re.sub(r'<del.*?<\/del>', '', pure_word_text)
        pure_word_text = re.sub(r'<.*?>', '', pure_word_text)    
        for t in tachigrafie:
            if t == pure_word_text:
                tachi = re.sub(r'[\(\)]', '', word_text)
                ref_tachi = re.sub(r'[\(\)]', '', pure_word_text)
                metadato = "<choice xml:id='{}'><abbr><am><g ref='#{}tachi'/></am></abbr><expan><ex>{}</ex></expan></choice>".format(xml_id_data.format('abbr'), ref_tachi, tachi)
                word_text = metadato
        if "(" in word_text:
            entro_parentesi = re.findall(r'\(.*?\)', word_text)
            fuori_parentesi = re.split(r'\(.*?\)', word_text)
            pure_fuori_parentesi = re.split(r'\(.*?\)', pure_word_text)
            metadato = "<choice xml:id='{}'><abbr>".format(xml_id_data.format('abbr'))
            for n, fuori in enumerate(fuori_parentesi[:-1]):
                if entro_parentesi[n][1:-1] == 'm':
                    if fuori != '':
                        if fuori_parentesi[n][-1] == '>':
                            true_letter = fuori.split(re.findall(r'<.*?>', fuori)[-1])[0][-1]
                            true_fuori = fuori.split(re.findall(r'<.*?>', fuori)[-1])[0][:-1] + re.findall(r'<.*?>', fuori)[-1]
                            metadato = metadato + true_fuori + "<am><g ref='#{}macr'/></am>".format(true_letter)
                        else:
                            metadato = metadato + fuori[:-1] + "<am><g ref='#{}macr'/></am>".format(pure_fuori_parentesi[n][-1])
                    else:
                        metadato = metadato + "<am><g ref='#{}macr'/></am>".format(pure_fuori_parentesi[n+1][0])
                elif entro_parentesi[n][1:-1] == 'n':
                    if fuori != '':
                        if fuori_parentesi[n][-1] == '>':
                            true_letter = fuori.split(re.findall(r'<.*?>', fuori)[-1])[0][-1]
                            true_fuori = fuori.split(re.findall(r'<.*?>', fuori)[-1])[0][:-1] + re.findall(r'<.*?>', fuori)[-1]
                            metadato = metadato + true_fuori + "<am><g ref='#{}tild'/></am>".format(true_letter)
                        else:
                            metadato = metadato + fuori[:-1] + "<am><g ref='#{}tild'/></am>".format(pure_fuori_parentesi[n][-1])
                    else:
                        metadato = metadato + "<am><g ref='#{}tild'/></am>".format(pure_fuori_parentesi[n+1][0])
                else:
                    if fuori != '':
                        if fuori_parentesi[n][-1] == '>':
                            true_letter = fuori.split(re.findall(r'<.*?>', fuori)[-1])[0][-1]
                            true_fuori = fuori.split(re.findall(r'<.*?>', fuori)[-1])[0][:-1] + re.findall(r'<.*?>', fuori)[-1]
                            metadato = metadato + true_fuori + "<am><g ref='#{}over'/></am>".format(true_letter)
                        else:
                            metadato = metadato + fuori[:-1] + "<am><g ref='#{}over{}'/></am>".format(entro_parentesi[n][1:-1], pure_fuori_parentesi[n][-1])
                    else:
                        metadato = metadato + "<am><g ref='#{}over{}'/></am>".format(entro_parentesi[n][1:-1], pure_fuori_parentesi[n+1][0])
        
            metadato = metadato + fuori_parentesi[-1] + "</abbr><expan>"
            for n, entro in enumerate(entro_parentesi):
                metadato = metadato + fuori_parentesi[n] + "<ex>{}</ex>".format(entro[1:-1])
            metadato = metadato + fuori_parentesi[-1] + "</expan></choice>"
            word_text = metadato

    #Punteggiatura
    metadato = re.sub(r'<sic.*?<\/sic>', '', word_text)
    metadato = re.sub(r'<del.*?<\/del>', '', metadato)
    metadato = re.sub(r'<.*?>', '', metadato)
    if metadato in ['˒', '›' , '·', ':', '→', '¶']:
        parola_o_punto_o_numero_segmento = "punto"

    risultati = [word_text, parola_o_punto_o_numero_segmento, parola_spezzata_fra_righi]

    return risultati
