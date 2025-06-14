ALPHABET = "abcdefghijklmnopqrstuvwxyz "

def bm_search(text, pattern):
    '''
    Mencari *pattern* dalam *text* dengan algoritma Boyer-Moore

    Args:
        text (str): Teks
        pattern (str): Kata kunci yang ingin dicari pada teks
    '''
    length_word = len(text)
    length_pattern = len(pattern)
    occur = 0

    b = get_last_occur_table(pattern)
    if(length_word < length_pattern):
        raise ValueError("Pencarian tidak bisa dilakukan karena pola lebih panjang daripada kata")
    
    i = 0
    j = length_pattern - 1
    while i <= length_word - length_pattern:
        if pattern[j].lower() == text[i+j].lower():
            if j == 0:
                occur += 1
                i += length_pattern
                j = length_pattern - 1
            else:
                j -= 1
        else:
            if b.get(text[i+j], -1) == -1:
                i += j + 1
                j = length_pattern - 1
            elif b.get(text[i+j], -1) < j:
                i += j - b.get(text[i+j], -1)
                j = length_pattern - 1
            else:
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
    txt = u"""sous chef work experience sous chef jul 2010 company name ï¼\u200b city , state assisted cooks in the preparation of green salads, fruit salads and pasta salads. worked the sautã© and fry stations. plated and distributed completed dishes to waiters. improved the accuracy of filled orders by changing the procedure of sharing tickets. took inventory and placed orders, assisted in the food and beverage operations. front desk agent company name ï¼\u200b city , state assisted the property coordinator with daily tasks and worked on hotel computer programming systems worked with hr department to control staffing and perform employee performance evaluations. handled property functions on daily basis to ensure best performance and persistent upgrading in customer service, employee proficiency, performance, marketing, property ambience and income. handled room reservation adjusted auditing reports received and send telephone messages and facsimiles. front desk manager jan 2013 to jan 2014 company name ï¼\u200b city , state process guest registration including calculation and collection of payment conduct night audit as assigned processed all financial transactions including the verification and processing of credit card transactions in accordance with company policies and procedures and complete shift reports maintain room status inventory respond to guest inquires and request regarding hotel services, reservations, local attractions, directions, etc. efficient in several software systems pbx and opera perform work duties in accordance with safety and security policies and procedures guest service recovery- night audit ihg rewards gold level rewards champion kept track of all enrollments for reward members maintained excellence according to ihgs standards for monthly enrollments completed several ihg rewards compliance training seminars. baquet- front desk jan 2010 to jan 2013 company name ï¼\u200b city , state assisted with administration work, contracts, contract changes, certificates. prepared access cards, ordered products. selected the right candidates for the companys needs. became familiar with various laws such as ada, fmla, and workers compensation. front desk agent jan 2011 to jan 2012 company name ï¼\u200b city , state accomplished appointment scheduling, data entry and revenue management, met sales goals. interact with customers on a daily basis via face to face or multi-line phone prep cook (banquet upheld department of health policies by maintaining a sanitary and pleasant dining environment prepared meals to customer satisfaction and performed inventory management. shift supervisor host jun 2007 to dec 2007 company name ï¼\u200b city , state in charge of all hosts hostesses during my time as shift supervisor, responsible for the front of the house. checked time sheets to ensure employees were clocking out properly, trained new employees on pos system. perform work duties in accordance with regulations such as osha, hazcom, and blood borne illnesses. career overview a highly- motivated, productive and customer-focused team player with strong communication, interpersonal, organizational, time management, analytical and problem solving skills. reliable and dedicated with the ability to grasp and apply new procedures quickly; organize and prioritize tasks to meet deadlines and adapt readily to new challenges. core strengths promoting hotel facilities customer service hospitality supervising resolving guest disputes project management marketing experienced in multiple reservation systems strong influencing  communication skills. in-depth knowledge of the hotel, hospitality, leisure and service sector. able to identify, understand and give priority to urgent issues. working long hours, under pressure and tight deadlines. accounting revenue management accomplishments hilton garden inn opening team member woodbridge, virginia educational background masters , business administration 2015 stratford university ï¼\u200b city , state gpa: gpa: 3.8 magna cum lade business administration gpa: 3.8 magna cum lade bachelors of arts , hospitality management 2013 stratford university ï¼\u200b city , state , usa hospitality management associate of applied science , advanced culinary arts 2010 stratford ï¼\u200b city , state , usa advanced culinary arts (c.c.) certifications and trainings city , state tips certified cpr-aed certified certified food handler, state of virginia food management professional, state of virginia ihg training onq training certified culinarian 2010 skills ada compliance, auditing, computer programming, contracts, cpr, credit, customer satisfaction, customer service, data entry, department of health, financial, hr, inventory management, cost accounting, marketing, access, pbx, policies, pos, safety, sales, scheduling, seminars, staffing, supervisor,"""
    print(bm_search(txt, "skills"))
