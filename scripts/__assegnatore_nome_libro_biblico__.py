#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

    

#Script per produrre i metadati corretti dell'attributo 'n' nell'elemento 'libro'
def __assegnatore_nome_libro_biblico__(libro_biblico, n_rigo):
    abbr = ('Mt', 'Lc', 'Mc', 'Gv', 'Rm', 'Ne')
    euseb_abbr_nom = ('m(a)þ(þaius)', 'luk(as)', 'm(a)r(kus)', 'ïoh(annes)')
    euseb_abbr_acc = ('m(a)þ(þaiu)', 'luk(an)', 'mar(ku)', 'ïoh(annen)')
    n = ('#Matthew', '#Luke', '#Mark', '#John', '#Romans', '#Nehemiah')
    
    while libro_biblico not in abbr and libro_biblico not in euseb_abbr_nom and libro_biblico not in euseb_abbr_acc:
        print("Errore nel libro biblico al rigo {}".format(str(n_rigo)))
        libro_biblico = input("Inserisci l'indicazione corretta del libro biblico:\n")
    
    if libro_biblico in abbr:
        n_per_abbr = n[abbr.index(libro_biblico)]
    
    elif libro_biblico in euseb_abbr_acc:
        n_per_abbr = abbr[euseb_abbr_acc.index(libro_biblico)]

    elif libro_biblico in euseb_abbr_nom:
        n_per_abbr = abbr[euseb_abbr_nom.index(libro_biblico)]

    return n_per_abbr
