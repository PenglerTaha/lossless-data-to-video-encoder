import os
import cv2
import numpy as np
import struct
import hashlib

def encode_file_to_video(input_file_path, output_video_path):
    
    with open(input_file_path, 'rb') as f:
        file_data = f.read()
        
    file_size = len(file_data)
    
# "pdf" not ".pdf"
    _, ext = os.path.splitext(input_file_path)
    ext = ext.lstrip('.').encode('utf-8')
    ext_length = len(ext)
    print(f"{file_size} octets. Format : {ext.decode('utf-8')}")

# SECURITE (SOMME CHECKSUM)
    checksum = hashlib.sha256(file_data).digest()

# MAGIC (4) + SIZE (8) + EXT_LEN (1) + EXT (var) + CHECKSUM (32)
    magic = b'MCOD'
    header_format = f'>4s Q B {ext_length}s 32s'
    header = struct.pack(header_format, magic, file_size, ext_length, ext, checksum)
    
    full_data = bytearray(header + file_data)
    total_bytes = len(full_data)

#frame = 1000x1000px * 3 (BGR/RGB) = 3 MB per frame, *24fps = 72 MB/s
    frame_size_bytes = 1000 * 1000 * 3
    remainder = total_bytes % frame_size_bytes
    
    if remainder != 0:
#Si ça ne tombe pas rond, on comble le vide avec des zéros. Ça règle d'un seul coup le souci des pixels incomplets (non multiple de 3) ET de la dernière frame qui ne serait pas pleine. Au décodage, la tronçonneuse s'arrêtera pile au `file_size`, donc on s'en fout.
        padding_needed = frame_size_bytes - remainder
        full_data.extend(b'\x00' * padding_needed)
        
    total_frames = len(full_data) // frame_size_bytes
    print("(MKV + Codec FFV1 à 24 FPS)...")
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_video_path, fourcc, 24.0, (1000, 1000))

    for i in range(total_frames):
        start_idx = i * frame_size_bytes
        end_idx = start_idx + frame_size_bytes
        chunk = full_data[start_idx:end_idx]
        
        frame_array = np.frombuffer(chunk, dtype=np.uint8).reshape((1000, 1000, 3))
        out.write(frame_array)

    out.release()
    print(f"Terminé, fichier ici : {output_video_path}")



# exe
if __name__ == "__main__":
    input_file = r"C:\Users\moths\Downloads\Test.pdf"
    output_video = r"C:\Users\moths\Downloads\Test.mkv"
    
    #si le fichier n'est pas à cet endroit pour faire un test rapide
    if not os.path.exists(input_file):
        print("Fichier introuvable.")
        os.makedirs(os.path.dirname(input_file), exist_ok=True)
        with open(input_file, 'wb') as f:
            f.write(os.urandom(5 * 1024 * 1024))
            
    encode_file_to_video(input_file, output_video)