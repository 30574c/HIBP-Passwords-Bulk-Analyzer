from hashlib import sha1
from os import stat
import csv

def binary_search(hash, haveibeenpwned_file, file_size, hashes):
    def get_full_line(file, pos):
        file.seek(pos)
        while pos > 0 and file.read(1) != '\n':
            pos -= 1
            file.seek(pos)
        return file.readline(), pos

    def search_hash(file, hash, start, end, hashes):
        if start >= end:
            return 0
        new_pos = start + (end - start) // 2
        candidate_line, pivot = get_full_line(file, new_pos)
        pwned_hash, count = candidate_line.split(':')
        if pwned_hash == hash:
            hashes[hash]['compromised'] = 'true'
            hashes[hash]['count'] = int(count.strip())
        if hash > pwned_hash:
            return search_hash(haveibeenpwned_file, hash, file.tell(), end, hashes)
        else:
            return search_hash(haveibeenpwned_file, hash, start, pivot, hashes)

    return search_hash(haveibeenpwned_file, hash, 0, file_size, hashes)

def save_to_csv(hashes, save_file):
    csv_ready = []
    for entry in hashes:
        hash = entry
        password = hashes[entry]['password']
        compromised = hashes[entry]['compromised']
        count = hashes[entry]['count']
        csv_ready.append({'hash': hash, 'password': password, 'compromised': compromised, 'count': count})

    fields = ['hash', 'password', 'compromised', 'count']
    with open(save_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = fields)
        writer.writeheader()
        writer.writerows(csv_ready)

clear_text_passwords_file = 'clear_text_passwords.txt'
haveibeenpwned = 'pwnedpasswords.txt'
save_file = 'results.csv'

file_size = stat(haveibeenpwned).st_size

clear_text_passwords = (line.rstrip() for line in open(clear_text_passwords_file))

hashes = {}
for password in clear_text_passwords:
    hash = sha1(bytes(password, 'ascii')).hexdigest().upper()
    if hash not in hashes:
        hashes[hash] = {'password': password}

with open(haveibeenpwned, 'r') as haveibeenpwned_file:
    for hash in hashes:
        print(f'Searching for hash {hash} of password "{hashes[hash]["password"]}".')
        binary_search(hash, haveibeenpwned_file, file_size, hashes)
        if 'compromised' not in hashes[hash].keys():
            hashes[hash]['compromised'] = 'false'
            hashes[hash]['count'] = 0

save_to_csv(hashes, save_file)