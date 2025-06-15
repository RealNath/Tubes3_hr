import re

_months = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
_year = r'\d{4}'
# awal atau akhir; bisa <Month YYYY>, <MM/YYYY> atau cuma <YYYY>
_short_date = rf'(?:{_months}\s+{_year}|\d{{1,2}}[\/\-]\d{{1,2}}(?:[\/\-]\d{{2,4}})?|{_year})'
# Simbol range tangal
_range_symbol = r'(?:\s*(?:–|-|to|until)\s*)'
# date-range with named groups
DATE_RANGE = re.compile(
    rf'(?P<start>{_short_date}){_range_symbol}(?P<end>{_short_date}|Present|Current|Now)',
    re.IGNORECASE
)
BULLET_RE = re.compile(r'^\s*[\-\*•▪○►\u2022]\s*')

def extract_experience(text):
    """
    Extract experience/job sections from resume text using regex patterns.

    Args:
        text (str): The resume text to search
        
    Returns:
        List of dictionary {start_date, end_date, title, company, description}
    """
    
    # Skills section headers
    experience_headers = [
        r'Experiences?',
        r'Experiences?\s+(?:Summary|Overview)',
        r'(?:Work|Employment|Career|Professional|Relevant|Jobs?|Occupations?)\s+(?:History|Experiences?|Backgrounds?)',
        r'Works?',
        r'Employments?',
        r'Careers?',
        r'Professions?',
        r'Jobs?',
        r'Occupations?'
    ]
    
    # Major resume sections (to know where skills section ends)
    major_sections = [
        r'Education',
        # r'Employment',
        # r'Training',
        r'Certifications?',
        r'Awards?',
        r'Projects?',
        r'Highlights?',
        r'Interests?',
        r'Personal\s+Information',
        r'Additional\s+Information',
        r'Professional\s+Affiliations?',
        r'Affiliations?',
        r'References?',
        r'About\s+me',
        r'Summary',
        r'Professional\s+Summary',
        # r'Career',
        r'Objective',
        r'Contact',
        r'Skills?',
        r'Skill\s+Highlights?',
        r'Key\s+Skills?',
        r'Technical\s+Skills?',
        r'Computer\s+Skills?',
        r'Professional\s+Skills?',
        r'Competencies',
        r'Expertise',
        r'Abilities',
        r'Qualifications'
    ]
    
    # Regex pattern
    experience_pattern = '|'.join(experience_headers)
    section_pattern = '|'.join(major_sections)
    
    pattern = fr'''
        (?:^|\n)                                               # Start of line
        ((?:{experience_pattern})\s*:?\s*)                         # Skills header (group 1)
        (?:\n|$)                                               # Newline or end of string
        ((?:(?!^(?:{section_pattern})\s*:?\s*$).*(?:\n|$))*)   # Content until next major section (group 2)
    '''
    
    # Find all matches
    matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.VERBOSE))
    
    if not matches:
        return None
    
    results = []
    
    for match in matches:
        block = match.group(2).strip()
        results += _process_experience(block)
    return results

def _process_experience(content):
    """
    Clean extracted skills content.
    
    Args:
        content (str): Raw skills content
        
    Returns:
        list: Skill list
    """
    # Remove whitespace and empty lines
    lines = [line.strip() for line in content.split('\n')]
    lines = [line for line in lines if line and len(line) > 1]
    
    entries = []
    
    for i, line in enumerate(lines):
        m = DATE_RANGE.search(line)
        if not m:
            continue

        # Capture dates
        start = m.group('start').strip()
        end = m.group('end').strip()

        # Pre- and post-date text
        prefix = line[:m.start()].strip(' -–—')
        suffix = line[m.end():].strip(' -–—')

        # Heuristics for title and company
        title, company = prefix, ''
        if suffix:
            company = suffix
        elif ' at ' in prefix.lower():
            parts = re.split(r'\s+at\s+', prefix, flags=re.IGNORECASE)
            title = parts[0].strip()
            company = parts[1].strip() if len(parts) > 1 else ''

        # Collect description until blank line or next date-range
        desc = ""
        for j in range(i+1, len(lines)):
            nl = lines[j]
            if not nl.strip():
                break
            if DATE_RANGE.search(nl):
                break
            # Strip any bullet symbol if present, otherwise take full line
            clean = BULLET_RE.sub('', nl).strip()
            if clean:
                if (desc!=""): desc += " "
                desc += clean

        entries.append({
            'start': start,
            'end': end,
            'title': title,
            'company': company,
            'description': desc,
        })

    return entries