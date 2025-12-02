# 🔒 Secure-LSB-Steganography
### AES-256 Şifrelemeyle Desteklenmiş Python Steganografi Aracı

## 🚀 Proje Hakkında
Bu araç, gizli mesajları görsel dosyaların piksel verilerine gömmek (**Steganography**) için tasarlanmıştır. Gömme işleminden önce mesajlar, modern ve güçlü bir şifreleme standardı olan **AES-256** ile şifrelenir. Bu, mesajın deşifre edilebilmesi için hem şifreli görsele hem de doğru **`secret.key`** dosyasına sahip olmayı zorunlu kılar.

**Amaç:** Siber güvenlik ve gizli iletişim prensiplerini uygulamalı olarak göstermek ve LSB ile Kriptografiyi birleştirmek.

## 🛠️ Teknik Detaylar

Proje, iki temel güvenlik mekanizması kullanır ve **algoritma bilginizi** gösterir:

1.  **LSB (Least Significant Bit - En Az Anlamlı Bit) Steganography:**
    Görselin her bir pikselinin (Kırmızı, Yeşil, Mavi kanallarının) **en az önemli bitini** (son 1 bitini) mesajın ikili (binary) verisiyle değiştirir. Bu minimal değişiklik, insan gözüyle ayırt edilemez.
2.  **Fernet Kriptografi (AES-256):**
    Mesaj, LSB ile gizlenmeden önce, Fernet (AES-128'in geliştirilmiş versiyonu) kullanılarak şifrelenir. Bu, veriye ek bir güvenlik katmanı sağlar.

## Kurulum ve Başlangıç

### Önkoşullar
* Python 3.x
* Gerekli kütüphaneler (`Pillow` ve `cryptography`)

### Kurulum Adımları
Gerekli kütüphaneleri `requirements.txt` dosyasını kullanarak kurun:

```bash
# Gerekli kütüphaneleri tek komutla kur
pip install -r requirements.txt
