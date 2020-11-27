import hashlib, getpass
from tqdm import tqdm

def rawcount(filename):
    f = open(filename, 'rb')
    lines = 0
    buf_size = 2048 * 2048
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)
    return lines

password = getpass.getpass(prompt='Password: ', stream=None)
ascii_password_byte = bytes(password, 'ascii')

hash_object = hashlib.sha1(ascii_password_byte)
hash = hash_object.hexdigest()

with open("FILENAME") as infile:
    for line in tqdm(infile, total=rawcount("FILENAME")):
        if hash.lower() == line.split(':')[0].lower():
            print("MATCH!")
            print(line)
            break