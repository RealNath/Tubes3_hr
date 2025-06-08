def kmp(word, pattern):
    length = len(pattern)
    occur = 0

    b = get_lps_table(pattern)

    return occur

def get_lps_table(pattern):
    length = len(pattern)
    i = 1
    last_id = 0 #i - 1 max length
    b = [0]*(length)

    while i < length:
        if pattern[i] == pattern[last_id]:
            last_id += 1
            b[i] == last_id
            i += 1
        
        else:
            if last_id != 0:
                last_id = b[last_id - 1]
            else:
                b[i] = 0
                i += 1

    return b

if __name__ == '__main__':
    print(get_lps_table("abaaba"))