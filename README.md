# ISTE_ASSISTANT
İSTE öğrencileri için öğrencilik hayatlarını kolaylaştırıcak RAG mimari temelli bir okul asistanı projesi


#  İSTE Akademik Asistan ve Öğrenci Yaşam Rehberi

İskenderun Teknik Üniversitesi (İSTE) öğrencileri için özel olarak geliştirilmiş, kapalı devre çalışan ve dışarıdan izole yapay zeka destekli kapsamlı bir akademik asistan uygulamasıdır. 

Sistem; karmaşık mevzuat metinlerini anında çözen bir **RAG (Retrieval-Augmented Generation)** mimarisinden güç alırken, yemekhane menüsünden sınav sayaçlarına kadar bir öğrencinin kampüs yaşamında ihtiyaç duyduğu her şeyi tek ekranda birleştirir.

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq_API-f55036?style=for-the-badge&logo=groq&logoColor=white)
![LangChain](https://img.shields.io/badge/RAG-LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-1E90FF?style=for-the-badge&logo=data&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Embeddings-HuggingFace-F9AB00?style=for-the-badge&logo=huggingface&logoColor=white)

---

##  Proje Vizyonu ve Öne Çıkan Özellikler

Sadece basit bir soru-cevap botu değil; öğrencinin kişisel notlarını tutabildiği, veri odaklı kararlar alabildiği çok yönlü bir yaşam koçudur:
-  **Halüsinasyonsuz AI:** Sadece resmi belgelere dayalı cevap üretir, uydurma bilgi vermez. Cevabın kaynağını PDF linki olarak sunar.
-  **Canlı Yemekhane Menüsü:** İSTE yemekhane sistemindeki güvenlik doğrulamalarını (token) aşarak günün menüsünü şık bir arayüzle sunar.
-  **Akıllı Sınav Sayacı & Not Hesaplayıcı:** Sınavlara kalan günü hesaplar, vize notunuza göre finalden geçmek için almanız gereken minimum puanı formülize eder.
-  **Lokal Hava Durumu:** İskenderun kampüsünün anlık hava durumunu Türkçe çevirisiyle ekrana yansıtır.

---

##  Teknoloji Yığını (Tech Stack)

| Teknoloji | Kullanım Amacı | Detay |
| :--- | :--- | :--- |
| **Streamlit** | Frontend | Web arayüzü, sohbet ekranı ve interaktif widget'lar. |
| **Groq API** | LLM | Hız ve maliyet etkinliği için `Llama-3.1-8b-instant` modeli. |
| **LangChain** | RAG Altyapısı | Belge yükleme, chunking ve prompt zincirleme (chaining). |
| **HuggingFace** | Embeddings | Offline hız ve güvenlik için `all-MiniLM-L6-v2` modeli. |
| **ChromaDB** | Vektör Veritabanı | Benzerlik araması (Similarity Search) ve metin koordinatlaması. |
| **BeautifulSoup & Requests**| Veri Madenciliği | Yemek menüsü JSON çekimi ve PDF mevzuat scraping işlemleri. |
| **Pandas** | Veri Manipülasyonu | Öğrenci sınav notları ve analitik tabloların yönetimi. |

---

##  Proje Mimarisi ve Modüller (`src/` Dizini)

Proje, S.O.L.I.D prensiplerine uygun, yüksek modüler bir yapıda tasarlanmıştır:

*  **`app.py` (Merkez Kontrol):** Projenin beyni. Sohbet geçmişini (`st.session_state`) yönetir, hızlı "Akıllı Etiketler" sunar ve öğrenci etkileşim loglarını tutar.
*  **`rag_engine.py` (AI Motoru):** Belgeleri okur, `RecursiveCharacterTextSplitter` ile 1000 karakterlik chunk'lara böler. Sorguya en yakın 6 paragrafı (k=6) bularak Llama-3.1'e bağlam olarak iletir.
*  **`scraper.py`:** Resmi mevzuat sayfasını tarayıp PDF linklerini tespit eder, Türkçe karakter temizliği yaparak belgeleri otomatik indirir.
*  **`yemekhane.py`:** Web scraping ve Regex ile İSTE yemekhane menüsünü çeker, UI üzerinde emoji entegrasyonuyla sergiler.
*  **`academic_calendar.py`:** Güz/Bahar sınavlarını takip eder. Sınava 7 günden az kaldığında UI üzerinde dinamik renkli (kırmızı/sarı) uyarılar oluşturur.
*  **`grade_manager.py` & `reminder_manager.py`:** Vize/Final (%40/%60) geçme notu algoritmalarını işletir. Verileri lokal `csv` dosyalarında güvenle saklar.
*  **`weather.py`:** `wttr.in` servisi üzerinden anlık İskenderun hava durumu verisini çeker ve yerelleştirir.
*  **`prompt.py` & `config.py`:** LLM'in resmi ve akademik bir dil kullanmasını sağlayan katı sistem promptlarını ve offline ayarları barındırır.

---

##  Veri Yönetimi

-  **`data/`:** Sistem RAG yapısının referans aldığı ham İSTE PDF, MD ve TXT dökümanlarının bulunduğu havuz.
-  **`vector_db/`:** Metinlerin sayısal koordinatlara dökülmüş, ChromaDB tarafından yönetilen sıkıştırılmış vektör formatları.
-  **`logs.csv`:** Sisteme sorulan soruların, latency (yanıt süresi) değerlerinin ölçüldüğü ve "Performans Raporu" oluşturulmasını sağlayan sistem günlüğü.

---

##  Kurulum ve Çalıştırma

Projeyi lokalinizde test etmek için aşağıdaki adımları izleyin:

1. **Depoyu Klonlayın:**
   ```bash
   git clone [https://github.com/ucera/ISTE_ASSISTANT.git](https://github.com/ucera/ISTE_ASSISTANT.git)
   cd ISTE_ASSISTANT
