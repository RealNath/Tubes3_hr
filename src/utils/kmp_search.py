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

if __name__ == '__main__':
    print(get_lps_table("aba"))
    print(kmp_search("abbabbabbabaabb","aba"))