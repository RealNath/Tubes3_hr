from src.utils.levensthein import similarity_score
import re

def fuzzy_search(text, pattern, threshold=0.8):
    """
    Fuzzy matching for a pattern in text using Levenshtein distance.

    Args:
        text (str): The text to search in
        pattern (str): The pattern to search for
        threshold (float): Minimum similarity score (0.0 to 1.0) to consider a match
        
    Returns:
        int: Number of fuzzy matches found
    """
    matches = 0

    # Handle multi-word patterns
    if ' ' in pattern:
        pattern_words = pattern.split()
        text_words = text.split()
        
        # Use sliding window for multi-word phrases
        for i in range(len(text_words) - len(pattern_words) + 1):
            window = text_words[i:i + len(pattern_words)]
            # Clean each word in the window
            clean_window = [re.sub(r'[^\w]', '', word.lower()) for word in window]
            window_text = ' '.join(clean_window)

            similarity = similarity_score(window_text, pattern)
            if similarity >= threshold:
                matches += 1
    else:
        # Single word pattern
        words = text.split()
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if len(clean_word) > 0:
                similarity = similarity_score(clean_word, pattern)
                if similarity >= threshold:
                    matches += 1
                    
    return matches