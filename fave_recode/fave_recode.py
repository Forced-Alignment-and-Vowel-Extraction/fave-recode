from aligned_textgrid.aligned_textgrid import AlignedTextGrid
from aligned_textgrid.sequences.word_and_phone import Word, Phone


def cmu2plotnik(phone):
    VOWELS =['AA0', 'AA1', 'AA2',
             'AE0', 'AE1', 'AE2',
             'AH0', 'AH1', 'AH2', 
             'AO0', 'AO1', 'AO2', 
             'AW0', 'AW1', 'AW2', 
             'AY0', 'AY1', 'AY2', 
             'EH0', 'EH1', 'EH2', 
             'ER0', 'ER1', 'ER2', 
             'EY0', 'EY1', 'EY2', 
             'IH0', 'IH1', 'IH2', 
             'IY0', 'IY1', 'IY2', 
             'OW0', 'OW1', 'OW2', 
             'OY0', 'OY1', 'OY2', 
             'UH0', 'UH1', 'UH2', 
             'UW0', 'UW1', 'UW2']
    
    CONSONANTS = ['B', 'CH', 'D', 
                  'DH', 'F', 'G', 
                  'HH', 'JH', 'K', 
                  'L', 'M', 'N', 'NG', 
                  'P', 'R', 'S', 
                  'SH', 'T', 'TH', 
                  'V', 'W', 'Y', 
                  'Z', 'ZH']
    ALL_PHONE = VOWELS + CONSONANTS + ["#"]
    
    DEFAULT = {
    'AA': 'o', 
    'AE': 'ae', 
    'AH': 'uh', 
    'AO': 'oh', 
    'AW': 'aw', 
    'AY': 'ay', 
    'EH': 'e', 
    'ER': '*hr', 
    'EY': 'ey', 
    'IH': 'i', 
    'IY': 'iy', 
    'OW': 'ow', 
    'OY': 'oy', 
    'UH': 'u', 
    'UW': 'uw'
    }
    
    if phone.label not in VOWELS:
        return phone.label
    if phone.label == "AH0":
        return "@" 
    if (phone.fol.label not in ALL_PHONE) or (phone.prev.label not in ALL_PHONE):
        return DEFAULT[phone.label[0:-1]]
    if phone.label in ["IY0", "IY1", "IY2"] and phone.fol.label == "#":
        return "iyF"
    if phone.label in ["EY0", "EY1", "EY2"] and phone.fol.label == "#":
        return "eyF"
    if phone.label in ["OW0", "OW1", "OW2"] and phone.fol.label == "#":
        return "owF"
    if phone.label in ["AY0", "AY1", "AY2"] and phone.fol.label in ['CH', 'F', 'HH', 'K',  'P', 'S', 'SH', 'T', 'TH']:
        return "ay0"