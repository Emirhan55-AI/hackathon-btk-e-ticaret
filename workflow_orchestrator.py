# 🚀 AURA AI - WORKFLOW ORCHESTRATION ENGINE (PHASE 7)
# Bu modül, tüm mikroservisleri koordine eden akıllı iş akışı motoru sağlar
# End-to-end fashion AI pipeline'ları ile gerçek zamanlı orkestrasyon yapar

# asyncio - asenkron programlama için temel kütüphane
import asyncio
# aiohttp - asenkron HTTP client işlemleri için
import aiohttp
# json - JSON veri işleme için
import json
# datetime - zaman damgası ve süre hesaplamaları için
from datetime import datetime, timedelta
# typing - type hints için
from typing import Dict, List, Any, Optional, Callable
# dataclasses - veri yapıları için
from dataclasses import dataclass, field
# enum - sabitler için
from enum import Enum
# logging - hata ayıklama ve izleme için
import logging
# uuid - benzersiz kimlik oluşturma için
import uuid
# time - performans ölçümü için
import time
# traceback - hata izleme için
import traceback

# Logging konfigürasyonu - detaylı izleme için
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    """
    İş akışı durumları enum sınıfı.
    Her iş akışının mevcut durumunu takip etmek için kullanılır.
    """
    PENDING = "pending"          # Beklemede - henüz başlamadı
    RUNNING = "running"          # Çalışıyor - aktif olarak işleniyor
    COMPLETED = "completed"      # Tamamlandı - başarıyla bitti
    FAILED = "failed"           # Başarısız - hata ile durdu
    CANCELLED = "cancelled"      # İptal edildi - kullanıcı tarafından durduruldu
    RETRYING = "retrying"       # Yeniden deniyor - hata sonrası tekrar

class ServiceType(Enum):
    """
    Mikroservis tipleri enum sınıfı.
    Her servisin tipini ve özelliklerini tanımlar.
    """
    IMAGE_PROCESSING = "image_processing"        # Görüntü işleme servisi
    NLU = "nlu"                                 # Doğal dil anlama servisi
    STYLE_PROFILE = "style_profile"             # Stil profil servisi
    COMBINATION_ENGINE = "combination_engine"    # Kombinasyon motor servisi
    RECOMMENDATION_ENGINE = "recommendation_engine"  # Öneri motor servisi

@dataclass
class WorkflowStep:
    """
    Tek bir iş akışı adımını temsil eden veri sınıfı.
    Her adım bir mikroservise karşılık gelir ve bağımlılıkları vardır.
    """
    step_id: str                    # Adım benzersiz kimliği
    service_type: ServiceType       # Hangi mikroservise karşılık geldiği
    endpoint: str                   # Servisin çağrılacak endpoint'i
    dependencies: List[str] = field(default_factory=list)  # Önce tamamlanması gereken adımlar
    timeout: float = 30.0           # Maximum bekleme süresi (saniye)
    retry_count: int = 3            # Hata durumunda kaç kez yeniden denenecek
    required: bool = True           # Bu adım zorunlu mu yoksa opsiyonel mi
    fallback_enabled: bool = True   # Hata durumunda fallback mekanizması var mı

@dataclass
class WorkflowDefinition:
    """
    Tam bir iş akışı tanımını içeren veri sınıfı.
    Adımlar, bağımlılıklar ve konfigürasyon bilgilerini tutar.
    """
    workflow_id: str                # İş akışı benzersiz kimliği
    name: str                      # İş akışı açıklayıcı ismi
    description: str               # Detaylı açıklama
    steps: List[WorkflowStep]      # İş akışını oluşturan adımlar listesi
    max_execution_time: float = 300.0  # Maximum toplam çalışma süresi (saniye)
    parallel_execution: bool = True     # Adımlar paralel çalıştırılabilir mi
    error_policy: str = "continue"      # Hata durumunda politika: "stop", "continue", "retry"

@dataclass
class WorkflowContext:
    """
    İş akışı çalışma zamanı bağlam bilgilerini tutan sınıf.
    Kullanıcı verisi, geçici sonuçlar ve metadata burada saklanır.
    """
    user_id: str                   # İş akışını başlatan kullanıcı kimliği
    session_id: str                # Oturum kimliği
    input_data: Dict[str, Any]     # Başlangıç input verileri
    context_data: Dict[str, Any] = field(default_factory=dict)  # Bağlamsal veriler
    step_results: Dict[str, Any] = field(default_factory=dict)  # Her adımın sonuçları
    metadata: Dict[str, Any] = field(default_factory=dict)      # Ek metadata bilgileri

@dataclass
class WorkflowExecution:
    """
    Çalışan bir iş akışının durumunu ve sonuçlarını tutan sınıf.
    Runtime bilgileri, performans metrikleri ve sonuçları içerir.
    """
    execution_id: str              # Çalıştırma benzersiz kimliği
    workflow_id: str               # Hangi iş akışının çalıştırıldığı
    status: WorkflowStatus         # Mevcut durum
    context: WorkflowContext       # Çalışma zamanı bağlamı
    start_time: datetime           # Başlangıç zamanı
    end_time: Optional[datetime] = None         # Bitiş zamanı
    current_step: Optional[str] = None          # Şu an çalışan adım
    completed_steps: List[str] = field(default_factory=list)  # Tamamlanan adımlar
    failed_steps: List[str] = field(default_factory=list)     # Başarısız adımlar
    error_messages: List[str] = field(default_factory=list)   # Hata mesajları
    performance_metrics: Dict[str, Any] = field(default_factory=dict)  # Performans metrikleri

class AuraWorkflowOrchestrator:
    """
    Aura AI Workflow Orchestration Engine - Ana orkestrasyon motoru.
    
    Bu sınıf tüm mikroservisleri koordine eder ve akıllı iş akışları yönetir.
    End-to-end fashion AI pipeline'larını gerçek zamanlı olarak çalıştırır.
    """
    
    def __init__(self):
        # Mikroservis URL'lerini tanımla - her servisin base URL'si
        self.service_urls = {
            ServiceType.IMAGE_PROCESSING: "http://localhost:8001",
            ServiceType.NLU: "http://localhost:8002", 
            ServiceType.STYLE_PROFILE: "http://localhost:8003",
            ServiceType.COMBINATION_ENGINE: "http://localhost:8004",
            ServiceType.RECOMMENDATION_ENGINE: "http://localhost:8005"
        }
        
        # Öntanımlı iş akışı şablonlarını yükle
        self.workflow_definitions = {}
        self._initialize_standard_workflows()
        
        # Aktif çalışan iş akışlarını takip et
        self.active_executions: Dict[str, WorkflowExecution] = {}
        
        # Circuit breaker pattern için servis sağlık durumları
        self.service_health = {service: True for service in ServiceType}
        
        # Performans metrikleri için sayaçlar
        self.metrics = {
            "total_workflows": 0,           # Toplam çalıştırılan iş akışı sayısı
            "successful_workflows": 0,      # Başarılı iş akışı sayısı
            "failed_workflows": 0,          # Başarısız iş akışı sayısı
            "average_execution_time": 0.0,  # Ortalama çalışma süresi
            "service_call_count": {service: 0 for service in ServiceType},  # Her servise yapılan çağrı sayısı
            "service_error_count": {service: 0 for service in ServiceType}  # Her serviste oluşan hata sayısı
        }
        
        logger.info("🚀 Aura Workflow Orchestrator initialized successfully!")
    
    def _initialize_standard_workflows(self):
        """
        Standart iş akışı şablonlarını başlat.
        En sık kullanılan fashion AI workflow'larını öntanımlı olarak oluşturur.
        """
        
        # 1. Complete Fashion Analysis Workflow - Tam moda analizi
        complete_analysis_steps = [
            WorkflowStep(
                step_id="image_analysis",
                service_type=ServiceType.IMAGE_PROCESSING,
                endpoint="/analyze_image_advanced",
                dependencies=[],  # İlk adım, bağımlılık yok
                timeout=15.0,
                retry_count=2
            ),
            WorkflowStep(
                step_id="text_understanding", 
                service_type=ServiceType.NLU,
                endpoint="/analyze_text_advanced",
                dependencies=[],  # Paralel çalışabilir
                timeout=10.0,
                retry_count=2
            ),
            WorkflowStep(
                step_id="style_profiling",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint="/analyze_style_advanced",
                dependencies=["image_analysis", "text_understanding"],  # Her ikisine de bağımlı
                timeout=12.0,
                retry_count=2
            ),
            WorkflowStep(
                step_id="combination_generation",
                service_type=ServiceType.COMBINATION_ENGINE,
                endpoint="/generate_combination_advanced",
                dependencies=["style_profiling"],
                timeout=8.0,
                retry_count=2
            ),
            WorkflowStep(
                step_id="personalized_recommendations",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/recommendations_advanced",
                dependencies=["combination_generation"],
                timeout=10.0,
                retry_count=2
            )
        ]
        
        self.workflow_definitions["complete_fashion_analysis"] = WorkflowDefinition(
            workflow_id="complete_fashion_analysis",
            name="Complete Fashion Analysis",
            description="End-to-end fashion analysis: image → style → combinations → recommendations",
            steps=complete_analysis_steps,
            max_execution_time=120.0,  # 2 dakika max
            parallel_execution=True,
            error_policy="continue"
        )
        
        # 2. Quick Style Assessment Workflow - Hızlı stil değerlendirmesi
        quick_style_steps = [
            WorkflowStep(
                step_id="quick_image_scan",
                service_type=ServiceType.IMAGE_PROCESSING,
                endpoint="/quick_analysis",
                timeout=5.0,
                retry_count=1
            ),
            WorkflowStep(
                step_id="style_classification",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint="/classify_style",
                dependencies=["quick_image_scan"],
                timeout=3.0,
                retry_count=1
            ),
            WorkflowStep(
                step_id="instant_recommendations",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/quick_recommendations",
                dependencies=["style_classification"],
                timeout=4.0,
                retry_count=1
            )
        ]
        
        self.workflow_definitions["quick_style_assessment"] = WorkflowDefinition(
            workflow_id="quick_style_assessment",
            name="Quick Style Assessment",
            description="Fast style analysis for immediate recommendations",
            steps=quick_style_steps,
            max_execution_time=30.0,  # 30 saniye max
            parallel_execution=False,  # Sıralı çalışsın, hız için
            error_policy="stop"
        )
        
        # 3. User Onboarding Workflow - Kullanıcı kayıt süreci
        onboarding_steps = [
            WorkflowStep(
                step_id="preference_analysis",
                service_type=ServiceType.NLU,
                endpoint="/analyze_preferences",
                timeout=8.0
            ),
            WorkflowStep(
                step_id="initial_profile_creation",
                service_type=ServiceType.STYLE_PROFILE,
                endpoint="/create_profile",
                dependencies=["preference_analysis"],
                timeout=10.0
            ),
            WorkflowStep(
                step_id="welcome_recommendations",
                service_type=ServiceType.RECOMMENDATION_ENGINE,
                endpoint="/welcome_recommendations",
                dependencies=["initial_profile_creation"],
                timeout=12.0
            )
        ]
        
        self.workflow_definitions["user_onboarding"] = WorkflowDefinition(
            workflow_id="user_onboarding",
            name="User Onboarding",
            description="New user onboarding with initial style profiling",
            steps=onboarding_steps,
            max_execution_time=60.0,
            parallel_execution=False,
            error_policy="retry"
        )
        
        logger.info(f"✅ Initialized {len(self.workflow_definitions)} standard workflows")
    
    async def execute_workflow(self, workflow_id: str, context: WorkflowContext) -> WorkflowExecution:
        """
        Belirtilen iş akışını çalıştır.
        
        Args:
            workflow_id: Çalıştırılacak iş akışının kimliği
            context: İş akışı bağlam bilgileri
            
        Returns:
            WorkflowExecution: Çalıştırma durumu ve sonuçları
        """
        
        # İş akışı tanımını bul
        if workflow_id not in self.workflow_definitions:
            raise ValueError(f"Workflow '{workflow_id}' not found")
        
        workflow_def = self.workflow_definitions[workflow_id]
        
        # Yeni çalıştırma instance'ı oluştur
        execution_id = str(uuid.uuid4())
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            context=context,
            start_time=datetime.now()
        )
        
        # Aktif çalıştırmalar listesine ekle
        self.active_executions[execution_id] = execution
        
        logger.info(f"🚀 Starting workflow '{workflow_def.name}' (ID: {execution_id})")
        
        try:
            # İş akışını çalıştır
            execution.status = WorkflowStatus.RUNNING
            await self._execute_workflow_steps(workflow_def, execution)
            
            # Başarıyla tamamlandı
            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = datetime.now()
            
            # Metrikleri güncelle
            self._update_metrics(execution, success=True)
            
            logger.info(f"✅ Workflow '{workflow_def.name}' completed successfully in {self._get_execution_duration(execution):.2f}s")
            
        except Exception as e:
            # Hata durumunda
            execution.status = WorkflowStatus.FAILED
            execution.end_time = datetime.now()
            execution.error_messages.append(str(e))
            
            # Metrikleri güncelle
            self._update_metrics(execution, success=False)
            
            logger.error(f"❌ Workflow '{workflow_def.name}' failed: {str(e)}")
            logger.error(f"🔍 Traceback: {traceback.format_exc()}")
        
        finally:
            # Temizlik işlemleri
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]
        
        return execution
    
    async def _execute_workflow_steps(self, workflow_def: WorkflowDefinition, execution: WorkflowExecution):
        """
        İş akışı adımlarını sırayla veya paralel olarak çalıştır.
        
        Args:
            workflow_def: İş akışı tanımı
            execution: Çalıştırma durumu
        """
        
        # Adımları bağımlılık sırasına göre grupla
        step_groups = self._organize_steps_by_dependencies(workflow_def.steps)
        
        # Her grup sırasıyla, grup içindeki adımlar paralel çalıştırılır
        for group_index, step_group in enumerate(step_groups):
            logger.info(f"🔄 Executing step group {group_index + 1}/{len(step_groups)} with {len(step_group)} steps")
            
            # Grup içindeki adımları paralel çalıştır
            if workflow_def.parallel_execution and len(step_group) > 1:
                # Paralel çalıştırma
                tasks = []
                for step in step_group:
                    task = asyncio.create_task(self._execute_single_step(step, execution))
                    tasks.append(task)
                
                # Tüm adımların tamamlanmasını bekle
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Sonuçları kontrol et
                for i, result in enumerate(results):
                    step = step_group[i]
                    if isinstance(result, Exception):
                        execution.failed_steps.append(step.step_id)
                        execution.error_messages.append(f"Step '{step.step_id}' failed: {str(result)}")
                        
                        if step.required and workflow_def.error_policy == "stop":
                            raise result
                    else:
                        execution.completed_steps.append(step.step_id)
            else:
                # Sıralı çalıştırma
                for step in step_group:
                    try:
                        result = await self._execute_single_step(step, execution)
                        execution.completed_steps.append(step.step_id)
                        
                    except Exception as e:
                        execution.failed_steps.append(step.step_id)
                        execution.error_messages.append(f"Step '{step.step_id}' failed: {str(e)}")
                        
                        if step.required and workflow_def.error_policy == "stop":
                            raise e
    
    def _organize_steps_by_dependencies(self, steps: List[WorkflowStep]) -> List[List[WorkflowStep]]:
        """
        Adımları bağımlılık sırasına göre gruplandır.
        Her grupta bulunan adımlar paralel çalıştırılabilir.
        
        Args:
            steps: İş akışı adımları listesi
            
        Returns:
            List[List[WorkflowStep]]: Bağımlılık sırasına göre gruplandırılmış adımlar
        """
        
        # Adımları ID'lerine göre mapple
        step_map = {step.step_id: step for step in steps}
        
        # Grupları tutacak liste
        step_groups = []
        completed_steps = set()
        
        # Tüm adımlar tamamlanana kadar devam et
        while len(completed_steps) < len(steps):
            # Bu iterasyonda çalıştırılabilecek adımları bul
            ready_steps = []
            
            for step in steps:
                # Zaten tamamlanmış adımları atla
                if step.step_id in completed_steps:
                    continue
                
                # Bağımlılıkları kontrol et
                dependencies_met = all(dep in completed_steps for dep in step.dependencies)
                
                if dependencies_met:
                    ready_steps.append(step)
            
            # Hazır adımlar yoksa sonsuz döngü var demektir
            if not ready_steps:
                remaining_steps = [s.step_id for s in steps if s.step_id not in completed_steps]
                raise ValueError(f"Circular dependency detected in steps: {remaining_steps}")
            
            # Hazır adımları gruba ekle
            step_groups.append(ready_steps)
            
            # Bu adımları tamamlanmış olarak işaretle
            for step in ready_steps:
                completed_steps.add(step.step_id)
        
        return step_groups
    
    async def _execute_single_step(self, step: WorkflowStep, execution: WorkflowExecution) -> Dict[str, Any]:
        """
        Tek bir iş akışı adımını çalıştır.
        
        Args:
            step: Çalıştırılacak adım
            execution: İş akışı çalıştırma durumu
            
        Returns:
            Dict[str, Any]: Adım sonucu
        """
        
        execution.current_step = step.step_id
        step_start_time = time.time()
        
        logger.info(f"🔄 Executing step '{step.step_id}' on service '{step.service_type.value}'")
        
        # Servis sağlık durumunu kontrol et (Circuit Breaker Pattern)
        if not self.service_health.get(step.service_type, True):
            if step.fallback_enabled:
                logger.warning(f"⚠️ Service '{step.service_type.value}' is unhealthy, using fallback")
                return await self._execute_fallback_step(step, execution)
            else:
                raise Exception(f"Service '{step.service_type.value}' is unhealthy and no fallback available")
        
        # Retry mekanizması ile adımı çalıştır
        last_exception = None
        for attempt in range(step.retry_count + 1):
            try:
                # Servis URL'sini oluştur
                service_url = self.service_urls[step.service_type]
                full_url = f"{service_url}{step.endpoint}"
                
                # Request payload'unu hazırla
                payload = self._prepare_step_payload(step, execution)
                
                # HTTP isteği gönder
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        full_url,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=step.timeout)
                    ) as response:
                        
                        if response.status == 200:
                            result = await response.json()
                            
                            # Sonucu execution context'e ekle
                            execution.context.step_results[step.step_id] = result
                            
                            # Performans metriklerini güncelle
                            step_duration = time.time() - step_start_time
                            execution.performance_metrics[f"{step.step_id}_duration"] = step_duration
                            
                            # Servis call count'ı artır
                            self.metrics["service_call_count"][step.service_type] += 1
                            
                            # Servis sağlıklı olarak işaretle
                            self.service_health[step.service_type] = True
                            
                            logger.info(f"✅ Step '{step.step_id}' completed in {step_duration:.2f}s")
                            return result
                        
                        else:
                            error_msg = f"HTTP {response.status}: {await response.text()}"
                            raise Exception(error_msg)
                
            except Exception as e:
                last_exception = e
                
                # Hata sayacını artır
                self.metrics["service_error_count"][step.service_type] += 1
                
                # Son deneme değilse retry yap
                if attempt < step.retry_count:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"⚠️ Step '{step.step_id}' attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}")
                    await asyncio.sleep(wait_time)
                else:
                    # Tüm denemeler başarısız
                    logger.error(f"❌ Step '{step.step_id}' failed after {step.retry_count + 1} attempts: {str(e)}")
                    
                    # Servis sağlıksız olarak işaretle
                    self.service_health[step.service_type] = False
                    
                    # Fallback varsa kullan
                    if step.fallback_enabled:
                        logger.info(f"🔄 Using fallback for step '{step.step_id}'")
                        return await self._execute_fallback_step(step, execution)
        
        # Tüm denemeler ve fallback başarısız
        raise last_exception
    
    def _prepare_step_payload(self, step: WorkflowStep, execution: WorkflowExecution) -> Dict[str, Any]:
        """
        Adım için HTTP request payload'unu hazırla.
        
        Args:
            step: Çalıştırılacak adım
            execution: İş akışı çalıştırma durumu
            
        Returns:
            Dict[str, Any]: Request payload
        """
        
        # Base payload with context
        payload = {
            "user_id": execution.context.user_id,
            "session_id": execution.context.session_id,
            "workflow_id": execution.workflow_id,
            "execution_id": execution.execution_id,
            "step_id": step.step_id
        }
        
        # Input data'yı ekle
        payload.update(execution.context.input_data)
        
        # Önceki adımların sonuçlarını ekle
        payload["previous_results"] = execution.context.step_results
        
        # Context data'yı ekle
        payload["context_data"] = execution.context.context_data
        
        return payload
    
    async def _execute_fallback_step(self, step: WorkflowStep, execution: WorkflowExecution) -> Dict[str, Any]:
        """
        Adım başarısız olduğunda fallback mekanizmasını çalıştır.
        
        Args:
            step: Başarısız olan adım
            execution: İş akışı çalıştırma durumu
            
        Returns:
            Dict[str, Any]: Fallback sonucu
        """
        
        logger.info(f"🔄 Executing fallback for step '{step.step_id}'")
        
        # Service type'a göre basit fallback sonuçları üret
        fallback_results = {
            ServiceType.IMAGE_PROCESSING: {
                "status": "fallback",
                "analysis": {
                    "items_detected": ["generic_clothing_item"],
                    "colors": ["neutral"],
                    "style": "casual",
                    "confidence": 0.5
                },
                "message": "Using fallback image analysis due to service unavailability"
            },
            
            ServiceType.NLU: {
                "status": "fallback", 
                "analysis": {
                    "intent": "general_fashion_query",
                    "entities": ["clothing", "style"],
                    "sentiment": "neutral",
                    "confidence": 0.5
                },
                "message": "Using fallback text analysis due to service unavailability"
            },
            
            ServiceType.STYLE_PROFILE: {
                "status": "fallback",
                "style_profile": {
                    "style_category": "casual",
                    "preferences": ["comfortable", "versatile"],
                    "recommendations": "general_style_advice",
                    "confidence": 0.5
                },
                "message": "Using fallback style profiling due to service unavailability"
            },
            
            ServiceType.COMBINATION_ENGINE: {
                "status": "fallback",
                "combination": {
                    "items": ["basic_top", "basic_bottom"],
                    "style": "casual",
                    "occasion": "everyday",
                    "confidence": 0.5
                },
                "message": "Using fallback combination generation due to service unavailability"
            },
            
            ServiceType.RECOMMENDATION_ENGINE: {
                "status": "fallback",
                "recommendations": [
                    {"item": "versatile_piece_1", "score": 0.7, "reason": "fallback_recommendation"},
                    {"item": "versatile_piece_2", "score": 0.6, "reason": "fallback_recommendation"}
                ],
                "message": "Using fallback recommendations due to service unavailability"
            }
        }
        
        result = fallback_results.get(step.service_type, {
            "status": "fallback",
            "message": f"Generic fallback for {step.service_type.value}",
            "confidence": 0.3
        })
        
        # Sonucu execution context'e ekle
        execution.context.step_results[step.step_id] = result
        
        return result
    
    def _update_metrics(self, execution: WorkflowExecution, success: bool):
        """
        İş akışı tamamlandıktan sonra metrikleri güncelle.
        
        Args:
            execution: Tamamlanan iş akışı çalıştırması
            success: Başarılı mı başarısız mı
        """
        
        self.metrics["total_workflows"] += 1
        
        if success:
            self.metrics["successful_workflows"] += 1
        else:
            self.metrics["failed_workflows"] += 1
        
        # Ortalama çalışma süresini güncelle
        duration = self._get_execution_duration(execution)
        current_avg = self.metrics["average_execution_time"]
        total_count = self.metrics["total_workflows"]
        
        self.metrics["average_execution_time"] = (
            (current_avg * (total_count - 1) + duration) / total_count
        )
    
    def _get_execution_duration(self, execution: WorkflowExecution) -> float:
        """
        İş akışı çalışma süresini hesapla.
        
        Args:
            execution: İş akışı çalıştırması
            
        Returns:
            float: Süre (saniye)
        """
        if execution.end_time:
            return (execution.end_time - execution.start_time).total_seconds()
        else:
            return (datetime.now() - execution.start_time).total_seconds()
    
    def get_workflow_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """
        Çalışan bir iş akışının durumunu getir.
        
        Args:
            execution_id: İş akışı çalıştırma kimliği
            
        Returns:
            Optional[WorkflowExecution]: İş akışı durumu veya None
        """
        return self.active_executions.get(execution_id)
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Orkestratör performans metriklerini getir.
        
        Returns:
            Dict[str, Any]: Detaylı metrik bilgileri
        """
        return {
            "orchestrator_metrics": self.metrics.copy(),
            "service_health": self.service_health.copy(),
            "active_executions": len(self.active_executions),
            "available_workflows": list(self.workflow_definitions.keys())
        }
    
    def register_workflow(self, workflow_def: WorkflowDefinition):
        """
        Yeni bir iş akışı tanımı kaydet.
        
        Args:
            workflow_def: İş akışı tanımı
        """
        self.workflow_definitions[workflow_def.workflow_id] = workflow_def
        logger.info(f"✅ Registered workflow '{workflow_def.name}' (ID: {workflow_def.workflow_id})")
    
    async def cancel_workflow(self, execution_id: str) -> bool:
        """
        Çalışan bir iş akışını iptal et.
        
        Args:
            execution_id: İptal edilecek iş akışı kimliği
            
        Returns:
            bool: İptal başarılı mı
        """
        if execution_id in self.active_executions:
            execution = self.active_executions[execution_id]
            execution.status = WorkflowStatus.CANCELLED
            execution.end_time = datetime.now()
            
            # Aktif listeden çıkar
            del self.active_executions[execution_id]
            
            logger.info(f"🚫 Workflow {execution_id} cancelled successfully")
            return True
        
        return False

# Global orchestrator instance - singleton pattern
aura_orchestrator = AuraWorkflowOrchestrator()

# Kolay kullanım için helper fonksiyonlar
async def execute_complete_fashion_analysis(user_id: str, image_data: Any, text_query: str) -> WorkflowExecution:
    """
    Tam moda analizi iş akışını çalıştır.
    
    Args:
        user_id: Kullanıcı kimliği
        image_data: Görüntü verisi
        text_query: Metin sorgusu
        
    Returns:
        WorkflowExecution: İş akışı sonucu
    """
    context = WorkflowContext(
        user_id=user_id,
        session_id=str(uuid.uuid4()),
        input_data={
            "image": image_data,
            "text": text_query,
            "analysis_type": "comprehensive"
        }
    )
    
    return await aura_orchestrator.execute_workflow("complete_fashion_analysis", context)

async def execute_quick_style_assessment(user_id: str, image_data: Any) -> WorkflowExecution:
    """
    Hızlı stil değerlendirmesi iş akışını çalıştır.
    
    Args:
        user_id: Kullanıcı kimliği
        image_data: Görüntü verisi
        
    Returns:
        WorkflowExecution: İş akışı sonucu
    """
    context = WorkflowContext(
        user_id=user_id,
        session_id=str(uuid.uuid4()),
        input_data={
            "image": image_data,
            "analysis_type": "quick"
        }
    )
    
    return await aura_orchestrator.execute_workflow("quick_style_assessment", context)

# Test fonksiyonu
async def test_orchestrator():
    """
    Orchestrator'ın temel işlevlerini test et.
    """
    logger.info("🧪 Testing Aura Workflow Orchestrator...")
    
    # Test context'i oluştur
    test_context = WorkflowContext(
        user_id="test_user_123",
        session_id="test_session_456",
        input_data={
            "text": "I need a casual outfit for weekend",
            "image": "test_image_data",
            "analysis_type": "comprehensive"
        }
    )
    
    # Test iş akışını çalıştır
    try:
        result = await aura_orchestrator.execute_workflow("complete_fashion_analysis", test_context)
        logger.info(f"✅ Test workflow completed with status: {result.status}")
        logger.info(f"📊 Execution took {aura_orchestrator._get_execution_duration(result):.2f} seconds")
        
        # Metrikleri göster
        metrics = aura_orchestrator.get_metrics()
        logger.info(f"📈 Orchestrator metrics: {metrics}")
        
    except Exception as e:
        logger.error(f"❌ Test workflow failed: {str(e)}")

if __name__ == "__main__":
    # Test çalıştır
    asyncio.run(test_orchestrator())
