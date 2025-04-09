def read_db_properties(filename):
    props = {}
    with open(filename, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                props[key.strip()] = value.strip()
    return props