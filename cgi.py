# Temporary patch for removed cgi module in Python 3.13
def parse_header(line):
    parts = line.split(';')
    key = parts[0].strip().lower()
    pdict = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1)
            pdict[k.strip().lower()] = v.strip().strip('"')
    return key, pdict
