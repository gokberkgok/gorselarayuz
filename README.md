# Rezervasyon Sistemi Kurulum ve Çalıştırma Rehberi

Bu projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın.

## 1. Veritabanı Kurulumu
Proje veritabanı olarak MySQL kullanmaktadır.

1. **XAMPP** kontrol panelini açın ve **MySQL** servisini başlatın.
2. **HeidiSQL** (veya phpMyAdmin) programını açarak veritabanınıza bağlanın.
3. `rezervasyon_db` adında yeni bir veritabanı oluşturun.
4. Proje klasöründeki `db.sql` dosyasını bu veritabanının içine aktarın (İçe Aktar / Import).

## 2. Sunucuyu (Backend) Başlatma
Arka uç sunucusunu başlatmak için proje ana dizininde bir terminal (komut satırı) açın ve şu komutu çalıştırın:

```bash
uvicorn backend.main:app --reload
```

## 3. Arayüzü (Frontend) Başlatma
Sunucu çalıştıktan sonra, masaüstü uygulamasını başlatmak için **yeni bir terminal sekmesi** açın ve şu komutu çalıştırın:

```bash
python -m frontend.main
```

---

## 🔑 Yönetici (Admin) Giriş Bilgileri
Sistem açıldığında, hazır gelen admin hesabı ile giriş yapabilirsiniz:
- **E-posta:** `admin@admin.com`
- **Şifre:** `admin123`
