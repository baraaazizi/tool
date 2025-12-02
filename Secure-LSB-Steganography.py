import os
from PIL import Image
from cryptography.fernet import Fernet
import sys

# === YARDIMCI FONKSİYONLAR (HELPER FUNCTIONS) ===

def generate_key():
    """
    Şifreleme için rastgele bir anahtar üretir ve 'secret.key' dosyasına kaydeder.
    """
    if not os.path.exists("secret.key"):
        try:
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file: # YAZMA MODU (wb)
                key_file.write(key)
            print("[+] Yeni anahtar oluşturuldu: secret.key")
        except Exception as e:
            print(f"[-] HATA: Anahtar oluşturulamadı. İzin sorunu olabilir: {e}")
            sys.exit(1)
    else:
        print("[!] Mevcut anahtar dosyası (secret.key) kullanılıyor.")

def load_key():
    """secret.key dosyasından anahtarı okur."""
    try:
        # KRİTİK DÜZELTME: Anahtarı okumak için 'rb' (read binary) modu kullanılmalı!
        return open("secret.key", "rb").read() # OKUMA MODU (rb)
    except FileNotFoundError:
        print("[-] HATA: 'secret.key' dosyası bulunamadı! Önce şifreleme yapmalısınız.")
        return None

def text_to_bin(message):
    return ''.join(format(ord(i), '08b') for i in message)

def bin_to_text(binary_message):
    binary_values = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    ascii_string = ""
    for binary_value in binary_values:
        try:
            ascii_string += chr(int(binary_value, 2))
        except:
            pass
    return ascii_string

# === ANA FONKSİYONLAR (CORE LOGIC) ===

def encrypt_and_hide(image_path, secret_message, output_path):
    # 1. Anahtar Yönetimi ve Şifreleme
    generate_key()
    key = load_key()
    if not key: return 
    
    try:
        f = Fernet(key)
    except Exception as e:
        print(f"[-] KRİTİK HATA: Anahtar bozuk ({e}). Lütfen 'secret.key' dosyasını silip tekrar deneyin.")
        return

    try:
        # Mesajı şifrele
        encrypted_message = f.encrypt(secret_message.encode())
        encrypted_str = encrypted_message.decode() + "#####"
        
        binary_msg = text_to_bin(encrypted_str)
        msg_len = len(binary_msg)
        
        # 2. Resim İşlemleri
        img = Image.open(image_path) # <-- HATA BURADA ÇIKIYOR
        img = img.convert("RGB")
        pixels = img.load()
        width, height = img.size
        
        max_capacity = width * height * 3
        if msg_len > max_capacity:
            print(f"[-] HATA: Mesaj çok uzun! Bu resme sığmaz.")
            return

        print(f"[*] Şifreli mesaj resme işleniyor... ({msg_len} bit)")
        
        data_index = 0
        for y in range(height):
            for x in range(width):
                if data_index < msg_len:
                    r, g, b = pixels[x, y]
                    
                    # LSB Algoritması
                    if data_index < msg_len:
                        r = int(format(r, '08b')[:-1] + binary_msg[data_index], 2)
                        data_index += 1
                    if data_index < msg_len:
                        g = int(format(g, '08b')[:-1] + binary_msg[data_index], 2)
                        data_index += 1
                    if data_index < msg_len:
                        b = int(format(b, '08b')[:-1] + binary_msg[data_index], 2)
                        data_index += 1
                        
                    pixels[x, y] = (r, g, b)
                else:
                    break
            if data_index >= msg_len:
                break
        
        img.save(output_path)
        print(f"[+] İŞLEM BAŞARILI! Gizli resim '{output_path}' olarak kaydedildi.")
        print(f"[!] UNUTMA: Mesajı çözmek için 'secret.key' dosyasına ihtiyacın var.")
        
    except Exception as e:
        print(f"[-] Bir HATA OLUŞTU! Kontrol Et: Dosya adı doğru mu? İzinler tam mı? Hata: {e}")

def reveal_and_decrypt(image_path):
    try:
        key = load_key()
        if not key: return

        f = Fernet(key)
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = img.load()
        width, height = img.size
        
        binary_data = ""
        print("[*] Resim taranıyor ve veri çıkarılıyor...")
        
        # Tüm pikselleri tara
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_data += format(r, '08b')[-1]
                binary_data += format(g, '08b')[-1]
                binary_data += format(b, '08b')[-1]

        all_text = bin_to_text(binary_data)
        
        if "#####" in all_text:
            encrypted_str = all_text.split("#####")[0]
            print("[*] Gizli veri bulundu, şifre çözülüyor...")
            
            try:
                decrypted_msg = f.decrypt(encrypted_str.encode()).decode()
                print(f"\n{'-'*30}")
                print(f"GİZLİ MESAJ: {decrypted_msg}")
                print(f"{'-'*30}\n")
            except:
                print("[-] HATA: Şifre çözülemedi! Yanlış 'secret.key' veya bozuk veri.")
        else:
            print("[-] Bu resimde gizli bir mesaj bulunamadı.")
            
    except Exception as e:
        print(f"[-] Bir hata oluştu: {e}")

# === MENÜ (CLI) ===

if __name__ == "__main__":
    print("######################################")
    print("#   Secure Steganography Tool v1.0   #")
    print("#   AES-256 Encryption + LSB Logic   #")
    print("######################################")
    
    while True:
        print("\n1. Resme Mesaj Gizle (Encrypt & Hide)")
        print("2. Resimden Mesaj Oku (Decrypt & Reveal)")
        print("3. Çıkış")
        
        choice = input("Seçiminiz: ")
        
        if choice == '1':
            img_in = input("Orijinal resim yolu (örn: image.png): ")
            msg = input("Gizlenecek mesaj: ")
            img_out = input("Çıktı dosyası adı (örn: secret.png): ")
            encrypt_and_hide(img_in, msg, img_out)
            
        elif choice == '2':
            img_in = input("Gizli resim yolu (örn: secret.png): ")
            reveal_and_decrypt(img_in)
            
        elif choice == '3':
            print("Görüşürüz!")
            break
        else:
            print("Geçersiz seçim.")