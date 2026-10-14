#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

from __assegnatore_nome_libro_biblico__ import __assegnatore_nome_libro_biblico__
from __conversione_posizione__ import __conversione_posizione__
from __evolve_word_str__ import __evolve_word_str__
from __goth_number_converter__ import __goth_number_converter__


# --- FUNZIONE PER CONVERTIRE TRASCRIZIONI DEI TESTIMONI DA .DOCX A TEI XML ---
# --- (funziona relatamente al sistema di trascrizione da me adottato) ---
    
def evolve_goth(file_txt, name_wit):
    """
    Converte il markdown di una trascrizione del progetto PRIN in markup TEI compliant.
    
    :param file_txt: Percorso del file di input (.txt)
    :param name_wit: Nome del testimone trascritto
    """
    
    import re
    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    #Importazione del contenuto della trascrizione in Word
    trascrizione = open(file_txt, encoding='UTF8').read()
    
    #Divisione del testo trascritto in righi
    righi_trascrizione = trascrizione.splitlines()
    
    #Lista degli escape_chars
    lista_escape = ['<', '>', '&', '"', "'"]
    lista_escaped = ['&lt', '&gt','&amp','&quot', '&apos']
    
    #Variabili da indicare previamente
    file_TEI = ""
    TEI_xml = ""

    #Entità corrispondenti a categorie di dati o metadati per la ricodifica
    libro_biblico = ""
    capitolo = ""
    versetto = ""
    n_foglio = ""
    n_ordinal_foglio = 0
    n_rigo_per_foglio = 0
    inchiostro_base = input("Indicare il tipo di inchiostro più frequente:\n")
    inchiostro = inchiostro_base
    lingua = ""
    parola_spezzata_fra_righi = False
    corresp1 = ""
    ID_testimone = name_wit    
    
    #Dizionario dei contenuti degli elementi parola-punto-segmento-numero e relativo identificatore univoco, da inserirsi poi in ogni file .txt finale
    contenuti = {}

    #Inizio della lettura e ricodifica della trascrizione
    for n_rigo, f_rigo_trascr in enumerate(righi_trascrizione):
        print(f_rigo_trascr)
        if f_rigo_trascr != "":                         #verifica che il rigo non sia uno spazio vuoto a separare intestazione o pié di pagina
            while f_rigo_trascr[0] == ' ':
                f_rigo_trascr = f_rigo_trascr[1:]
            while f_rigo_trascr[-1] == ' ':
                f_rigo_trascr = f_rigo_trascr[:-1]

            #Elaborazione del sottoelemento 'libro biblico'
            if "{lib.:" in f_rigo_trascr:
                
                if libro_biblico != "":
                    #Salvataggio del file per il libro precedente - txt in cui inserire i valori del dizionario
                    xmlstr = minidom.parseString(ET.tostring(TEI_xml, encoding='UTF-8')).toprettyxml(indent="   ")
                    with open("v2_{}_{}_TEI_predict.txt".format(name_wit, libro_biblico), 'w', encoding='UTF-8') as f:
                        f.write(xmlstr)
                    
                    #Salvataggio del file per il libro precedente - xml finale
                    file_TEI = open("v2_{}_{}_TEI.xml".format(name_wit, libro_biblico), 'w', encoding='UTF-8')
                    file_txt_xml = open("v2_{}_{}_TEI_predict.txt".format(name_wit, libro_biblico), 'r', encoding='UTF-8').read()
                    for voce in contenuti:
                        file_txt_xml = re.sub(voce, contenuti[voce], file_txt_xml)
                    print(file_txt_xml, file=file_TEI, flush=True)

                    #Reset delle variabili
                    capitolo = ""
                    versetto = ""
                    inchiostro = inchiostro_base
                
                #Creazione degli elementi principali del file TEI
                TEI_xml = ET.Element('TEI')
                TEI_xml.attrib['xmlns'] = "http://www.tei-c.org/ns/1.0"
                teiHeader = ET.SubElement(TEI_xml, 'teiHeader')
                facsimile = ET.SubElement(TEI_xml, 'facsimile')
                text = ET.SubElement(TEI_xml, 'text')
                text.attrib['n'] = name_wit
                body = ET.SubElement(text, 'body')

                #Identificazione del metadato relativo al libro biblico
                libro_token = re.findall(r'\{lib.*?\}', f_rigo_trascr)[0][len("{lib.:"):-1]        
                if libro_biblico != libro_token:
                    libro_biblico = libro_token

                    facsimile.attrib['xml:id'] = '{}_facs_{}'.format(ID_testimone, libro_biblico)
                    
                    libro = ET.SubElement(body, 'div')
                    libro.attrib['type'] = "book"
                    libro.attrib['ana'] = __assegnatore_nome_libro_biblico__(libro_token, n_rigo)
                    libro.attrib['xml:id'] = "{}_book_{}".format(ID_testimone, libro_biblico)

                    #Eliminazione dei riferimenti al libro biblico
                    f_rigo_trascr = re.sub(r'\{lib.*?\}', '', f_rigo_trascr)                           
            
            #Elaborazione del primo sottolemento 'capitolo' e del primo sottoelemento 'versetto'
            if capitolo == "":
                cap_vers_token = re.findall(r'\[c\..*?v\..*?\]', f_rigo_trascr)[0]        #identificazione del metadato contenuto nel rigo
                capitolo_token = int(cap_vers_token.split(",")[0][len("[c."):])     #identificazione del metadato capitolo
                versetto_token = int(cap_vers_token.split(",")[1][len("v."):-1])     #identificazione del metadato capitolo
                capitolo = capitolo_token
                versetto = versetto_token
                
                cap = ET.SubElement(libro, 'div')
                cap.attrib['type'] = "chapter"
                cap.attrib['n'] = str(capitolo)
                cap.attrib['xml:id'] = "{}_{}_chapter_{}".format(ID_testimone, libro_biblico, str(capitolo))

                ver = ET.SubElement(cap, 'ab')
                ver.attrib['type'] = "verse"
                ver.attrib['n'] = str(versetto)
                ver.attrib['xml:id'] = "{}_{}_{}_verse_{}".format(ID_testimone, libro_biblico, capitolo, versetto)

                #Eliminazione dei riferimenti a capitolo e versetto
                f_rigo_trascr = re.sub(r'\[c\..*?v\..*?\]', '', f_rigo_trascr)      

            #Elaborazione dell'elemento foglio
            if "{f." in f_rigo_trascr:
                n_ordinal_foglio = n_ordinal_foglio+1
                n_rigo_per_foglio = 0
                foglio = ET.SubElement(ver, 'pb')
                n_foglio = re.findall(r'\{f\..*?\}', f_rigo_trascr)[0][len("{f."):-1]       #identificazione del metadato contenuto nel rigo
                check_foglio = [c for c in n_foglio]
                for n, c in enumerate(check_foglio):
                    if c in lista_escape:
                        c = lista_escaped[lista_escape.index(c)]
                n_foglio = ""
                for c in check_foglio:
                    n_foglio = n_foglio + c
                foglio.attrib['n'] = n_foglio
                foglio.attrib['xml:id'] = "{}_pb_{}_{}".format(ID_testimone, n_ordinal_foglio, n_foglio)
                foglio.attrib['facs'] = '#{}_facs_{}_{}'.format(ID_testimone, n_ordinal_foglio, n_foglio)

                #Creazione del riferimento nel teiHeader al facsimile corrispondente
                surface = ET.SubElement(facsimile, 'surface')
                surface.attrib['xml:id'] = '{}_facs_{}_{}'.format(ID_testimone, n_ordinal_foglio, n_foglio)
                graphic = ET.SubElement(surface, 'graphic')
                graphic.attrib['url'] = '{}_fol._{}_{}.jpeg'.format(ID_testimone, n_ordinal_foglio, n_foglio)
                graphic.attrib['height'] = '1800px'
                graphic.attrib['width'] = '1200px'

                #Eliminazione del riferimento al foglio
                f_rigo_trascr = re.sub(r'\{f\..*?\}', '', f_rigo_trascr)
            
            #Elaborazione dell'elemento mano del copista
            if "{hand:" in f_rigo_trascr:
                metadati_mano = re.findall(r'\{hand:.*?\}', f_rigo_trascr)[0][len("{hand:"):-1]
                mano = ET.SubElement(ver, 'handNote')
                mano.attrib['scribe'] = "hand {}".format(metadati_mano.split(';')[0])
                mano.attrib['script'] = "type {}".format(metadati_mano.split(';')[1][len('t.'):])

                #Eliminazione del riferimento alla mano
                f_rigo_trascr = re.sub(r'\{hand:.*?\}', '', f_rigo_trascr)
            
            #Elaborazione del sottoelemento titolo corrente
            if n_rigo+1 < len(righi_trascrizione) and righi_trascrizione[n_rigo+1] == "" and n_rigo_per_foglio == 0:
                intestazione = ET.SubElement(ver, 'fw')
                intestazione.attrib['type'] = 'header'
                intestazione.attrib['place'] = 'top_center'
                intestazione.attrib['rend'] = 'silver_ink'
                intestazione.attrib['xml:id'] = '{}_fw_{}_head'.format(ID_testimone, n_foglio)
            
                intestazione.text = f_rigo_trascr
                f_rigo_trascr = ''
            
            #Elaborazione del sottoelemento pié di pagina
            if righi_trascrizione[n_rigo-1] == "" and n_rigo_per_foglio != 0 and "[can.eus." in f_rigo_trascr:
                pie_pagina = ET.SubElement(ver, 'fw')
                pie_pagina.attrib['type'] = "footer"
                pie_pagina.attrib['place'] = "bottom_center"
                pie_pagina.attrib['xml:id'] = "{}_fw_{}_foot".format(ID_testimone, n_foglio)
                tavola = ET.SubElement(pie_pagina, 'table')
                tavola.attrib['type'] = "eusebian_canons"
                tavola.attrib['xml:id'] = "{}_{}_tb".format(ID_testimone, n_foglio)
                canoni = re.findall(r'\[can\.eus.*?;.*?;.*?;.*?\]', f_rigo_trascr)[0]
                precedente_metadato = f_rigo_trascr.split(canoni)[0]
                seguente_metadato = f_rigo_trascr[len(precedente_metadato+canoni):]
                
                #Correzione se presenti metadati nidificati
                while len([c for c in canoni if c=='[']) > len([c for c in canoni if c==']']):
                    da_considerare = seguente_metadato.split("]")[0] + "]"
                    seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                    canoni = canoni + da_considerare
                
                can = canoni[len("[can.eus.:_"):-1].split('_;_')

                lista_canoni = []
                rows = 1
                lista_libri = []

                for canone_singolo in can:
                    c_s = canone_singolo.split('_')
                    c_s = [e for e in c_s if e != '']
                    lista_canoni.append(c_s)
                    rows = len(c_s) if len(c_s) > rows else rows

                for n in range(rows):
                    row = ET.SubElement(tavola, 'row')
                    row.attrib['xml:id'] = "{}_{}_tb_row_{}".format(ID_testimone, n_foglio, n+1)
                    row.attrib['n'] = str(n+1)
                    if n == 0:
                        for c_s in lista_canoni:
                            c_s_libro = ET.SubElement(row, 'w')
                            c_s_nome_libro = __assegnatore_nome_libro_biblico__(c_s[0], n_rigo)
                            lista_libri.append(c_s_nome_libro)
                            c_s_libro.attrib['xml:id'] = "{}_{}_tb_ana_{}".format(ID_testimone, n_foglio, c_s_nome_libro)
                            c_s_libro.attrib['ana'] = c_s_nome_libro
                            c_s_libro.attrib['rend'] = "gold_ink"
                            c_s_libro.text = c_s[0]
                            
                    else:
                        for n_c_s, c_s in enumerate(lista_canoni):
                            if n < len(c_s):
                                c_s_numero = ET.SubElement(row, 'num')
                                c_s_numero.attrib['rend'] = "silver_ink"
                                c_s_n = __evolve_word_str__(c_s[n], n+1, ID_testimone, n_foglio, 'ec', inchiostro)[0]
                                if c_s_n == c_s[n]:
                                    numero_gotico = c_s[n]
                                    testo_numero = c_s[n]                     
                                else:
                                    c_s[n] = re.sub(r'<.*?>', '', c_s_n)
                                    numero_gotico = c_s[n]
                                    testo_numero = c_s_n                               
                                if numero_gotico in ["·", "?"]:
                                    c_s_numero.attrib['value'] = numero_gotico
                                else:
                                    c_s_numero.attrib['value'] = str(__goth_number_converter__(numero_gotico))
                                                            
                                riferimento_univoco = "RIF_ID:{}_{}_tb_{}_{}".format(ID_testimone, n_foglio, lista_libri[n_c_s], n)
                                c_s_numero_w = ET.SubElement(c_s_numero, 'w')
                                c_s_numero_w.attrib['xml:id'] = "{}_{}_tb_{}_{}".format(ID_testimone, n_foglio, lista_libri[n_c_s], n)
                                c_s_numero_w.text = riferimento_univoco
                                contenuti[riferimento_univoco] = testo_numero

                #Eliminazione del riferimento ai canoni eusebiani
                pre = f_rigo_trascr.split(canoni)[0]
                post = f_rigo_trascr.split(canoni)[1]
                f_rigo_trascr = pre+post

            #Elaborazione del numero di fascicolo
            if "[fasc.:" in f_rigo_trascr:
                fasc = re.findall(r'\[fasc\.:.*?\]', f_rigo_trascr)[0]
                precedente_metadato = f_rigo_trascr.split(fasc)[0]
                seguente_metadato = f_rigo_trascr[len(precedente_metadato+fasc):]
                
                #Correzione se presenti metadati nidificati
                while len([c for c in fasc if c=='[']) > len([c for c in fasc if c==']']):
                    da_considerare = seguente_metadato.split("]")[0] + "]"
                    seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                    fasc = fasc + da_considerare

                fasc_p = fasc[len("[fasc.:"):-1].split(';')[0][len('p.'):]
                fasc_n = fasc[len("[fasc.:"):-1].split(';')[1]
                f_n = __evolve_word_str__(fasc_n, 0, ID_testimone, n_foglio, 'fa', inchiostro)[0]
                if f_n == fasc_n:
                    numero_gotico = fasc_n
                    testo_numero = fasc_n                         
                else:
                    fasc_n = re.sub(r'<.*?>', '', f_n)
                    numero_gotico = fasc_n
                    testo_numero = f_n
                fasc_n_arabo = __goth_number_converter__(numero_gotico)
                riferimento_univoco = "RIF_ID:{}_{}_gb_{}".format(ID_testimone, n_foglio, fasc_n_arabo)
                
                fascicolo = ET.SubElement(ver, 'gb')
                fascicolo.attrib['n'] = str(fasc_n_arabo)
                fasc_indicazione = ET.SubElement(ver, 'add')
                fasc_indicazione.attrib['type'] = "quire"
                fasc_indicazione.attrib['place'] = __conversione_posizione__(fasc_p)
                fasc_indicazione.attrib['rend'] = "silver_ink"
                fasc_indicazione.attrib['value'] = str(fasc_n_arabo)
                fasc_indicazione.attrib['xml:id'] = "{}_{}_gb_{}".format(ID_testimone, n_foglio, fasc_n_arabo)                
                fasc_indicazione.text = riferimento_univoco

                contenuti[riferimento_univoco] = testo_numero

                #Eliminazione dei riferimenti al numero di fascicolo
                pre = f_rigo_trascr.split(fasc)[0]
                post = f_rigo_trascr.split(fasc)[1]
                f_rigo_trascr = pre+post
            
            #Divisione del rigo in token, spezzando la stringa ad ogni spazio
            if f_rigo_trascr == " ":
                f_rigo_trascr = ""
            rigo_trascr = f_rigo_trascr.split(' ')

            #Elaborazione del rigo di testo
            if len(rigo_trascr) > 1:
                n_rigo_per_foglio = n_rigo_per_foglio+1
                 
                rigo = ET.SubElement(ver, 'lb')
                rigo.attrib['n'] = str(n_rigo_per_foglio)
                rigo.attrib['xml:id'] = "{}_lb_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio)
                
                for n_token, token in enumerate(rigo_trascr):
                    
                    #Elaborazione del cambio di capitolo o versetto
                    if "[c." in token:
                        cap_vers_token = re.findall(r'\[c\..*?v\..*?\]', token)[0]

                        #Identificazione dei metadati di capitolo e versetto
                        capitolo_token = int(cap_vers_token.split(",")[0][len("[c."):])
                        versetto_token = int(cap_vers_token.split(",")[1][len("v."):-1])
                        if capitolo != capitolo_token:
                            cap = ET.SubElement(libro, 'div')
                            cap.attrib['type'] = "chapter"
                            cap.attrib['n'] = str(capitolo_token)
                            cap.attrib['xml:id'] = "{}_{}_chapter_{}".format(ID_testimone, libro_biblico, str(capitolo_token))
                            capitolo = capitolo_token
                        if versetto != versetto_token:
                            ver = ET.SubElement(cap, 'ab')
                            ver.attrib['type'] = "verse"
                            ver.attrib['n'] = str(versetto_token)
                            ver.attrib['xml:id'] = "{}_{}_{}_verse_{}".format(ID_testimone, libro_biblico, str(capitolo_token), versetto_token)
                            versetto = versetto_token
                        
                        #Eliminazione dei riferimenti a capitolo e versetto
                        token = re.sub(r'\[c\..*?v\..*?\]', '', token)

                    #Elaborazione dell'elemento lingua
                    if "{lan.:" in token:
                        lingua = re.findall(r'\{lan\.:.*?\}', token)[0][len("{lan.:"):-1]
                        token = re.sub(r'\{lan\.:.*?\}', '', token)
                    
                    #Elaborazione delle sezioni ammoniane-eusebiane
                    if "[sez.amm.:" in token:

                        #Estrazione della posizione e del numerale gotico
                        sezione = re.findall(r'\[sez\.amm\..*?\]', token)[0]
                        precedente_metadato = token.split(sezione)[0]
                        seguente_metadato = token[len(precedente_metadato+sezione):]
                        
                        #Correzione se presenti metadati nidificati
                        while len([c for c in sezione if c=='[']) > len([c for c in sezione if c==']']):
                            da_considerare = seguente_metadato.split("]")[0] + "]"
                            seguente_metadato = seguente_metadato[len(seguente_metadato.split("]")[0] + "]"):]
                            sezione = sezione + da_considerare
                        
                        #Distinzione di posizione e numerale
                        
                        sez = sezione[len("[sez.amm.:"):-1].split(';')      
                        posizione_sezione = sez[0][len("p.:"):]
                        posizione_sezione = __conversione_posizione__(posizione_sezione)
                        numerale_sezione = sez[1]
                        n_sez = __evolve_word_str__(numerale_sezione, n_token+1, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)[0]
                        if n_sez == numerale_sezione:
                            numero_gotico = numerale_sezione
                            testo_numero = numerale_sezione                         
                        else:
                            numerale_sezione = re.sub(r'<.*?>', '', n_sez)
                            numero_gotico = numerale_sezione
                            testo_numero = n_sez
                        numerale_arabo_sezione = __goth_number_converter__(numero_gotico)

                        #Elaborazione dell'elemento TEI
                        sez_ammoniana = ET.SubElement(ver, 'label')
                        sez_ammoniana.attrib['type'] = "eusebian_section"
                        sez_ammoniana.attrib['ana'] = libro_biblico
                        sez_ammoniana.attrib['place'] = posizione_sezione
                        sez_ammoniana.attrib['rend'] = 'silver_ink'
                        sez_ammoniana.attrib['xml:id'] = "{}_eusebian_section_{}_{}_{}_{}".format(ID_testimone, libro_biblico, numerale_arabo_sezione, n_foglio, n_rigo_per_foglio)
                        sez_ammoniana_numero = ET.SubElement(sez_ammoniana, 'num')
                        sez_ammoniana_numero.attrib['value'] = str(numerale_arabo_sezione)
                    
                        riferimento_univoco = "RIF_ID:{}_eusebian_section_{}_{}_{}_{}".format(ID_testimone, libro_biblico, numerale_arabo_sezione, n_foglio, n_rigo_per_foglio)
                        sez_ammoniana_numero.text = riferimento_univoco
                        
                        contenuti[riferimento_univoco] = testo_numero
                        
                        #Eliminazione dei riferimenti alla sezione ammoniana nel token
                        pre = token.split(sezione)[0]
                        post = token.split(sezione)[1]
                        token = pre+post

                    #Elaborazione delle aggiunte in margine
                    if "[marg.:" in token:
                        #Estrazione della posizione e del testo a margine
                        agg_a_margine = re.findall(r'\[marg\..*?\]', token)[0][len("[marg.:"):-1]
                        
                        #Distinzione di posizione e testo a margine      
                        agg_a_margine = agg_a_margine.split(';')
                        posizione_marginalia = agg_a_margine[0][len("p.:"):]
                        posizione_marginalia = __conversione_posizione__(posizione_marginalia)
                        testo_marginalia = agg_a_margine[1].split(' ')
                        
                        #Elaborazione dell'elemento TEI
                        marginalia = ET.SubElement(ver, 'add')
                        marginalia.attrib['type'] = "marginalia"
                        marginalia.attrib['place'] = posizione_marginalia
                        marginalia.attrib['xml:id'] = "{}_marginalia_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio)
                        marginalia.text = testo_marginalia
                        
                        #Eliminazione dei riferimenti all'aggiunta in margine nel token
                        token = re.sub(r'\[marg.\..*?\]', '', token)      
                    
                    #Elaborazione dell'eventuale cambio di inchiostro
                    if "{s.i.}" in token:
                        inchiostro = "silver_ink"
                        token = re.sub('{s.i.}', '', token)
                    if "{g.i.}" in token:
                        inchiostro = "gold_ink"
                        token = re.sub('{g.i.}', '', token)
                    if "{gs.i.}" in token:
                        inchiostro = "gold_and_silver_ink"
                        token = re.sub('{gs.i.}', '', token)

                    #Elaborazione riferimenti all'Antico Testamento
                    if "[AT:" in token:
                        rif_AT_text = re.findall(r'\[AT:.*?\]', token)[0][len("[AT:"):-1]
                        rif_AT = ET.SubElement(ver, 'ref')
                        rif_AT.attrib['type'] = 'Old_Testament_reference'
                        rif_AT.attrib['corresp'] = rif_AT_text
                        rif_AT.attrib['xml:id'] = "{}_AT_ref_{}_{}".format(ID_testimone, capitolo, versetto)

                        #Eliminazione dei riferimenti all'aggiunta in margine nel token
                        token = re.sub(r'\[AT:.*?\]', '', token)     

                    if "[fAT]" in token:
                        rif_AT = ET.SubElement(ver, 'ref')
                        rif_AT.attrib['type'] = 'Old_Testament_reference'
                        rif_AT.attrib['corresp'] = rif_AT_text
                        rif_AT.attrib['xml:id'] = "{}_AT_ref_end_{}_{}".format(ID_testimone, capitolo, versetto)

                        #Eliminazione dei riferimenti all'aggiunta in margine nel token
                        token = re.sub(r'\[fAT\]', '', token)  

                    #Elaborazione delle spaziature
                    if "[space]" in token:
                        
                        spaziatura = ET.SubElement(ver, 'space')
                        spaziatura.attrib['xml:id'] = '{}_space_{}_{}_{}'.format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                        spaziatura.attrib['dim'] = 'horizontal'

                        token = re.sub(r'\[space\]', '', token)

                    #Elaborazione dei singoli termini
                    if len(token) > 0:      #verifica che il token contenga ancora testo
                        parola_spezzata_fra_righi = False
                        word_results = __evolve_word_str__(token, n_token+1, ID_testimone, n_foglio, n_rigo_per_foglio, inchiostro)
                        
                        word_text = word_results[0]
                        tipo_word = word_results[1]
                        parola_spezzata_fra_righi = word_results[2]

                        #Numerale
                        if tipo_word == "numero":
                            numero = ET.SubElement(ver, 'num')
                            numero.attrib['rend'] = inchiostro
                            metadato = re.sub(r'<sic.*?<\/sic>', '', word_text)
                            metadato = re.sub(r'<del.*?<\/del>', '', metadato)
                            metadato = re.sub(r'<.*?>', '', metadato)
                            numerale_arabo = __goth_number_converter__(metadato)
                            numero.attrib['value'] = str(numerale_arabo)
                            w_numero = ET.SubElement(numero, 'w')
                            w_numero.attrib['xml:id'] = "{}_w_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                            riferimento_univoco = "RIF_ID:{}_num_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                            
                            if parola_spezzata_fra_righi == True:
                                seg_w_numero = ET.SubElement(w_numero, 'seg')
                                corresp1 = '{}_seg_1_{}_{}_{}'.format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                riferimento_seg_precedente = "RIF_ID:{}_seg_1_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                seg_w_numero.attrib['corresp'] = riferimento_seg_precedente
                                seg_w_numero.text = riferimento_univoco

                            elif parola_spezzata_fra_righi == False and corresp1 != "":
                                seg_w_numero = ET.SubElement(w_numero, 'seg')
                                w_numero.attrib['corresp'] = corresp1
                                contenuti[riferimento_seg_precedente] = '{}_seg_2_{}_{}_{}'.format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                corresp1 = ""
                                riferimento_seg_precedente = ""
                                seg_w_numero.text = riferimento_univoco

                            else:
                                w_numero.text = riferimento_univoco

                            contenuti[riferimento_univoco] = word_text
                            
                        #Punteggiatura
                        if tipo_word == "punto":

                            riferimento_univoco = "RIF_ID:{}_pc_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                            
                            punto = ET.SubElement(ver, 'pc')
                            metadato = re.sub(r'<sic.*?<\/sic>', '', word_text)
                            metadato = re.sub(r'<del.*?<\/del>', '', metadato)
                            metadato = re.sub(r'<.*?>', '', metadato)
                            
                            if metadato == '˒':
                                punto.attrib['type'] = "quick_diple"
                                punto.attrib['rend'] = inchiostro
                                punto.attrib['place'] = "margin_left"
                                punto.attrib['xml:id'] = "{}_q_diple_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                punto.text = riferimento_univoco

                            elif metadato == '›':
                                punto.attrib['type'] = "full_diple"
                                punto.attrib['rend'] = inchiostro
                                punto.attrib['place'] = "margin_left"
                                punto.attrib['xml:id'] = "{}_f_diple_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                punto.text = riferimento_univoco
                                
                            elif metadato == '→':
                                punto.attrib['type'] = "obelo_diple"
                                punto.attrib['rend'] = inchiostro
                                punto.attrib['place'] = "margin_left"
                                punto.attrib['xml:id'] = "{}_o_diple_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                punto.text = riferimento_univoco

                            elif metadato == '¶':
                                punto.attrib['type'] = "paraph"
                                punto.attrib['rend'] = inchiostro
                                punto.attrib['xml:id'] = "{}_paraph_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                punto.text = riferimento_univoco
                        
                            elif metadato == '·':
                                punto.attrib['type'] = "comma"
                                punto.attrib['rend'] = inchiostro
                                punto.attrib['xml:id'] = "{}_comma_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                punto.text = riferimento_univoco

                            else:
                                punto.attrib['type'] = "colon"
                                punto.attrib['rend'] = inchiostro
                                punto.attrib['xml:id'] = "{}_colon_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                punto.text = riferimento_univoco
                            
                            contenuti[riferimento_univoco] = word_text
                                
                            
                        #Parola semplice
                        if tipo_word == "parola":
                            parola = ET.SubElement(ver, 'w')
                            parola.attrib['rend'] = inchiostro
                            parola.attrib['xml:lang'] = lingua
                            parola.attrib['xml:id'] = "{}_w_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                            riferimento_univoco = "RIF_ID:{}_w_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)

                            if parola_spezzata_fra_righi == True:
                                seg_parola = ET.SubElement(parola, 'seg')
                                corresp1 = '{}_seg_1_{}_{}_{}'.format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                riferimento_seg_precedente = "RIF_ID:{}_seg_1_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                seg_parola.attrib['corresp'] = riferimento_seg_precedente
                                seg_parola.text = riferimento_univoco

                            elif parola_spezzata_fra_righi == False and corresp1 != "":
                                seg_parola = ET.SubElement(parola, 'seg')
                                seg_parola.attrib['corresp'] = corresp1
                                contenuti[riferimento_seg_precedente] = '{}_seg_2_{}_{}_{}'.format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                corresp1 = ""
                                riferimento_seg_precedente = ""
                                seg_parola.text = riferimento_univoco

                            else:
                                parola.text = riferimento_univoco

                            contenuti[riferimento_univoco] = word_text


                        #Composto occasionale
                        if tipo_word == "segmento":
                            parola = ET.SubElement(ver, 'w')
                            parola.attrib['rend'] = inchiostro
                            parola.attrib['xml:lang'] = lingua
                            segmento = ET.SubElement(parola, 'seg')
                            segmento.attrib['type'] = 'composite-word'
                            segmento.attrib['xml:id'] = "{}_seg_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                            riferimento_univoco = "RIF_ID:{}_seg_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                            
                            if parola_spezzata_fra_righi == True:
                                seg_segmento = ET.SubElement(segmento, 'seg')
                                corresp1 = '{}_seg_1_{}_{}_{}'.format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                riferimento_seg_precedente = "RIF_ID:{}_seg_1_{}_{}_{}".format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                seg_segmento.attrib['corresp'] = riferimento_seg_precedente
                                seg_segmento.text = riferimento_univoco

                            elif parola_spezzata_fra_righi == False and corresp1 != "":
                                seg_segmento = ET.SubElement(segmento, 'seg')
                                seg_segmento.attrib['corresp'] = corresp1
                                contenuti[riferimento_seg_precedente] = '{}_seg_2_{}_{}_{}'.format(ID_testimone, n_foglio, n_rigo_per_foglio, n_token+1)
                                corresp1 = ""
                                riferimento_seg_precedente = ""
                                seg_segmento.text = riferimento_univoco

                            else:
                                segmento.text = riferimento_univoco
                            
                            contenuti[riferimento_univoco] = word_text

                    print('parola {} fatta!'.format(n_token+1))

    #Salvataggio del file per il libro precedente - txt in cui inserire i valori del dizionario
    xmlstr = minidom.parseString(ET.tostring(TEI_xml, encoding='UTF-8')).toprettyxml(indent="   ")
    with open("v2_{}_{}_TEI_predict.txt".format(name_wit, libro_biblico), 'w', encoding='UTF-8') as f:
        f.write(xmlstr)

    #Salvataggio del file per il libro precedente - xml finale
    file_TEI = open("v2_{}_{}_TEI.xml".format(name_wit, libro_biblico), 'w', encoding='UTF-8')
    file_txt_xml = open("v2_{}_{}_TEI_predict.txt".format(name_wit, libro_biblico), 'r', encoding='UTF-8').read()
    for voce in contenuti:
        file_txt_xml = re.sub(voce, contenuti[voce], file_txt_xml)
    print(file_txt_xml, file=file_TEI, flush=True)
    print(f"Documento elaborato")
