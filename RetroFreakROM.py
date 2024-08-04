#!/usr/bin/env python3

from os import urandom
from argparse import ArgumentParser
from os.path import isfile, join, basename
from struct import unpack, pack_into, unpack_from
from binascii import unhexlify, crc32, hexlify as _hexlify

# pip install pycryptodomex
from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import MD5, SHA1
from Cryptodome.Util.Padding import unpad
from Cryptodome.Signature import PKCS1_v1_5

ROM_MAGIC = b"RFRK"
ROM_SECRET = unhexlify("6F5BC7F1068C3D60D6A62E757739453A")
REQUEST_MAGIC = b"WPR2"
REQUEST_SECRET = unhexlify("D7A1066CE2DC0D5A8636D1E8D0965E90")
REQUEST_FILE = "serial.txt"

REQUEST_SIZE = 192

NES_MAGIC = b"NES\x1a"

REQUEST_PUB_KEY = None

hexlify = lambda b: _hexlify(b).decode("utf8").upper()

def read_file(filename: str) -> bytes:
	with open(filename, "rb") as f:
		data = f.read()
	return data

def write_file(filename: str, data: (bytes, bytearray)) -> None:
	with open(filename, "wb") as f:
		f.write(data)
		
def derive_rom_key(dna: (bytes, bytearray)) -> bytes:
	global ROM_SECRET

	digest = bytearray(MD5.new(dna).digest())
	for i in range(16):
		digest[i] ^= ROM_SECRET[i]
	return bytes(digest)

def decrypt_rom(dna: (bytes, bytearray), data: (bytes, bytearray)) -> (bytes, bytearray):
	global ROM_MAGIC

	key = derive_rom_key(dna)
	assert data[:4] == ROM_MAGIC, "Invalid magic"
	iv = data[0x10:0x10 + 16]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	dec_data = cipher.decrypt(data[0x20:0x20 + 0x1E0])
	(magic, rom_crc, rom_size) = unpack_from("<4s 2I", dec_data, 0)
	assert magic == ROM_MAGIC, "Invalid magic"
	dec_data = cipher.decrypt(data[0x200:0x200 + rom_size])
	if dec_data[:4] == NES_MAGIC: # Adding NES rom handler missing from original code

                # Decouple iNES header from rom body
                NES_header = dec_data[:0x10]
                NES_rom = dec_data[0x10:]

                # Get correct rom CRC by ignoring iNES header
                dec_crc = crc32(NES_rom)

                # Getting and fixing iNES header and flags
                flag_6 = NES_header[6]
                flag_9 = NES_header[9]
                
                # Inspect and fix error in iNES flag 9 as it can only be 0 or 1
                if flag_9 > 0x01:
                        print("Bad iNES Header: " + str(NES_header))
                        NES_header = NES_header[:9] + b'\x00' + NES_header[10:] # Forcing flag 9 as NTSC in iNES header

                # Fixing wrong first bit for flag 6
                flag_6 ^= 1 << 0 # flipped the first bit
                NES_header = NES_header[:6] + flag_6.to_bytes(1,'little') + NES_header[7:]
                print("Fixed Header: " + str(NES_header))
    
                # Recombind header with rom
                dec_data = NES_header + NES_rom

	else:
                dec_crc = crc32(dec_data)

        print("Org CRC: " + str(hex(rom_crc)))
        print("Dec CRC: " + str(hex(dec_crc)))
        assert rom_crc == dec_crc, "Invalid ROM checksum"

	return dec_data

def encrypt_rom(dna: (bytes, bytearray), data: (bytes, bytearray)) -> (bytes, bytearray):
	global ROM_MAGIC

	key = derive_rom_key(dna)
	hdr_buf = bytearray(urandom(0x200))
	(iv,) = unpack_from("16s", hdr_buf, 0x10)

	if data[:4] == NES_MAGIC: # Get correct rom CRC by ignoring iNES header
                data_crc = crc32(data[0x10:])
        else:
                data_crc = crc32(data)

        print("Rom CRC: " + str(hex(data_crc)))
        
	pack_into("<4s", hdr_buf, 0, ROM_MAGIC)
	pack_into("<4s 2I", hdr_buf, 0x20, ROM_MAGIC, crc32(data), len(data))
	cipher = AES.new(key, AES.MODE_CBC, iv)
	pack_into(f"{0x1E0}s", hdr_buf, 0x20, cipher.encrypt(hdr_buf[0x20:0x20 + 0x1E0]))
	return hdr_buf + cipher.encrypt(data)

def main() -> None:
	global REQUEST_PUB_KEY, REQUEST_PUB_KEY_FILE, ROM_MAGIC, REQUEST_FILE

	REQUEST_PUB_KEY = RSA.import_key(read_file(join("Keys", REQUEST_PUB_KEY_FILE)))

	parser = ArgumentParser(description="A script to encrypt/decrypt ROM's to/from the RetroFreak")
	parser.add_argument("ifile", type=str, help="The ROM to read from")
	parser.add_argument("-o", type=str, help="The ROM file to write to")
	parser.add_argument("-s", "--serial", type=str, help="The serial number you want to use")
	parser.add_argument("-k", "--keyfile", type=str, default=REQUEST_FILE, help="The serial number in serial.txt file to read from")
	
	args = parser.parse_args()

	assert isfile(args.ifile), "The specified ROM file doesn't exist"

	if args.serial:
		dna = unhexlify(args.serial)
	elif args.keyfile and isfile(args.keyfile):
		dna = unhexlify(read_file(args.keyfile))
	else:
		raise FileNotFoundError("-s (--serial) or -k (--keyfile) is required but not provided")

	print("Serial #: " + hexlify(dna))

	rom_data = read_file(args.ifile)
	if rom_data[:4] == ROM_MAGIC:  # encrypted
		print(f"Decrypting \"{basename(args.ifile)}\"...")
		write_file(args.o if args.o else args.ifile, decrypt_rom(dna, rom_data))
	else:  # plaintext
		print(f"Encrypting \"{basename(args.ifile)}\"...")
		write_file(args.o if args.o else args.ifile, encrypt_rom(dna, rom_data))
	print("Done!")


if __name__ == "__main__":
	main()
