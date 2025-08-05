# 📋 AURA AI - Script Komutları Hızlı Erişim Kılavuzu

Bu dosya AURA AI sisteminin tüm script komutlarını ve kullanım örneklerini içerir.

## 🚀 Ana Script'ler

### 1. 🏗️ Setup Script - `.\scripts\setup.ps1`

**Amaç**: Geliştirme ortamını otomatik olarak kurar

```powershell
# Tam kurulum (önerilen)
.\scripts\setup.ps1 -FullSetup

# Docker olmadan kurulum
.\scripts\setup.ps1 -SkipDocker

# Mevcut kurulumu güncelle
.\scripts\setup.ps1 -Force

# Python 3.10 ile kurulum
.\scripts\setup.ps1 -PythonVersion 3.10

# Yardım
.\scripts\setup.ps1 -Help
```

**Ne yapar**:
- Virtual environment oluşturur
- Python dependencies yükler
- Docker container'ları başlatır
- Database migration yapar
- Environment dosyalarını oluşturur
- Pre-commit hooks kurar
- VS Code ayarlarını yapılandırır

---

### 2. 🚀 Deployment Script - `.\scripts\deploy.ps1`

**Amaç**: Docker Compose ile servisleri yönetir

```powershell
# Servisleri başlat
.\scripts\deploy.ps1 up

# Container'ları yeniden build ederek başlat
.\scripts\deploy.ps1 up -Build

# Servisleri zorla yeniden oluştur
.\scripts\deploy.ps1 up -Force

# Servisleri durdur
.\scripts\deploy.ps1 down

# Volume'ları da silerek durdur
.\scripts\deploy.ps1 down -Force

# Servisleri yeniden başlat
.\scripts\deploy.ps1 restart

# Belirli bir servisi yeniden başlat
.\scripts\deploy.ps1 restart -Service image-processing

# Logları izle
.\scripts\deploy.ps1 logs

# Belirli servisin loglarını izle
.\scripts\deploy.ps1 logs -Service orchestrator

# Servis durumlarını kontrol et
.\scripts\deploy.ps1 status

# Temel API testleri çalıştır
.\scripts\deploy.ps1 test

# Docker sistem temizliği
.\scripts\deploy.ps1 clean

# Yardım
.\scripts\deploy.ps1 -Help
```

**Servis URL'leri** (up komutundan sonra erişilebilir):
- Orchestrator: http://localhost:8007
- Image Processing: http://localhost:8001  
- NLU Service: http://localhost:8002
- Style Profile: http://localhost:8003
- Combination Engine: http://localhost:8004
- Recommendation Engine: http://localhost:8005
- Feedback Loop: http://localhost:8006
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

---

### 3. 🧪 Test Script - `.\scripts\test.ps1`

**Amaç**: Tüm test türlerini çalıştırır ve raporlar

```powershell
# Tüm testleri çalıştır
.\scripts\test.ps1 all

# Unit testleri çalıştır
.\scripts\test.ps1 unit

# Integration testleri çalıştır
.\scripts\test.ps1 integration

# End-to-end testleri çalıştır
.\scripts\test.ps1 e2e

# Performance testleri çalıştır
.\scripts\test.ps1 performance

# AI model testleri çalıştır
.\scripts\test.ps1 ai

# API testleri çalıştır
.\scripts\test.ps1 api

# Belirli bir servisin testlerini çalıştır
.\scripts\test.ps1 unit -Service image-processing

# Coverage raporu ile
.\scripts\test.ps1 unit -Coverage

# Paralel test çalıştırma
.\scripts\test.ps1 all -Parallel

# HTML raporu oluştur
.\scripts\test.ps1 all -OutputFormat html

# Detaylı çıktı
.\scripts\test.ps1 unit -Verbose

# İlk hatada dur
.\scripts\test.ps1 integration -StopOnFail

# Test pattern ile
.\scripts\test.ps1 unit -TestPattern "*auth*"

# Yardım
.\scripts\test.ps1 -Help
```

**Test Kategorileri**:
- `unit`: Birim testler
- `integration`: Entegrasyon testleri
- `e2e`: Uçtan uca testler
- `performance`: Performans testleri
- `ai`: AI model testleri
- `api`: API endpoint testleri

---

### 4. 🔍 Monitoring Script - `.\scripts\monitor.ps1`

**Amaç**: Sistem sağlığını izler ve raporlar

```powershell
# Genel sistem durumu
.\scripts\monitor.ps1 status

# Detaylı durum bilgisi
.\scripts\monitor.ps1 status -Detailed

# Sürekli izleme modu
.\scripts\monitor.ps1 status -Watch

# Belirli bir servisi izle
.\scripts\monitor.ps1 status -Service image-processing

# Detaylı sağlık kontrolü
.\scripts\monitor.ps1 health

# Performance metrikleri
.\scripts\monitor.ps1 metrics

# Container metrikleri detayları
.\scripts\monitor.ps1 metrics -Detailed

# Son logları göster
.\scripts\monitor.ps1 logs

# Belirli servisin logları
.\scripts\monitor.ps1 logs -Service nlu-service

# Performance analizi
.\scripts\monitor.ps1 performance

# Aktif alertleri göster
.\scripts\monitor.ps1 alerts

# Kapsamlı sistem raporu
.\scripts\monitor.ps1 report

# Raporu dosyaya aktar
.\scripts\monitor.ps1 report -Export

# Özel rapor dizini
.\scripts\monitor.ps1 report -OutputPath "./custom-reports"

# Yardım
.\scripts\monitor.ps1 -Help
```

**Monitoring Özellikleri**:
- Servis sağlık durumu
- Container resource kullanımı
- Sistem metrikleri (CPU, Memory, Disk)
- Response time analizi
- Otomatik alert sistemi
- JSON/HTML rapor export

---

## 🔄 Tipik Geliştirme Workflow'u

### İlk Kurulum
```powershell
# 1. Repository'yi klonla
git clone <repository-url>
cd aura-ai

# 2. Geliştirme ortamını kur
.\scripts\setup.ps1 -FullSetup

# 3. Servisleri başlat
.\scripts\deploy.ps1 up -Build

# 4. Sistem durumunu kontrol et
.\scripts\monitor.ps1 status

# 5. Testleri çalıştır
.\scripts\test.ps1 unit
```

### Günlük Geliştirme
```powershell
# Servisleri başlat
.\scripts\deploy.ps1 up

# Kod değişikliklerinden sonra testleri çalıştır
.\scripts\test.ps1 unit -Service your-service

# Servisi yeniden başlat
.\scripts\deploy.ps1 restart -Service your-service

# Logları kontrol et
.\scripts\deploy.ps1 logs -Service your-service

# Performance'ı test et
.\scripts\monitor.ps1 performance -Service your-service
```

### Debug ve Troubleshooting
```powershell
# Sistem durumu kontrolü
.\scripts\monitor.ps1 health

# Tüm logları göster
.\scripts\deploy.ps1 logs

# Container stats kontrol et
.\scripts\monitor.ps1 metrics -Detailed

# Aktif alertleri kontrol et
.\scripts\monitor.ps1 alerts

# Detaylı rapor oluştur
.\scripts\monitor.ps1 report -Export
```

### Test ve Validation
```powershell
# Tüm testleri çalıştır
.\scripts\test.ps1 all -Coverage

# Integration testleri
.\scripts\test.ps1 integration -Verbose

# Performance testleri
.\scripts\test.ps1 performance

# API testleri
.\scripts\test.ps1 api -OutputFormat html
```

---

## 🛠️ Utility Komutları

### Docker Yönetimi
```powershell
# Container'ları listeleme
docker ps

# Logs takip etme
docker logs -f container-name

# Container'a bağlanma
docker exec -it container-name bash

# Docker sistem temizliği
docker system prune -f
```

### Database Yönetimi
```powershell
# Database migration
alembic upgrade head

# Migration oluşturma
alembic revision --autogenerate -m "description"

# Migration geçmişi
alembic history

# Database backup
pg_dump postgresql://user:pass@localhost:5432/db > backup.sql
```

### Virtual Environment
```powershell
# Virtual environment aktifleştir
.\venv\Scripts\Activate.ps1

# Dependencies güncelle
pip install -r requirements.txt

# Yeni dependency ekle
pip install package-name
pip freeze > requirements.txt
```

---

## 🎯 Hızlı Komut Örnekleri

### Development Başlatma
```powershell
.\scripts\setup.ps1 -FullSetup && .\scripts\deploy.ps1 up -Build
```

### Test ve Status Check
```powershell
.\scripts\test.ps1 unit && .\scripts\monitor.ps1 status
```

### Full System Restart
```powershell
.\scripts\deploy.ps1 down -Force && .\scripts\deploy.ps1 up -Build
```

### Comprehensive Health Check
```powershell
.\scripts\monitor.ps1 health && .\scripts\test.ps1 api && .\scripts\monitor.ps1 performance
```

---

## 📊 Monitoring Dashboard URL'leri

| Service | URL | Description |
|---------|-----|-------------|
| **API Documentation** | http://localhost:8007/docs | Swagger UI |
| **Prometheus** | http://localhost:9090 | Metrics collection |
| **Grafana** | http://localhost:3000 | Visualization dashboard |
| **Health Checks** | http://localhost:800X/health | Service health endpoints |

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.env.development` | Development environment variables |
| `.env.test` | Test environment variables |
| `docker-compose.dev.yml` | Development Docker configuration |
| `alembic.ini` | Database migration configuration |
| `pytest.ini` | Test configuration |
| `.vscode/settings.json` | VS Code workspace settings |

---

## 💡 Pro Tips

1. **Sürekli İzleme**: `.\scripts\monitor.ps1 status -Watch` ile real-time monitoring
2. **Hızlı Test**: `.\scripts\test.ps1 unit -Service service-name` ile sadece ilgili servisi test et
3. **Performance Debug**: `.\scripts\monitor.ps1 performance` ile response time'ları analiz et
4. **Log Analizi**: `.\scripts\deploy.ps1 logs -Service service-name` ile spesifik log'ları izle
5. **Export Reports**: Tüm monitoring script'lerinde `-Export` flag'i ile raporları kaydet

Bu kılavuz ile AURA AI sistemini verimli bir şekilde geliştirebilir ve yönetebilirsiniz! 🚀
