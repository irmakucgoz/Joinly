# 🚀 Joinly - İlan & Etkinlik Platformu

**Joinly**, İnsanların kendi aralarında etkinlik planlayabildiği, çalışma grupları kurabildiği ve ilan paylaşabildiği dinamik bir web platformudur. Bu proje, **MAT132** dersi kapsamında "Fonksiyonalite ve Kullanıcı Deneyimi" odaklı olarak geliştirilmiştir.

---

## 🛠 Fonksiyonel Özellikler 

Proje, bir veri objesinin yaşam döngüsünü (CRUD) tam olarak simüle etmektedir:

| Fonksiyon | Açıklama 
| :--- | :---  
| **Listeleme (Read)** | Paylaşılan tüm ilanların ana sayfada kronolojik olarak sunulması. 
| **Yaratma (Create)** | Kullanıcıların mor temalı, dinamik formlarla yeni ilan ekleyebilmesi. 
| **Detay (Detail)** | Her ilanın kendine özel sayfasında tüm ayrıntılarıyla görüntülenmesi. 
| **Düzenleme (Update)** | İlan sahibinin, mevcut veriyi simetrik bir form üzerinden güncelleyebilmesi. 
| **Silme (Delete)** | İlanın, kullanıcı onayı alındıktan sonra sistemden kalıcı olarak kaldırılması. 

---

## 🎨 Tasarım ve Kullanıcı Deneyimi (UI/UX)

Projenin görsel dili **"Joinly Moru"** (#5d3ebc) üzerine inşa edilmiştir:
- **Responsive Tasarım:** İlanlar hem mobilde hem masaüstünde (4'lü ızgara) kusursuz görünür.
- **Merkezi Odaklama:** Giriş ve form sayfaları, kullanıcı dikkatini dağıtmamak adına ekranda tam ortalanmış (Flexbox) şekilde tasarlanmıştır.
- **Dinamik Başlıklar:** Tek bir form yapısı hem "Yeni İlan" hem de "Düzenle" işlemleri için akıllıca (Django logic) kullanılmaktadır.

---

## 🚀 Teknik Altyapı (Tech Stack)

- **Backend:** Django 6.0.3 (Python tabanlı güçlü mimari)
- **Frontend:** HTML5, CSS3 (Custom Grid & Flexbox)
- **Database:** SQLite (Geliştirme aşaması için hafif ve hızlı)
- **Authentication:** Django Custom User Model (E-posta tabanlı giriş)

---

## 💻 Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için:

1. Depoyu bilgisayarınıza indirin:  
   `git clone https://github.com/irmakucgoz/Joinly.git`
2. Gerekli kütüphaneleri kurun:  
   `pip install -r requirements.txt`
3. Veritabanını hazırlayın:  
   `python manage.py migrate`
4. Sunucuyu başlatın:  
   `python manage.py runserver`

---

> **Hazırlayan:** Irmak
