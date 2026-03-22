import cv2
import struct
import hashlib
import os

def decode_video_to_file(input_video_path, output_dir):

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Impossible d'ouvrir la vidéo. Vérifiez le chemin : {input_video_path}")

    byte_stream = bytearray()
    frame_count = 0
    
# Les octets ont été gravés en BGR, OpenCV lit en BGR. C'est du 1 pour 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break  #fin du fichier vidéo

        byte_stream.extend(frame.reshape(-1))
        frame_count += 1
        if frame_count % 10 == 0:
            print(f"   ... {frame_count} frames avalées ...")

    cap.release()
    print(f"{frame_count} frames extraites. {len(byte_stream)} octets.")

    
#Magic Number (4 bytes) 
    magic = byte_stream[0:4]
    if magic != b'MCOD':
        raise ValueError(f"❌ Erreur critique : Magic number attendu 'MCOD', reçu '{magic}'. Ce fichier est corrompu ou n'est pas le bon format.")

#METADATA  (8 octets)
    file_size = struct.unpack('>Q', byte_stream[4:12])[0]
    ext_length = byte_stream[12]

#extension 
    ext_start = 13
    ext_end = ext_start + ext_length
    extension = byte_stream[ext_start:ext_end].decode('utf-8')

#checksum (32 octets)
    checksum_start = ext_end
    checksum_end = checksum_start + 32
    stored_checksum = byte_stream[checksum_start:checksum_end]
    data_start = checksum_end
    print(f"Taille utile = {file_size} octets, Format = .{extension}")

    file_data = byte_stream[data_start : data_start + file_size]
    calculated_checksum = hashlib.sha256(file_data).digest()

    if calculated_checksum != stored_checksum:
        #le fichier sur le disque a été corrupted
        print("❌ ALERTE : le fichier sur le disque a été corrupted")
        raise ValueError("Checksum mismatch: Le fichier reconstitué est corrompu.")
    print("Checksum validé.")
    os.makedirs(output_dir, exist_ok=True)
    
    output_filename = f"recovered_file.{extension}"
    output_file_path = os.path.join(output_dir, output_filename)

    with open(output_file_path, 'wb') as f:
        f.write(file_data)

    print(f" Le fichier ici : {output_file_path}")


if __name__ == "__main__":
    # .mkv
    input_video = r"C:\Users\moths\Downloads\Test.mkv"
    output_folder = r"C:\Users\moths\Downloads\decrypt"
    
    try:
        decode_video_to_file(input_video, output_folder)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")