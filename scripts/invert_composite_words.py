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

#Script per invertire la nidificazione dei composite-word
def invert_composite_words(input_file, output_file=None):
    """
    Inverte la nidificazione di tutti i <seg type="composite-word"> nel file.
    
    Trasformazione:
        <seg type="composite-word" xml:id="CArg_seg_130r_14_1" ...>
            <w>managuþ</w>
            <w>þan</w>
        </seg>
    
    Diventa:
        <w xml:id="CArg_w_130r_14_1" ...>
            <seg type="composite-word" xml:id="CArg_seg_130r_14_1_1" n="1">managuþ</seg>
            <seg type="composite-word" xml:id="CArg_seg_130r_14_1_2" n="2">þan</seg>
        </w>
    
    Args:
        input_file: Path del file XML di input
        output_file: Path del file di output (None = sovrascrive input con backup)
    
    Returns:
        Numero di elementi modificati
    """

    import xml.etree.ElementTree as ET
    from pathlib import Path
    from datetime import datetime
    import shutil

    input_path = Path(input_file)
    
    # Crea backup se sovrascrive
    if output_file is None:
        output_path = input_path
        backup = input_path.with_suffix(f'.backup_{datetime.now():%Y%m%d_%H%M%S}.xml')
        shutil.copy2(input_path, backup)
        print(f"✅ Backup: {backup}")
    else:
        output_path = Path(output_file)
    
    # Parse XML
    tree = ET.parse(input_path)
    root = tree.getroot()
    
    # Estrai namespace TEI se presente
    ns = root.tag.split('}')[0].strip('{') if root.tag.startswith('{') else None
    
    # Trova tutti i <seg type="composite-word">
    xpath = f".//{{{ns}}}seg[@type='composite-word']" if ns else ".//seg[@type='composite-word']"
    composite_words = root.findall(xpath)
    
    print(f"🔍 Trovati {len(composite_words)} composite-word")
    
    num_modified = 0
    xml_ns = "{http://www.w3.org/XML/1998/namespace}"
    
    # Per ogni composite-word
    for seg in composite_words:
        # Trova genitore
        parent = next((elem for elem in root.iter() if seg in list(elem)), None)
        if parent is None:
            continue
        
        # Crea nuovo <w> contenitore
        w_tag = f"{{{ns}}}w" if ns else "w"
        new_w = ET.Element(w_tag)
        
        # Copia attributi del <seg> nel <w> (tranne 'type')
        for attr, value in seg.attrib.items():
            if not attr.endswith('type'):
                if 'id' in attr.lower():
                    value = value.replace('seg', 'w')
                new_w.set(attr, value)
        
        # Trova tutti i <w> figli
        w_children = seg.findall(f'{{{ns}}}w' if ns else 'w')
        
        # Per ogni <w> figlio, crea un <seg> nel nuovo contenitore
        for idx, w_child in enumerate(w_children, start=1):
            seg_tag = f"{{{ns}}}seg" if ns else "seg"
            new_seg = ET.Element(seg_tag)
            
            # Copia attributi del <seg> originale
            for attr, value in seg.attrib.items():
                if 'id' in attr.lower():
                    value = f"{value}_{idx}"
                new_seg.set(attr, value)
            
            # Aggiungi attributo 'n'
            new_seg.set('n', str(idx))
            
            # Copia contenuto e attributi specifici del <w> figlio
            new_seg.text = w_child.text
            for attr, value in w_child.attrib.items():
                if 'id' not in attr.lower():
                    new_seg.set(attr, value)
            
            # Copia eventuali figli
            for child in w_child:
                new_seg.append(child)
            
            # Preserva tail
            if w_child.tail:
                new_seg.tail = w_child.tail
            
            new_w.append(new_seg)
        
        # Sostituisci <seg> con nuovo <w>
        seg_index = list(parent).index(seg)
        new_w.tail = seg.tail
        parent.remove(seg)
        parent.insert(seg_index, new_w)
        
        num_modified += 1
        
        # Log
        old_id = seg.get(f"{xml_ns}id") or seg.get('xml:id') or 'unknown'
        new_id = new_w.get(f"{xml_ns}id") or new_w.get('xml:id') or 'unknown'
        print(f"   {num_modified}. {old_id} → {new_id} ({len(w_children)} parti)")
    
    # Salva
    if ns:
        ET.register_namespace('', ns)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Salvato: {output_path}")
    print(f"✅ Modificati: {num_modified} elementi")
    
    return num_modified
