#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# AI-assistance disclosure
# This script was developed with the assistance of Claude (Anthropic),
# a large language model. The code was reviewed, tested and adapted by the
# author, who takes full responsibility for its content.
# ---------------------------------------------------------------------------

"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

"""
Script per aggiungere <note type="corresp-text"> agli elementi <seg> con @corresp
"""
def add_corresp_notes(input_file, output_file):
    import re
    
    # Leggi il file XML
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # STEP 1: Crea mappa xml:id → testo
    seg_map = {}
    for match in re.finditer(r'<seg[^>]*xml:id="([^"]+)"[^>]*>(.*?)</seg>', content, re.DOTALL):
        seg_id = match.group(1)
        seg_text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        seg_map[seg_id] = seg_text
        print(f"Trovato seg: {seg_id} = '{seg_text}'")
    
    print(f"\nTotale seg trovati: {len(seg_map)}\n")
    
    # STEP 2: Trova e sostituisci tutti i seg con @corresp
    for match in re.finditer(r'<seg[^>]*corresp="([^"]+)"[^>]*>(.*?)</seg>', content, re.DOTALL):
        corresp_id = match.group(1)
        original_seg = match.group(0)
        
        if corresp_id in seg_map:
            note = f'<note type="corresp-text">{seg_map[corresp_id]}</note>'
            new_seg = original_seg.replace('</seg>', f'{note}</seg>')
            content = content.replace(original_seg, new_seg, 1)
            print(f"Aggiunto note a seg con corresp={corresp_id}: '{seg_map[corresp_id]}'")
        else:
            print(f"⚠️ Corresp non trovato: {corresp_id}")
    
    # Scrivi il file di output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ File salvato: {output_file}")
