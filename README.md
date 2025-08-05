# 🚀 AURA - Personal Style Assistant AI System

<div align="center">

![AURA AI Logo](https://img.shields.io/badge/AURA-AI%20System-blue?style=for-the-badge&logo=robot)

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://docker.com)
[![Microservices](https://img.shields.io/badge/Architecture-Microservices-orange?style=flat-square)](https://microservices.io)
[![AI/ML](https://img.shields.io/badge/AI%2FML-PyTorch%20%7C%20CLIP-red?style=flat-square&logo=pytorch)](https://pytorch.org)

**Kullanıcıların gardıroplarını dijitalleştiren, kıyafet kombinleri öneren, toplulukla etkileşime geçen ve ikinci el alışveriş yapmalarını sağlayan yapay zeka destekli mobil uygulama**

[Demo](#️-demo) • [Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [API Docs](#-api-dokümantasyonu) • [Katkı](#-katkı)

</div>

---

## 📖 Proje Açıklaması

**AURA**, kullanıcıların kişisel stillerini keşfetmelerine ve geliştirmelerine yardımcı olan gelişmiş bir yapay zeka sistemidir. Kullanıcılar gardıroplarını dijital ortama aktarabilir, AI destekli stil önerileri alabilir, toplulukla etkileşime geçebilir ve sürdürülebilir moda için ikinci el alışveriş yapabilirler.

### 🎯 Misyon
Modern teknoloji ile moda dünyasını birleştirerek, herkesin kendi stilini keşfetmesini ve sürdürülebilir moda alışkanlıkları geliştirmesini sağlamak.

### 🌟 Vizyon
Yapay zeka destekli kişiselleştirilmiş stil danışmanlığı ile moda endüstrisinde dijital dönüşümün öncüsü olmak.

---

## 🚀 Özellikler

### 👗 **Gardırop Dijitalleştirme**
- **Akıllı Görüntü Analizi**: AI destekli kıyafet tanıma ve kategorilendirme
- **Otomatik Etiketleme**: Renk, desen, stil ve marka bilgilerinin otomatik çıkarılması
- **Dijital Gardırop Yönetimi**: Kıyafetlerin organize edilmesi ve takip edilmesi

### 🎨 **AI Destekli Stil Danışmanlığı**
- **Kişiselleştirilmiş Öneriler**: Kullanıcının tarzına uygun kombinler
- **Trend Analizi**: Güncel moda trendlerinin takibi ve önerilere entegrasyonu
- **Mevsimsel Öneriler**: Hava durumu ve mevsime uygun kıyafet önerileri
- **Özel Durum Stilizmi**: Iş, gece, spor, özel etkinlik vb. için özel öneriler

### 🤝 **Sosyal Topluluk**
- **Stil Paylaşımı**: Kombinlerin toplulukla paylaşılması
- **Oylamalı Değerlendirme**: Topluluk geribildirimi ile stil puanlama
- **Stil Meydan Okumaları**: Haftalık/aylık tema bazlı stil yarışmaları
- **Takip Sistemi**: Beğenilen kullanıcıların takip edilmesi

### 🛒 **Sürdürülebilir Alışveriş**
- **Ikinci El Pazarı**: AI destekli eşleştirme sistemi
- **Değer Takdiri**: Kıyafetlerin güncel piyasa değerinin analizi
- **Sürdürülebilirlik Puanı**: Satın alma kararlarında çevre dostu seçeneklerin vurgulanması
- **Takas Sistemi**: Kıyafet değişimi için akıllı eşleştirme

### 🧠 **Gelişmiş AI Yetenekleri**
- **Doğal Dil İşleme**: Türkçe stil isteklerinin anlaşılması
- **Görüntü İşleme**: Gelişmiş bilgisayarlı görü teknolojileri
- **Makine Öğrenmesi**: Kullanıcı tercihlerinden sürekli öğrenme
- **Feedback Loop**: Kullanıcı geribildirimleri ile sistem iyileştirme

---

## 🏗️ Mimari ve Teknolojiler

### 🎯 **Mikroservis Mimarisi**

```
AURA AI Ecosystem
├── 🖼️  Image Processing Service      (Port 8001)
├── 🧠 NLU Service                    (Port 8002) 
├── 👤 Style Profile Service          (Port 8003)
├── 🎨 Combination Engine Service     (Port 8004)
├── 💡 Recommendation Engine Service  (Port 8005)
├── 🔄 Feedback Loop Service          (Port 8006)
└── 🎯 Orchestrator Service           (Port 8007)
```

### 🛠️ **Teknoloji Yığını**

#### **Backend Framework**
- **FastAPI**: Yüksek performanslı API geliştirme
- **Pydantic**: Veri doğrulama ve serileştirme
- **Uvicorn**: ASGI sunucu

#### **AI/ML Stack**
- **PyTorch**: Derin öğrenme modelleri
- **CLIP**: Görsel-metin anlayışı
- **Detectron2**: Nesne tespiti ve segmentasyon
- **Transformers**: Doğal dil işleme
- **OpenCV**: Bilgisayarlı görü işlemleri

#### **Veritabanı & Depolama**
- **PostgreSQL**: İlişkisel veri yönetimi
- **Redis**: Önbellekleme ve oturum yönetimi
- **MinIO**: Nesne depolama (görüntüler için)

#### **DevOps & Dağıtım**
- **Docker**: Konteynerizasyon
- **Docker Compose**: Çoklu servis orkestrasyon
- **GitHub Actions**: CI/CD pipeline
- **Nginx**: Reverse proxy ve yük dengeleme

#### **Monitoring & Logging**
- **Prometheus**: Metrikleri toplama
- **Grafana**: Görselleştirme ve dashboard
- **ELK Stack**: Log analizi

---

## 📦 Kurulum

### 🔧 **Sistem Gereksinimleri**

- **Python**: 3.9 veya üzeri
- **Docker**: 20.10 veya üzeri
- **Docker Compose**: 1.29 veya üzeri
- **Minimum RAM**: 8GB (16GB önerilir)
- **Disk Alanı**: 10GB boş alan
- **GPU** (İsteğe bağlı): CUDA destekli GPU (performans için)

### 🚀 **Hızlı Başlangıç**

#### 1. **Repository'yi Klonlayın**
```bash
git clone https://github.com/Emirhan55-AI/AURA_AI.git
cd AURA_AI
```

#### 2. **Ortam Değişkenlerini Ayarlayın**
```bash
cp .env.example .env
# .env dosyasını düzenleyerek gerekli değişkenleri ayarlayın
```

#### 3. **Docker ile Tüm Sistemi Başlatın**
```bash
# Tüm servisleri build edin ve başlatın
docker-compose up --build -d

# Servislerin durumunu kontrol edin
docker-compose ps
```

#### 4. **Sistem Sağlık Kontrolü**
```bash
# Sağlık kontrolü scripti çalıştırın
./scripts/health_check.sh
```

### 🔧 **Manuel Kurulum (Geliştirme için)**

#### 1. **Python Sanal Ortamı Oluşturun**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate     # Windows
```

#### 2. **Bağımlılıkları Yükleyin**
```bash
pip install -r requirements.txt
```

#### 3. **Veritabanını Başlatın**
```bash
# PostgreSQL ve Redis'i Docker ile başlatın
docker-compose up -d postgres redis
```

#### 4. **Servisleri Tek Tek Başlatın**
```bash
# Örnek: Image Processing Service
cd services/image_processing_service
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

---

## ▶️ Çalıştırma

### 🐳 **Docker Compose ile (Önerilen)**

```bash
# Tüm servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f

# Servisleri durdur
docker-compose down
```

### 🔧 **Geliştirme Modu**

```bash
# Geliştirme ortamı scripti
./scripts/dev_setup.sh

# Tek bir servisi geliştirme modunda çalıştır
cd services/image_processing_service
uvicorn main:app --reload --port 8001
```

### 📊 **Monitoring Dashboard**

```bash
# Grafana dashboard
http://localhost:3000

# Prometheus metrics
http://localhost:9090
```

---

## 🧪 Test

### 🚀 **Otomatik Test Çalıştırma**

```bash
# Tüm testleri çalıştır
./scripts/run_tests.sh

# Belirli bir servisin testlerini çalıştır
./scripts/test_service.sh image_processing

# Test coverage raporu
./scripts/coverage_report.sh
```

### 🔧 **Manuel Test**

```bash
# Unit testler
python -m pytest tests/unit/

# Integration testler
python -m pytest tests/integration/

# End-to-end testler
python -m pytest tests/e2e/
```

### 📊 **Test Coverage**

```bash
# Coverage raporu oluştur
coverage run -m pytest
coverage html
# htmlcov/index.html dosyasını açın
```

---

## 📚 API Dokümantasyonu

### 🌐 **Interactive API Docs**

Her servis kendi Swagger UI dokümantasyonuna sahiptir:

- **Orchestrator**: http://localhost:8007/docs
- **Image Processing**: http://localhost:8001/docs
- **NLU Service**: http://localhost:8002/docs
- **Style Profile**: http://localhost:8003/docs
- **Combination Engine**: http://localhost:8004/docs
- **Recommendation Engine**: http://localhost:8005/docs
- **Feedback Loop**: http://localhost:8006/docs

### 📖 **Detaylı Dokümantasyon**

- [Mimari Rehberi](docs/ARCHITECTURE.md)
- [API Referansı](docs/API.md)
- [Geliştirici Rehberi](docs/DEVELOPMENT.md)
- [Deployment Rehberi](docs/DEPLOYMENT.md)

### 🔧 **Örnek API Kullanımı**

```python
import requests

# Görüntü analizi
response = requests.post(
    'http://localhost:8001/analyze',
    files={'image': open('shirt.jpg', 'rb')}
)

# Stil profili oluşturma
response = requests.post(
    'http://localhost:8003/profile',
    json={
        'user_id': 'user123',
        'preferences': {
            'style': 'casual',
            'colors': ['blue', 'white'],
            'brands': ['zara', 'h&m']
        }
    }
)
```

---

## 🤝 Katkı

### 💡 **Katkıda Bulunma Süreci**

1. **Fork edin** ve yeni bir branch oluşturun
2. **Değişikliklerinizi yapın** ve test edin
3. **Commit mesajlarını** anlamlı yazın
4. **Pull Request** oluşturun

### 📋 **Katkı Kuralları**

- [Katkı Rehberi](CONTRIBUTING.md)
- [Kod Standartları](docs/CODE_STANDARDS.md)
- [Commit Konvansiyonları](docs/COMMIT_CONVENTIONS.md)

### 🐛 **Hata Bildirimi**

Hata bulduğunuzda lütfen [GitHub Issues](https://github.com/Emirhan55-AI/AURA_AI/issues) üzerinden bildirin.

### ✨ **Özellik İsteği**

Yeni özellik önerilerinizi [Discussions](https://github.com/Emirhan55-AI/AURA_AI/discussions) bölümünde paylaşabilirsiniz.

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Detaylar için `LICENSE` dosyasını inceleyebilirsiniz.

---

## 📞 İletişim & Destek

### 👨‍💻 **Geliştirici**
- **GitHub**: [@Emirhan55-AI](https://github.com/Emirhan55-AI)
- **Email**: emirhan.ai.dev@gmail.com

### 🌟 **Proje Bağlantıları**
- **GitHub Repository**: https://github.com/Emirhan55-AI/AURA_AI
- **Documentation**: https://emirhan55-ai.github.io/AURA_AI
- **Demo Site**: https://aura-ai-demo.herokuapp.com

### 💬 **Topluluk**
- **Discord**: [AURA AI Community](https://discord.gg/aura-ai)
- **Telegram**: [@aura_ai_community](https://t.me/aura_ai_community)

---

## 🙏 Teşekkürler

- **Open Source Community**: Kullandığımız açık kaynak kütüphaneler için
- **AI/ML Research Community**: İlham aldığımız araştırmalar için
- **Beta Testers**: Değerli geribildirimleri için
- **Contributors**: Projeye katkıda bulunan herkese

---

<div align="center">

**🌟 AURA AI ile stilinizi keşfedin! 🌟**

[![Stars](https://img.shields.io/github/stars/Emirhan55-AI/AURA_AI?style=social)](https://github.com/Emirhan55-AI/AURA_AI/stargazers)
[![Forks](https://img.shields.io/github/forks/Emirhan55-AI/AURA_AI?style=social)](https://github.com/Emirhan55-AI/AURA_AI/network/members)
[![Issues](https://img.shields.io/github/issues/Emirhan55-AI/AURA_AI)](https://github.com/Emirhan55-AI/AURA_AI/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/Emirhan55-AI/AURA_AI)](https://github.com/Emirhan55-AI/AURA_AI/pulls)

Made with ❤️ by [Emirhan55-AI](https://github.com/Emirhan55-AI)

</div>
