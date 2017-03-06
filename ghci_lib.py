def filter_ghci_line(line):
    for pref in ['Ok', 'Failed']:
        full_pref = pref + ", modules loaded: "
        if line.startswith(full_pref):
            rest = line[len(full_pref):]
            n = 1 + rest.count(',')
            return ('%s, %d modules loaded.\n' % (pref, n))
    return line
