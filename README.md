# lossless-data-to-video-encoder
A Python pipeline to encode binary files into lossless MKV video frames and decode them back perfectly. A project in: data encoding systems, steganography foundations, multimedia data pipelines


# File-to-Video Lossless Encoding System

## Overview

This project implements a **deterministic, lossless file-to-video encoding pipeline**. It enables any binary file (PDF, image, executable, etc.) to be converted into a video stream and later reconstructed **bit-for-bit identical** to the original.

The system is built around a simple but robust principle:
**map raw bytes directly into pixel data, store them in a lossless video stream, and reconstruct them deterministically.**

This is not encryption. It is a **data transport and transformation protocol** with integrity guarantees.

---

## Key Features

* **Lossless Encoding**: Every byte of the original file is preserved.
* **Deterministic Reconstruction**: Output file is identical to input (verified via checksum).
* **Structured Metadata Header**:

  * Magic identifier (`MCOD`)
  * File size
  * File extension
  * SHA-256 checksum
* **High Throughput**:

  * ~3 MB per frame (1000×1000×3)
  * ~72 MB/s at 24 FPS
* **Integrity Validation**:

  * SHA-256 ensures detection of any corruption
* **Efficient Processing**:

  * NumPy vectorization (no pixel-level loops)
* **Codec Safety**:

  * Uses **FFV1 (lossless)** to preserve pixel fidelity

---

## System Architecture

### Encoding Pipeline

```
File → Byte Stream → Header Injection → Padding → Frame Mapping → Video Encoding
```

### Decoding Pipeline

```
Video → Frame Extraction → Byte Stream Reconstruction → Header Parsing → Validation → File Reconstruction
```

---

## Technical Design

### 1. Byte-to-Pixel Mapping

Each pixel encodes **3 bytes**:

```
(R, G, B) → 3 bytes
```

Frame capacity:

```
1000 × 1000 × 3 = 3,000,000 bytes per frame (~3 MB)
```

---

### 2. Header Structure

The system embeds metadata at the start of the byte stream:

| Field      | Size     | Description                 |
| ---------- | -------- | --------------------------- |
| MAGIC      | 4 bytes  | Format identifier (`MCOD`)  |
| FILE_SIZE  | 8 bytes  | Original file size          |
| EXT_LENGTH | 1 byte   | Extension length            |
| EXT        | variable | File extension (e.g. "pdf") |
| CHECKSUM   | 32 bytes | SHA-256 hash of file        |

Packed using big-endian format:

```python
'>4s Q B {ext_length}s 32s'
```

---

### 3. Padding Strategy

To ensure full frame alignment:

* If total bytes ≠ multiple of frame size → pad with `0x00`
* Padding is safely ignored during decoding using `FILE_SIZE`

---

### 4. Video Encoding

* Resolution: **1000 × 1000**
* Channels: **3 (BGR)**
* Codec: **FFV1 (lossless)**
* Container: **MKV**

Why FFV1:

* No compression artifacts
* Exact pixel preservation
* Required for deterministic reconstruction

---

### 5. Integrity Verification

Checksum mechanism:

```python
SHA-256(original_data)
```

During decoding:

* Recomputed checksum is compared to stored checksum
* Any mismatch → immediate failure

---

## Usage

### Encoding

```python
encode_file_to_video(input_file_path, output_video_path)
```

Example:

```python
input_file = r"C:\path\to\file.pdf"
output_video = r"C:\path\to\output.mkv"
```

---

### Decoding

```python
decode_video_to_file(input_video_path, output_directory)
```

Example:

```python
input_video = r"C:\path\to\video.mkv"
output_folder = r"C:\path\to\output"
```

---

## Dependencies

Install required libraries:

```bash
pip install opencv-python numpy
```

---

## Performance Considerations

### Strengths

* Fast encoding due to vectorized operations
* High data density per frame
* Minimal CPU overhead per byte

### Limitations

* **High storage usage** (lossless video)
* Entire file loaded into RAM (not optimized for very large files)
* Sequential decoding required (no random access)

---

## Failure Conditions

The system will fail (by design) if:

* Lossy codec is used (e.g., MP4, H.264)
* Frames are dropped or reordered
* Resolution or channel format is altered
* Any byte is modified (checksum mismatch)

---


For secure usage:

```
Encrypt → Encode → Store → Decode → Decrypt
```

---

## Future Improvements

* Streaming support (avoid full RAM load)
* Adaptive resolution based on file size
* Multi-threaded encoding
* Redundant headers for fault tolerance
* Optional AES encryption layer
* Frame indexing for faster decoding

---

## Conclusion

This project demonstrates a **robust, lossless data encoding mechanism using video as a transport medium**. With proper codec selection (FFV1), it achieves **bit-perfect reconstruction**, making it suitable for:

* Data archival experiments
* Steganographic research foundations
* Custom data transport systems
* Educational demonstrations of encoding pipelines

---

## Author Notes

This implementation prioritizes:

* determinism
* integrity
* simplicity of reconstruction

It is intentionally designed as a **low-level, transparent system**, making every transformation traceable and verifiable.
@penglertaha  22-03-2026 1:03PM

---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---

#Français
# Système d’Encodage de Fichiers en Vidéo (Lossless)

## Vue d’ensemble

Ce projet implémente un **pipeline déterministe et sans perte (lossless)** permettant de convertir n’importe quel fichier binaire (PDF, image, exécutable, etc.) en une vidéo, puis de le reconstruire **bit à bit à l’identique**.

Le principe est simple et robuste :
**mapper directement les octets en pixels, les stocker dans une vidéo sans perte, puis reconstruire le flux original.**

Ce système n’est pas un chiffrement. C’est un **protocole de transformation et de transport de données** avec garantie d’intégrité.

---

## Fonctionnalités principales

* **Encodage sans perte** : chaque octet est conservé
* **Reconstruction déterministe** : sortie identique à l’entrée (vérifiée par checksum)
* **En-tête structuré (header)** :

  * Identifiant magique (`MCOD`)
  * Taille du fichier
  * Extension
  * Empreinte SHA-256
* **Débit élevé** :

  * ~3 Mo par frame (1000×1000×3)
  * ~72 Mo/s à 24 FPS
* **Validation d’intégrité** :

  * SHA-256 détecte toute altération
* **Optimisation des performances** :

  * Vectorisation NumPy (aucune boucle pixel)
* **Fiabilité codec** :

  * Utilisation de **FFV1 (lossless)**

---

## Architecture du système

### Pipeline d’encodage

```text id="jvzt3d"
Fichier → Flux d’octets → Injection du header → Padding → Mapping pixels → Encodage vidéo
```

### Pipeline de décodage

```text id="z7wq0s"
Vidéo → Extraction des frames → Reconstruction du flux → Parsing header → Validation → Reconstruction fichier
```

---

## Conception technique

### 1. Mapping octets → pixels

Chaque pixel encode **3 octets** :

```text id="fd4q3k"
(R, G, B) → 3 octets
```

Capacité d’une frame :

```text id="zssr4e"
1000 × 1000 × 3 = 3 000 000 octets (~3 Mo)
```

---

### 2. Structure du header

Les métadonnées sont injectées au début du flux :

| Champ      | Taille    | Description           |
| ---------- | --------- | --------------------- |
| MAGIC      | 4 octets  | Identifiant (`MCOD`)  |
| FILE_SIZE  | 8 octets  | Taille originale      |
| EXT_LENGTH | 1 octet   | Longueur extension    |
| EXT        | variable  | Extension (ex: "pdf") |
| CHECKSUM   | 32 octets | Hash SHA-256          |

Format binaire :

```python id="eixzfd"
'>4s Q B {ext_length}s 32s'
```

---

### 3. Stratégie de padding

Pour aligner parfaitement les frames :

* Si la taille ≠ multiple de la frame → padding en `0x00`
* Ignoré au décodage grâce à `FILE_SIZE`

---

### 4. Encodage vidéo

* Résolution : **1000 × 1000**
* Canaux : **3 (BGR)**
* Codec : **FFV1 (lossless)**
* Conteneur : **MKV**

Pourquoi FFV1 :

* aucune perte
* pixels strictement identiques
* indispensable pour reconstruction fiable

---

### 5. Vérification d’intégrité

Calcul :

```python id="ksh5gc"
SHA-256(données_originales)
```

Au décodage :

* recalcul du hash
* comparaison avec le hash stocké
* toute différence → erreur

---

## Utilisation

### Encodage

```python id="6f1n6m"
encode_file_to_video(input_file_path, output_video_path)
```

Exemple :

```python id="t1ndu9"
input_file = r"C:\chemin\fichier.pdf"
output_video = r"C:\chemin\sortie.mkv"
```

---

### Décodage

```python id="96v8mn"
decode_video_to_file(input_video_path, output_directory)
```

Exemple :

```python id="v2mjlwm"
input_video = r"C:\chemin\video.mkv"
output_folder = r"C:\chemin\sortie"
```

---

## Dépendances

Installation :

```bash id="q4a7nx"
pip install opencv-python numpy
```

---

## Performances

### Avantages

* encodage rapide (NumPy)
* forte densité de données
* faible overhead CPU

### Limites

* **fichiers volumineux** (lossless)
* chargement en RAM
* décodage séquentiel

---

## Conditions d’échec

Le système échoue si :

* codec avec perte (MP4, H.264…)
* frames manquantes ou désordonnées
* résolution modifiée
* altération d’un seul octet (checksum)

---

Pour sécuriser :

```text id="8xkks9"
Chiffrer → Encoder → Stocker → Décoder → Déchiffrer
```

---

## Améliorations possibles

* support streaming (éviter RAM complète)
* résolution dynamique
* multithreading
* header redondant
* couche AES
* indexation des frames

---

## Conclusion

Ce projet met en place un **système fiable d’encodage de données en vidéo sans perte**, permettant une reconstruction parfaite.

Cas d’usage :

* archivage expérimental
* base pour stéganographie
* transport de données
* démonstration pédagogique

---

## Notes

L’implémentation privilégie :

* la déterminisme
* l’intégrité
* la transparence

Chaque transformation est traçable et vérifiable.
@penglertaha  22-03-2026 1:03PM
