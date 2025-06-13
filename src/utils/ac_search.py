from collections import deque

class Node:
    def __init__(self):
        self.children = {}
        self.output = []
        self.fail = None

def build_trie(patternList):
    root = Node(None)

    # trie
    for pattern in patternList:
        node = root
        for char in pattern:
            node = node.children.setdefault(char, Node())
        node.output.append(pattern)

    # === failure link ===
    queue = deque()
    for node in root.children.values():
        queue.append(node)
        node.fail = root
        
        # bfs
    while queue:
        cur_node = queue.popleft()
        for key, next_node in cur_node.children.items():
            queue.append(next_node)
            fail_node = cur_node.fail
            # lps
            while (fail_node) and (key not in fail_node.children):
                fail_node = fail_node.fail
            if fail_node: next_node.fail = fail_node.children[key]
            else: next_node.fail = root
            next_node.output += next_node.fail.output

    return root

def ac_search(text, patternList):
    '''
    Mencari sekumpulan *pattern* dalam *text* dengan algoritma Aho-Corasick
    
    Args:
        text (str): Teks
        patternList (list): Kumpulan kata kunci yang ingin dicari pada teks
    '''
    root = build_trie(patternList)
    result = {pattern: [] for pattern in patternList}

    cur_node = root
    for i, char in enumerate(text):
        while (cur_node) and (char not in cur_node.children):
            cur_node = cur_node.fail
        
        if not cur_node:
            cur_node = root
            continue

        cur_node = cur_node.children[char]
        for pattern in cur_node.output:
            result[pattern].append(i-len(pattern)+1)
    
    return result