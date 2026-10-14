#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

#Script per convertire i numerali alfabetici del gotico in numeri arabi
def __goth_number_converter__(numero_alfabetico):
    insieme_numeri = numero_alfabetico.split('·')
    lista_numeri_gotici = ('a', 'b', 'g', 'd', 'e', 'q', 'z', 'h', 'þ', 'i', 'k', 'l', 'm', 'n', 'j', 'u', 'p', 'ɥ', 'r', 's', 't', 'w', 'f', 'x', 'ƕ', 'o')
    lista_numeri_arabi = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70 , 80, 90, 100, 200, 300, 400, 500, 600, 700, 800)
    
    insieme_numeri = [num for num in insieme_numeri if num != '']

    numeri_convertiti = ""

    for num in insieme_numeri:
        numero_arabo = 0
        for carattere in num:
            numerale_convertito = lista_numeri_arabi[lista_numeri_gotici.index(carattere)]
            numero_arabo = numero_arabo + numerale_convertito
        numeri_convertiti = numeri_convertiti + str(numero_arabo) + ", "

    numeri_convertiti = numeri_convertiti[:-2]

    return numeri_convertiti
