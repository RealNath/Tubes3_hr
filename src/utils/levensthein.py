def levenshtein_distance(str1, str2):
    """
    Menghitung Levenshtein *distance* antara string `text` dan `pattern`
    """
    str_len_1 = len(str1)
    str_len_2 = len(str2)
    if str_len_1 == 0: return str_len_2
    if str_len_2 == 0: return str_len_1

    # === Tabel DP ===
        # Inisialisasi
    dp = [[0] * (str_len_2 + 1) for _ in range(str_len_1 + 1)]
    for i in range(str_len_1 + 1): dp[i][0] = i
    for j in range(str_len_2 + 1): dp[0][j] = j

        # Isi tabel
    for i in range(1, str_len_1 + 1):
        for j in range(1, str_len_2 + 1):
            if str1[i-1] == str2[j-1]: cost = 0
            else: cost = 1
            dp[i][j] = min(
                dp[i-1][j] + 1, # hapus karakter
                dp[i][j-1] + 1, # insert karakter
                dp[i-1][j-1] + cost # ganti karakter
            )
    
    return dp[str_len_1][str_len_2]

def similarity_score(str1, str2):
    """
    Skor kemiripan (0.0 sampai 1.0) antara string `text` dan `pattern`.
    """
    distance = levenshtein_distance(str1, str2)
    max_length = max(len(str1), len(str2))
    if max_length == 0: return 1.0
    return 1.0 - distance / max_length

if __name__ == "__main__":
    text_1 = "never gonna run around in desert typhoons"
    text_2 = "never gonna run around with dessert spoons"
    print(f"Teks 1: \"{text_1}\"\nTeks 2: \"{text_2}\"")
    print(f"Distance: {levenshtein_distance(text_1, text_2)}")
    print(f"Similarity: {similarity_score(text_1, text_2):.3f}")