#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 08:36:20 2024

@author: pierandrea
"""

# Script per inserire note TEI basate su target line breaks
def insert_notes(notes_file, input_dir='.', output_dir=None):
    """
    Inserisce note TEI prima del line break successivo.
    CORRETTO: Trova <lb> nidificati in qualsiasi elemento.
    """
    
    import xml.etree.ElementTree as ET
    import re
    from pathlib import Path
    from datetime import datetime
    import shutil

    # Leggi file note
    print(f"📖 Lettura note: {notes_file}")
    with open(notes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Estrai note per vangelo
    gospels = {'Matthew': 'Matteo', 'John': 'Giovanni', 'Luke': 'Luca', 'Mark': 'Marco'}
    notes = {}
    
    for english, italian in gospels.items():
        pattern = rf'{italian}\s*\n(.*?)(?=\n(?:Matteo|Giovanni|Luca|Marco)\s*\n|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            section = match.group(1)
            gospel_notes = re.findall(r'(<note[^>]*>.*?</note>)', section, re.DOTALL)
            notes[english] = gospel_notes
            print(f"   {english}: {len(gospel_notes)} note")
        else:
            notes[english] = []
    
    print()
    
    # File mapping
    files = {
        'Matthew': 'v2_CArg_Mt_TEI.xml',
        'John': 'v2_CArg_Gv_TEI.xml',
        'Luke': 'v2_CArg_Lc_TEI.xml',
        'Mark': 'v2_CArg_Mc_TEI.xml'
    }
    
    total_inserted = 0
    xml_ns = "{http://www.w3.org/XML/1998/namespace}"
    
    # Processa ogni vangelo
    for gospel, filename in files.items():
        if not notes.get(gospel):
            continue
        
        xml_path = Path(input_dir) / filename
        
        if not xml_path.exists():
            print(f"⚠️  {filename}: file non trovato")
            continue
        
        print(f"📝 {gospel} ({filename}):")
        
        # Determina output
        if output_dir:
            output_path = Path(output_dir) / filename
            backup_path = Path(output_dir) / f"{xml_path.stem}_original_v2.xml"
            if not backup_path.exists():
                shutil.copy2(xml_path, backup_path)
                print(f"   ✅ Backup: {backup_path.name}")
        else:
            output_path = xml_path
            backup_path = xml_path.with_suffix(f'.backup_v2_{datetime.now():%Y%m%d_%H%M%S}.xml')
            shutil.copy2(xml_path, backup_path)
            print(f"   ✅ Backup: {backup_path.name}")
        
        # Parse XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Namespace
        ns = root.tag.split('}')[0].strip('{') if root.tag.startswith('{') else None
        lb_tag = f"{{{ns}}}lb" if ns else "lb"
        
        # IMPORTANTE: Crea lista di TUTTI gli <lb> in ordine documento
        all_lb_elements = [elem for elem in root.iter(lb_tag)]
        print(f"   📋 Trovati {len(all_lb_elements)} <lb> totali nel documento")
        
        # Organizza note per target
        notes_by_target = {}
        for note_str in notes[gospel]:
            target_match = re.search(r'target="([^"]+)"', note_str)
            if target_match:
                target = target_match.group(1).lstrip('#')
                if target not in notes_by_target:
                    notes_by_target[target] = []
                notes_by_target[target].append(note_str)
        
        print(f"   📋 {len(notes_by_target)} target diversi")
        
        # Inserisci note
        inserted = 0
        for lb_id, note_strings in notes_by_target.items():
            # Trova elemento lb target nella lista completa
            lb_elem = None
            for elem in all_lb_elements:
                if elem.get(f'{xml_ns}id') == lb_id:
                    lb_elem = elem
                    break
            
            if lb_elem is None:
                print(f"   ⚠️  Target non trovato: {lb_id}")
                continue
            
            # Trova il parent del lb target
            parent = None
            for p in root.iter():
                if lb_elem in list(p):
                    parent = p
                    break
            
            if parent is None:
                print(f"   ⚠️  Parent non trovato per: {lb_id}")
                continue
            
            # Trova l'INDICE del lb corrente nella lista completa
            try:
                current_lb_index = all_lb_elements.index(lb_elem)
            except ValueError:
                print(f"   ⚠️  Errore indice per: {lb_id}")
                continue
            
            # Trova il PROSSIMO <lb> nella lista completa (ovunque nel documento)
            next_lb_elem = None
            if current_lb_index + 1 < len(all_lb_elements):
                next_lb_elem = all_lb_elements[current_lb_index + 1]
            
            # Determina dove inserire le note
            if next_lb_elem is not None:
                # Trova il parent del prossimo lb
                next_lb_parent = None
                for p in root.iter():
                    if next_lb_elem in list(p):
                        next_lb_parent = p
                        break
                
                if next_lb_parent is not None:
                    # Inserisci PRIMA del prossimo lb nel SUO parent
                    next_lb_index = list(next_lb_parent).index(next_lb_elem)
                    
                    for i, note_str in enumerate(note_strings):
                        try:
                            # Aggiungi namespace
                            if ns:
                                note_str = note_str.replace('<note', f'<note xmlns="{ns}"')
                                note_str = note_str.replace('<hi', f'<hi xmlns="{ns}"')
                            
                            note_elem = ET.fromstring(note_str)
                            next_lb_parent.insert(next_lb_index + i, note_elem)
                            inserted += 1
                            
                        except ET.ParseError as e:
                            print(f"   ❌ Errore parsing nota {lb_id}: {e}")
                            continue
                else:
                    print(f"   ⚠️  Parent del prossimo lb non trovato per {lb_id}")
            else:
                # È l'ultimo lb, inserisci alla fine del parent corrente
                insert_position = len(list(parent))
                
                for i, note_str in enumerate(note_strings):
                    try:
                        if ns:
                            note_str = note_str.replace('<note', f'<note xmlns="{ns}"')
                            note_str = note_str.replace('<hi', f'<hi xmlns="{ns}"')
                        
                        note_elem = ET.fromstring(note_str)
                        parent.insert(insert_position + i, note_elem)
                        inserted += 1
                        
                    except ET.ParseError as e:
                        print(f"   ❌ Errore parsing nota {lb_id}: {e}")
                        continue
        
        print(f"   ✅ Inserite {inserted} note")
        
        # Salva
        if ns:
            ET.register_namespace('', ns)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"   💾 Salvato: {output_path.name}\n")
        
        total_inserted += inserted
    
    return total_inserted
