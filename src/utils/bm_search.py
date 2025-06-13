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


if __name__ == '__main__':
    print(bm_search("I love math and mathematics", "matg"))
