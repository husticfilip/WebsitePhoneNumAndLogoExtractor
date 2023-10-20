import re

MIN_DIGITS = 6
MAX_DIGITS = 11


def cleanText(text):
    removedlines = re.sub(r'-', " ", text)
    return re.sub(r'[^\+0-9\s\(\)]', r'', removedlines)

def replaceAllNonDigitsPlusesAndParenthesis(text):
    return re.sub(r'[^\+0-9\s\(\)]', " ", text)

def getPhoneNumers(text):
    #cleaned_list = re.findall(r'[\+0-9].+?(?=(?:\s\s|\s$|$))', text)
    # nalazi sve brojeve koji imaju i ( ) - \s i cijeli string je dugacak od 5-17 TODO razmisli o vrijednostima
    #cleaned_list = re.findall(r'[+\d][\d\(\)\-\s]{5,17}(?=[^\d])', text)
    cleaned_list = re.findall(r'.{1}[+\d][\d\(\)\-\s]{5,17}(?=[^\d]).{1}', text)

    filtered = filterWrongCharacterAtBegginigOrEnd(cleaned_list)

    numbers_set = set()
    for candidate in cleaned_list:
        if candidate.startswith("+"):
            pass

        if not candidate in numbers_set:
            num_of_digits = sum(c.isdigit() for c in candidate)
            if num_of_digits >= MIN_DIGITS and num_of_digits <= MAX_DIGITS:
                numbers_set.add(candidate)
    return numbers_set

def filterWrongCharacterAtBegginigOrEnd(candidates):
    passed_candidates = []

    for candidate in candidates:

        # pocetak treba biti pored praznog polja ili pocetka > html zagrade ili pak ako je broj na samom pocetku reda onda pocetak moze biti i + ili broj
        if candidate[0] == " " or candidate[0] == ">" or candidate[0] == "+" or candidate[0].isnumeric():
            # kraj treba biti pored praznog polja ili kraja < html zagrade ili ako je na samom kraju reda moze biti i broj
            if candidate[-1] == " " or candidate[-1] == "<" or candidate[-1].isnumeric():
                passed_candidates.append(candidate)

    return passed_candidates









