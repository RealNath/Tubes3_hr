ALPHABET = "abcdefghijklmnopqrstuvwxyz "

def bm_search(word, pattern):
    length_word = len(word)
    length_pattern = len(pattern)
    occur = 0

    b = get_last_occur_table(pattern)
    if(length_word < length_pattern):
        raise ValueError("Pencarian tidak bisa dilakukan karena pola lebih panjang daripada kata")
    
    i = 0
    j = length_pattern - 1
    while i <= length_word - length_pattern:
        if pattern[j].lower() == word[i+j].lower():
            if j == 0:
                occur += 1
                i += length_pattern
                j = length_pattern - 1
            else:
                j -= 1
        elif b.get(word[i+j]) == -1:
            i += j + 1
            j = length_pattern - 1
        elif b.get(word[i+j]) < j:
            i += j - b.get(word[i+j])
            j = length_pattern - 1
        elif b.get(word[i+j]) > j:
            i += 1
            j = length_pattern - 1

    return occur

def get_last_occur_table(pattern):
    table_dict = {}
    for letter in ALPHABET:
        table_dict[letter] = -1
        for i in range(len(pattern) - 1, -1, -1):
            if(letter.lower() == pattern[i].lower()):
                table_dict[letter] = i
                break
        
        
    return table_dict


def kmp_search(word, pattern):
    length_word = len(word)
    length_pat = len(pattern)
    occur = 0

    b = get_lps_table(pattern)
    if(length_word < length_pat):
        raise ValueError("Pencarian tidak bisa dilakukan karena pola lebih panjang daripada kata")

    i = 0
    j = 0
    while i <= length_word - length_pat:
        if pattern[j].lower() == word[i+j].lower():
            if j == length_pat-1:
                occur += 1
                i += length_pat
                j = 0
            else:
                j += 1
        elif j > 0:
            i += j - b[j - 1]
            j = b[j-1]
        else:
            i += 1

    return occur

def get_lps_table(pattern):
    length = len(pattern)
    i = 1
    last_id = 0 #(i - 1) max length
    lps_table = [0]*(length - 1)

    while i < length - 1:
        if pattern[i].lower() == pattern[last_id].lower():
            last_id += 1
            lps_table[i] = last_id
            i += 1
        
        else:
            if last_id != 0:
                last_id = lps_table[last_id - 1]
            else:
                lps_table[i] = 0
                i += 1

    return lps_table

def calc_levenshtein_dist(s1, s2):
    m, n = len(s1), len(s2)

    dp = [[0]*(n+1) for _ in range(m+1)]

    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(m + 1):
        dp[i][0] = i
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1,
                    dp[i][j-1] + 1,
                    dp[i-1][j-1] + 1 
                )
        
    return dp[m][n]
