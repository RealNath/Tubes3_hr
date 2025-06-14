def levenshtein_distance(text, pattern):
    """
    Fuzzy matching menggunakan algoritma Levenshtein Distance.
    """
    text_len = len(text)
    pattern_len = len(pattern)
    if text_len == 0: return pattern_len
    if pattern_len == 0: return text_len

    # === Tabel DP ===
        # Inisialisasi
    dp = [[0] * (pattern_len + 1) for _ in range(text_len + 1)]
    for i in range(text_len + 1): dp[i][0] = i
    for j in range(pattern_len + 1): dp[0][j] = j

        # Isi tabel
    for i in range(1, text_len + 1):
        for j in range(1, pattern_len + 1):
            if text[i-1] == pattern[j-1]: cost = 0
            else: cost = 1
            dp[i][j] = min(
                dp[i-1][j] + 1, # hapus karakter
                dp[i][j-1] + 1, # insert karakter
                dp[i-1][j-1] + cost # ganti karakter
            )
    
    return dp[text_len][pattern_len]

def similarity_score(text, pattern):
    """
    Skor kemiripan (0.0 sampai 1.0) antara string str1 dan str2.
    """
    distance = levenshtein_distance(text, pattern)
    max_length = max(len(text), len(pattern))
    if max_length == 0: return 1.0
    return 1.0 - distance / max_length

if __name__ == "__main__":
    a = "oiai oiiai"
    b = "oiiai oiai"
    print(f"str1: \"{a}\"\nstr2: \"{b}\"")
    print(f"Distance: {levenshtein_distance(a, b)}")
    print(f"Similarity: {similarity_score(a, b):.3f}")