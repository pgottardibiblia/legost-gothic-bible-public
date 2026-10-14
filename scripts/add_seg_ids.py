#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

"""
Script per aggiungere xml:id agli elementi <seg> basandosi sul xml:id del <w> padre
"""
def add_seg_ids(input_file, output_file):
    import re
    
 # Leggi il file XML
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Contatori per statistiche
    stats = {'total_segs': 0, 'seg_with_id': 0, 'seg_without_id': 0, 
             'seg_1_added': 0, 'seg_2_added': 0, 'no_match': 0}
    
    print("\n=== PROCESSAMENTO SEG ===\n")
    
    # Pattern per trovare <w> con <seg> figli
    pattern = r'(<w[^>]*xml:id="([^"]+)"[^>]*>\s*)(<seg\s+([^>]*?)(corresp="([^"]+)")([^>]*?)>)(.*?</seg>)'
    
    # Trova tutti i match e sostituisci uno alla volta
    for match in re.finditer(pattern, content):
        stats['total_segs'] += 1
        
        w_opening = match.group(1)
        w_id = match.group(2)
        seg_full_opening = match.group(3)
        seg_attrs_before = match.group(4)
        corresp_full = match.group(5)
        corresp_value = match.group(6)
        seg_attrs_after = match.group(7)
        seg_content = match.group(8)
        original = match.group(0)
        
        # Controlla se xml:id è già presente
        if 'xml:id=' in seg_attrs_before or 'xml:id=' in seg_attrs_after:
            stats['seg_with_id'] += 1
            print(f"  ⏭️  Seg già con xml:id (w={w_id}), skip")
            continue
        
        stats['seg_without_id'] += 1
        
        # Determina il nuovo xml:id basandosi sul corresp
        if '_seg_2_' in corresp_value:
            seg_id = w_id.replace('_w_', '_seg_1_')
            stats['seg_1_added'] += 1
            print(f"  ✅ Aggiunto xml:id={seg_id} (corresp contiene _seg_2_)")
        elif '_seg_1_' in corresp_value:
            seg_id = w_id.replace('_w_', '_seg_2_')
            stats['seg_2_added'] += 1
            print(f"  ✅ Aggiunto xml:id={seg_id} (corresp contiene _seg_1_)")
        else:
            stats['no_match'] += 1
            print(f"  ⚠️  Nessun pattern _seg_X_ in corresp={corresp_value}, skip")
            continue
        
        # Ricostruisci il tag <seg> con xml:id aggiunto
        new_seg_opening = f'<seg {seg_attrs_before}{corresp_full} xml:id="{seg_id}"{seg_attrs_after}>'
        replacement = f'{w_opening}{new_seg_opening}{seg_content}'
        
        # Sostituisci nel contenuto (solo la prima occorrenza per sicurezza)
        content = content.replace(original, replacement, 1)
    
    # Salva il file di output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Stampa statistiche
    print(f"\n=== STATISTICHE ===")
    print(f"Totale <seg> con corresp trovati: {stats['total_segs']}")
    print(f"  - Già con xml:id (skipped): {stats['seg_with_id']}")
    print(f"  - Senza xml:id: {stats['seg_without_id']}")
    print(f"    · _seg_1_ aggiunti: {stats['seg_1_added']}")
    print(f"    · _seg_2_ aggiunti: {stats['seg_2_added']}")
    print(f"    · Nessun pattern (skipped): {stats['no_match']}")
    print(f"\n✅ File salvato: {output_file}")
