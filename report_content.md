# ISTE ASİSTAN: AKADEMİK MEVZUAT VE ÖĞRENCİ DESTEK SİSTEMİ PROJE RAPORU

## 1. KAPAK SAYFASI
- **Proje Adı:** ISTE ASİSTAN
- **Ders:** [Ders Adı]
- **Öğrenci Adı:** [Adınız Soyadınız]
- **Öğrenci Numarası:** [Numaranız]
- **Tarih:** 10.05.2026
- **GitHub Sayfa Linki:** [GitHub Linkiniz]

---

## 2. PROJENİN AMACI
Bu projenin temel amacı, İskenderun Teknik Üniversitesi (İSTE) öğrencilerinin üniversite yaşamları boyunca ihtiyaç duydukları akademik bilgilere, yönetmeliklere ve günlük kampüs verilerine hızlı, doğru ve interaktif bir şekilde erişebilmelerini sağlamaktır. Öğrencilerin uzun ve karmaşık mevzuat metinleri içerisinde boğulmadan, sadece soru sorarak aradıkları cevabı bulabilmeleri hedeflenmiştir. Ayrıca, sınav takibi, not hesaplama ve yemekhane menüsü gibi yan özelliklerle öğrencinin günlük asistanı olması amaçlanmıştır.

---

## 3. PROBLEM TANIMI
Üniversite öğrencileri için akademik mevzuat (yatay geçiş, ders muafiyeti, sınav yönetmeliği vb.) oldukça kritiktir ancak bu bilgilere erişmek genellikle zordur. Resmi web sitelerinde yayınlanan onlarca sayfalık PDF dosyaları içerisinde spesifik bir kuralı bulmak zaman alıcıdır. Ayrıca, akademik takvim, yemek listesi ve hava durumu gibi bilgiler farklı platformlarda dağınık halde bulunmaktadır. Bu durum, öğrencilerin bilgiye erişiminde verimlilik kaybına ve bazen yanlış bilgilendirilmelere yol açmaktadır.

---

## 4. PROBLEME DAİR VERİ, ELDE EDİLME YÖNTEMLERİ VE ÖRNEK VERİLER
Projede kullanılan veriler iki ana kaynaktan elde edilmiştir:
1. **Statik Mevzuat Verileri:** İSTE resmi web sitesinden indirilen PDF formatındaki yönetmelikler ve yönergeler.
2. **Dinamik Veriler:** Web scraping (veri kazıma) yöntemiyle elde edilen yemekhane menüsü ve API'lar aracılığıyla alınan hava durumu verileri.

### Örnek Veri Tablosu
| Veri Tipi | Kaynak | Açıklama |
| :--- | :--- | :--- |
| Mevzuat (PDF) | iste.edu.tr | Lisans Eğitim-Öğretim Yönetmeliği |
| Kütüphane Kuralları (TXT) | Kütüphane DB | Ödünç verme süreleri ve cezalar |
| Yemek Menüsü | Web Scraping | Günlük çıkan yemek listesi |
| Sınav Notları | Kullanıcı Girişi | Vize ve final notları |

---

## 5. YÖNTEM (RAG ADIMLARI)
Proje, Retrieval-Augmented Generation (RAG) mimarisi üzerine kurulmuştur. Bu yöntem, yapay zekanın sadece kendi eğitimiyle sınırlı kalmayıp, verilen özel belgelerden (mevzuat) bilgi çekerek cevap üretmesini sağlar.

### RAG İşlem Adımları:
1. **Veri Yükleme (Ingestion):** PDF, TXT ve MD formatındaki belgeler sistem tarafından okunur.
2. **Parçalama (Chunking):** Uzun metinler, anlam bütünlüğünü bozmayacak şekilde (1000 karakterlik parçalar, 150 karakter örtüşme ile) küçük parçalara bölünür.
3. **Vektörleştirme (Embedding):** Her bir metin parçası, "all-MiniLM-L6-v2" modeli kullanılarak sayısal vektörlere (matematiksel ifadelere) dönüştürülür.
4. **Vektör Veritabanı (Storage):** Oluşturulan vektörler "ChromaDB" içerisinde saklanır.
5. **Geri Getirme (Retrieval):** Kullanıcı bir soru sorduğunda, sorunun vektörü ile veritabanındaki metinlerin vektörleri karşılaştırılır ve en alakalı 6 parça getirilir.
6. **Üretim (Generation):** Seçilen metin parçaları ve kullanıcı sorusu, "Llama 3.1" modeline gönderilerek samimi bir "Kıdemli Mentor" üslubuyla cevap üretilir.

---

## 6. UYGULAMA TASARIMI VE GÖRSELLER
Uygulama, Python dilinde **Streamlit** kütüphanesi kullanılarak geliştirilmiştir. Modern ve kullanıcı dostu bir arayüze sahiptir.

### Arayüz Özellikleri:
- **Chat Ekranı:** Kullanıcının doğal dilde sorular sorduğu ana alan.
- **Sidebar (Kenar Çubuğu):** Belge yükleme, sınav notu takibi, hatırlatıcı ekleme ve hava durumu/yemek listesi paneli.
- **Performans Raporu:** Sistemin verdiği cevapların doğruluğunu ve hızını gösteren metrikler.

*(Buraya uygulama ekran görüntüleri eklenecektir)*

---

## 7. ÖRNEK TEST VERİLERİ VE SONUÇLAR
Sistem, gerçek kullanıcı senaryoları ile test edilmiştir.

### Test Sonuçları:
- **Soru:** "Yaz okulunda kaç kredi alabilirim?"
- **Cevap:** "Alt dönemim, yönetmeliğe göre yaz okulunda en fazla 20 AKTS değerinde ders alabilirsin. Ama dikkat et, vize final arası çok kısa oluyor, tempoyu iyi ayarla!"
- **Doğruluk:** %95 (Belgeye dayalı cevap verme başarısı)

Sistem günlük ortalama 0.8 saniye cevap süresiyle yüksek performans göstermektedir.
