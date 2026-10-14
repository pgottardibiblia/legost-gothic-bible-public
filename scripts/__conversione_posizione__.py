#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

#Script per convertire un abbreviazione di posizione nel suo corrispettivo completo
def __conversione_posizione__(posizione):
    lista_abbreviazioni = ('mr', 'ml', 'tr', 'tc', 'tb', 'br', 'bc', 'bl', 'a', 'b', 'l', 'r')
    lista_posizioni = ('margin_right', 'margin_left', 'top_right', 'top_center', 'top_left', 'bottom_right', 'bottom_center', 'bottom_left', 'above', 'below', 'align_left', 'align_right')

    posizione_estesa = lista_posizioni[lista_abbreviazioni.index(posizione)]

    return posizione_estesa
