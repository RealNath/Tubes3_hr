import re

def extract_education(text):
    """
    Extract education sections from resume text using regex patterns.

    Args:
        text (str): The resume text to search
        
    Returns:
        dict: { major: str, school: str, year: int }

    """
    
    # Education section headers
    education_headers = [
        r'Education',
        r'Education\s+and\s+Training',
        r'Educational\s+Background',
        r'Academic\s+Background',
        r'Academic\s+Qualifications',
        r'Academic\s+Experience',
        r'Degrees?',
        r'Training'
    ]
    
    # Major resume sections (to know where education section ends)
    major_sections = [
        r'Experience',
        r'Work\s+History',
        r'Professional\s+Experience',
        r'Relevant\s+Experience',
        r'Employment',
        r'Skills?',
        r'Technical\s+Skills?',
        r'Computer\s+Skills?',
        r'Professional\s+Skills?',
        r'Competencies',
        r'Expertise',
        r'Abilities',
        r'Qualifications',
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
        r'Career',
        r'Objective',
        r'Contact',
        r'Accomplishments'
    ]
    
    # Regex pattern
    education_pattern = '|'.join(education_headers)
    section_pattern = '|'.join(major_sections)
    
    pattern = fr'''
        (?:^|\n)                                               # Start of line
        ((?:{education_pattern})\s*:?\s*)                      # Education header (group 1)
        (?:\n|$)                                               # Newline or end of string
        ((?:(?!^(?:{section_pattern})\s*:?\s*$).*(?:\n|$))*)   # Content until next major section (group 2)
    '''
    
    # Find all matches
    matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.VERBOSE))
    
    if not matches:
        return None
    
    # Parse
    education_content = matches[0].group(2).strip()
    
    return _parse_education(education_content)

def _parse_education(education_content):
    """
    Parse the education content to extract relevant details.

    Args:
        education_content (str): The education section content

    Returns:
        dict: { major: str, school: str, year: int }
    """
    if not education_content:
        return {}

    # Initialize the result dictionary
    result = {
        "major": None,
        "school": None,
        "year": None
    }

    # Extract degree, major
    degree_pattern = r'''
        (Bachelor|Master|Doctorate|PhD|Associate|MBA|MS|BS|BA|MA|MSc|BSc|MSW|JD|MD|DDS|PharmD|EdD)  # Degree types
        \s+                                                                                          # Whitespace
        (?:of|:|\s+in)?                                                                              # Optional connector
        \s*                                                                                          # Optional whitespace
        ([A-Za-z\s]+)                                                                                # Major/field
        (?=\s*[\n,\-]|\s*[0-9]*|\s{2,}[A-Z][a-z]+|$)                                               # Stop conditions
    '''
    
    # School pattern (* University of *)
    school_pattern = r'''
        (?:^|[\n,\-\s]+)                                          # Start or separator
        (?:at\s+|from\s+|,\s*|\n\s*|[0-9]*)?                      # Optional preposition
        (                                                         # Capture group for school name
            (?:[A-Z][a-zA-Z\s&\-'\.]+\s+)?                        # Optional prefix (e.g., "State", "California")
            (?:University|College|Institute|School|Academy)       # Institution type
            (?:\s+of\s+)                                          # "of" connector
            (?:[A-Za-z\s&\-'\.]+)                                 # Location/Name
            (?=\s*[\n,\-]|\s*[0-9]*|\s{2,}[A-Z][a-z]+|$)          # Stop conditions
            |                                                     # OR
            (?:[A-Z][a-zA-Z\s&\-'\.]+\s+)?                        # Name prefix
            (?:University|College|Institute|School|Academy)       # Institution type
        )
        (?=\s*[\n,\-]|\s*[0-9]*|\s{2,}[A-Z][a-z]+|$)              # Followed by separator or end
    '''

    # Year pattern
    year_pattern = r'''
        (?:\b(?:\d{4})\b)  # 4-digit year
    '''

    degree_match = re.search(degree_pattern, education_content, re.IGNORECASE | re.VERBOSE)
    school_match = re.search(school_pattern, education_content, re.IGNORECASE | re.VERBOSE)
    year_match = re.search(year_pattern, education_content, re.IGNORECASE | re.VERBOSE)

    if degree_match:
        result["major"] = degree_match.group(2).strip()

        if result['major'].endswith(' City'):
            result['major'] = result['major'][:-len(' City')].strip()

    if school_match:
        result["school"] = school_match.group(1).strip()
        if result["school"].endswith('  City'):
            result["school"] = result["school"][:-len('  City')].strip()

    if year_match:
        result["year"] = int(year_match.group(0).strip())

    return result