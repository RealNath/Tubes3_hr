import re

def extract_skills(text):
    """
    Extract skills sections from resume text using regex patterns.

    Args:
        text (str): The resume text to search
        
    Returns:
        list: Skill list
    """
    
    # Skills section headers
    skills_headers = [
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
    
    # Major resume sections (to know where skills section ends)
    major_sections = [
        r'Experience',
        r'Education',
        r'Work\s+History',
        r'Professional\s+Experience',
        r'Relevant\s+Experience',
        r'Employment',
        r'Training',
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
        r'Contact'
    ]
    
    # Regex pattern
    skills_pattern = '|'.join(skills_headers)
    section_pattern = '|'.join(major_sections)
    
    pattern = fr'''
        (?:^|\n)                                               # Start of line
        ((?:{skills_pattern})\s*:?\s*)                         # Skills header (group 1)
        (?:\n|$)                                               # Newline or end of string
        ((?:(?!^(?:{section_pattern})\s*:?\s*$).*(?:\n|$))*)   # Content until next major section (group 2)
    '''
    
    # Find all matches
    matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.VERBOSE))
    
    if not matches:
        return None
    
    results = []
    
    for match in matches:
        content = match.group(2).strip()

        # Clean and format the content
        skills_list = _process_skills(content)

        if skills_list:
            results.extend(skills_list)
    
    # Remove duplicates but preserve order
    unique_results = list(dict.fromkeys(results))
    return unique_results


def _process_skills(content):
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
    
    skills = []
    
    # Check if lines already have bullet points
    has_bullets = any(re.match(r'^[\s•\-\*▪○►]+', line) for line in lines)
    
    if has_bullets:
        for line in lines:
            # Remove bullet points and extract skill
            skill = re.sub(r'^[\s•\-\*▪○►]+', '', line).strip()
            if skill:
                # Check if this is a categorical skill
                if ':' in skill:
                    category, items = skill.split(':', 1)
                    category = category.strip()
                    items = items.strip()
                    
                    # Parse items after the colon
                    item_skills = []
                    for item in re.split(r'[,;|]', items):
                        item = item.strip().rstrip('.')
                        if item and 2 <= len(item) <= 100:
                            item_skills.append(item)
                            skills.append(f"{category}: {item}")
                else:
                    skills.append(skill)
    else:
        for line in lines:
            # Check if this is a categorical skill (contains colon)
            if ':' in line:
                category, items = line.split(':', 1)
                category = category.strip()
                items = items.strip()
                
                # Parse the items after the colon
                item_skills = []
                for item in re.split(r'[,;|]', items):
                    item = item.strip().rstrip('.')
                    if item and 2 <= len(item) <= 100:
                        item_skills.append(item)
                        skills.append(f"{category}: {item}")
            else:
                # Join all non-categorical lines and check for separators
                all_text = line
                separators = [',', ';', '|', '•', '▪', '○', '►', '-', '*']
                
                # Count separators and find the most common one
                separator_counts = {}
                for sep in separators:
                    separator_counts[sep] = all_text.count(sep)
                
                # Find most frequent separator
                best_separator = max(separator_counts, key=separator_counts.get)
                best_count = separator_counts[best_separator]
                word_count = len(all_text.split())
                
                # If has many separators, treat as separated list
                if best_count >= 3 and word_count > 0 and (best_count / word_count) > 0.08:
                    for part in all_text.split(best_separator):
                        skill = part.strip()
                        # Clean up common connectors
                        skill = re.sub(r'^(and\s+|&\s+)', '', skill, flags=re.IGNORECASE)
                        skill = re.sub(r'\s+(and|&)\s*$', '', skill, flags=re.IGNORECASE)
                        skill = re.sub(r'\s+', ' ', skill)  # Normalize whitespace
                        skill = skill.rstrip('.')  # Remove trailing periods
                        
                        # Sanity length check
                        if skill and 2 <= len(skill) <= 30:
                            skills.append(skill)
                else:
                    # Treat the line as a single skill
                    skill = line.strip()
                    if skill and 2 <= len(skill) <= 30:
                        skills.append(skill)
    
    return skills