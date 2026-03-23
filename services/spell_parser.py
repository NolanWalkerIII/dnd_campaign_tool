"""
Spell doc parser — reads Documentation/07_SPELLS_REFERENCE.md and
Documentation/24_EXPANSION_SPELLS.md and returns a unified list of
structured spell dicts.

Called once at import time from game_data.py; result cached as ALL_SPELLS.
"""
import os
import re

_DOC_DIR = os.path.join(os.path.dirname(__file__), '..', 'Documentation')

# Maps source annotation strings (from the *Classes: ...* line) to canonical tags
_SOURCE_PATTERNS = [
    (re.compile(r'\*\(TCoE revision', re.I), 'TCoE'),
    (re.compile(r'\*\(TCoE\)',        re.I), 'TCoE'),
    (re.compile(r'\*\(XGtE\)',        re.I), 'XGtE'),
]

# Level header patterns
_CANTRIP_RE = re.compile(r'^##\s+Cantrips?\s*\(Level\s+0\)', re.I)
_LEVEL_RE   = re.compile(r'^##\s+(\d+)(?:st|nd|rd|th)?\s+Level', re.I)

# First-line entry pattern: **Spell Name** (optional level hint) | rest…
_ENTRY_RE = re.compile(r'^\*\*(.+?)\*\*(?:\s*\((\d+)(?:st|nd|rd|th)\))?\s*\|(.+)')

# Classes line
_CLASSES_RE = re.compile(r'^\*Classes:\s*([^*]+)\*')


def _parse_file(path, default_source):
    spells = []
    current_level = 0
    entry = None  # dict being accumulated

    def _flush(e):
        if e and e.get('name'):
            e['description'] = e['description'].strip()
            spells.append(e)

    with open(path, encoding='utf-8') as fh:
        for raw_line in fh:
            line = raw_line.rstrip('\n')

            # Detect level header
            if _CANTRIP_RE.match(line):
                _flush(entry); entry = None
                current_level = 0
                continue
            m = _LEVEL_RE.match(line)
            if m:
                _flush(entry); entry = None
                current_level = int(m.group(1))
                continue

            # Detect new spell entry
            m = _ENTRY_RE.match(line)
            if m:
                _flush(entry)
                name = m.group(1).strip()
                level_hint = m.group(2)  # present for 6th–9th entries like **Heal** (6th)
                meta = [p.strip() for p in m.group(3).split('|')]
                school       = meta[0] if len(meta) > 0 else ''
                casting_time = meta[1] if len(meta) > 1 else ''
                range_       = meta[2] if len(meta) > 2 else ''
                components   = meta[3] if len(meta) > 3 else ''
                duration     = meta[4] if len(meta) > 4 else ''
                concentration = 'concentration' in duration.lower()
                spell_level = int(level_hint) if level_hint else current_level
                entry = {
                    'name':         name,
                    'level':        spell_level,
                    'school':       school,
                    'casting_time': casting_time,
                    'range':        range_,
                    'components':   components,
                    'duration':     duration,
                    'concentration': concentration,
                    'description':  '',
                    'classes':      [],
                    'source':       default_source,
                }
                continue

            if entry is None:
                continue

            # Detect classes line (ends the entry's description)
            m = _CLASSES_RE.match(line)
            if m:
                raw_classes = m.group(1)
                # Strip source annotations like *(XGtE)* that may trail the classes
                for pattern, tag in _SOURCE_PATTERNS:
                    if pattern.search(line):
                        entry['source'] = tag
                        break
                # Parse class names (comma-separated, before any trailing *)
                classes_part = re.split(r'\*', raw_classes)[0]
                entry['classes'] = [c.strip() for c in classes_part.split(',') if c.strip()]
                _flush(entry)
                entry = None
                continue

            # Accumulate description (skip blank lines between spell and class list)
            text = line.strip()
            if text and not text.startswith('#') and not text.startswith('---'):
                if entry['description']:
                    entry['description'] += ' ' + text
                else:
                    entry['description'] = text

    _flush(entry)
    return spells


def parse_spell_docs():
    """Parse both spell reference docs and return the combined ALL_SPELLS list."""
    core_path = os.path.join(_DOC_DIR, '07_SPELLS_REFERENCE.md')
    exp_path  = os.path.join(_DOC_DIR, '24_EXPANSION_SPELLS.md')

    spells = []
    if os.path.exists(core_path):
        spells.extend(_parse_file(core_path, 'PHB'))
    if os.path.exists(exp_path):
        spells.extend(_parse_file(exp_path, 'XGtE'))  # default; overridden per-entry

    # Deduplicate by name (core takes precedence over expansion for same name)
    seen = {}
    deduped = []
    for s in spells:
        if s['name'] not in seen:
            seen[s['name']] = True
            deduped.append(s)

    return deduped
