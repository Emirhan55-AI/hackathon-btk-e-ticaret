# 🚀 AURA AI - SERVICE CHOREOGRAPHY MANAGER (PHASE 7)
# Bu modül, mikroservisler arası koordinasyonu ve event-driven iletişimi yönetir
# Servisler arası veri akışı, state management ve transaction consistency sağlar

# asyncio - asenkron programlama için
import asyncio
# aioredis - Redis ile asenkron iletişim için
import aioredis
# json - JSON veri işleme için
import json
# datetime - zaman damgası işlemleri için
from datetime import datetime, timedelta
# typing - type hints için
from typing import Dict, List, Any, Optional, Callable, Set
# dataclasses - veri yapıları için
from dataclasses import dataclass, field
# enum - sabitler için
from enum import Enum
# logging - hata ayıklama ve izleme için
import logging
# uuid - benzersiz kimlik oluşturma için
import uuid
# asyncio - event loop yönetimi için
from asyncio import Queue
# traceback - hata izleme için
import traceback

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EventType(Enum):
    """
    Sistem event tiplerini tanımlayan enum sınıfı.
    Servisler arası iletişimde kullanılan event kategorileri.
    """
    SERVICE_REQUEST = "service_request"           # Servis isteği eventi
    SERVICE_RESPONSE = "service_response"         # Servis yanıt eventi
    SERVICE_ERROR = "service_error"               # Servis hata eventi
    WORKFLOW_STARTED = "workflow_started"         # İş akışı başladı eventi
    WORKFLOW_COMPLETED = "workflow_completed"     # İş akışı tamamlandı eventi
    WORKFLOW_FAILED = "workflow_failed"           # İş akışı başarısız eventi
    DATA_UPDATED = "data_updated"                 # Veri güncellendi eventi
    SYSTEM_HEALTH_CHECK = "system_health_check"   # Sistem sağlık kontrolü eventi

class TransactionStatus(Enum):
    """
    Distributed transaction durumlarını tanımlayan enum.
    Mikroservisler arası transaction consistency için kullanılır.
    """
    PENDING = "pending"           # Beklemede - henüz başlamadı
    PREPARING = "preparing"       # Hazırlanıyor - servisler hazırlanıyor
    PREPARED = "prepared"         # Hazır - tüm servisler hazır
    COMMITTING = "committing"     # Commit ediliyor - değişiklikler uygulanıyor
    COMMITTED = "committed"       # Commit edildi - başarıyla tamamlandı
    ABORTING = "aborting"        # İptal ediliyor - geri alınıyor
    ABORTED = "aborted"          # İptal edildi - geri alındı

@dataclass
class ServiceEvent:
    """
    Servisler arası iletişimde kullanılan event veri yapısı.
    Her event'in tipi, verisi ve metadata bilgileri burada tutulur.
    """
    event_id: str                 # Event benzersiz kimliği
    event_type: EventType         # Event tipi
    source_service: str           # Event'i gönderen servis
    target_service: Optional[str] # Hedef servis (broadcast için None)
    payload: Dict[str, Any]       # Event verisi
    correlation_id: str           # İlişkili işlem kimliği
    timestamp: datetime = field(default_factory=datetime.now)  # Event zamanı
    ttl: int = 300               # Time to live (saniye)
    retry_count: int = 0         # Yeniden deneme sayısı
    metadata: Dict[str, Any] = field(default_factory=dict)    # Ek metadata

@dataclass
class TransactionContext:
    """
    Distributed transaction bağlam bilgilerini tutan veri yapısı.
    Two-Phase Commit protokolü için gerekli bilgileri içerir.
    """
    transaction_id: str           # Transaction benzersiz kimliği
    coordinator_service: str      # Koordinatör servis
    participants: List[str]       # Katılımcı servisler
    status: TransactionStatus     # Mevcut durum
    operations: Dict[str, Any]    # Her serviste yapılacak işlemler
    start_time: datetime = field(default_factory=datetime.now)  # Başlangıç zamanı
    timeout: int = 60            # Timeout (saniye)
    compensation_actions: Dict[str, Any] = field(default_factory=dict)  # Rollback işlemleri

class ServiceChoreographyManager:
    """
    Service Choreography Manager - Mikroservisler arası koordinasyon motoru.
    
    Bu sınıf mikroservisler arasında event-driven iletişim, distributed transactions
    ve state management sağlar. Choreography pattern ile servisler kendi aralarında
    koordine olurlar, merkezi orchestration'a ihtiyaç duymadan.
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Redis bağlantısı - event store ve message queue için kullanılır
        self.redis_url = redis_url
        self.redis_client = None
        
        # Event subscriptions - hangi servisin hangi event'leri dinlediği
        self.event_subscriptions: Dict[str, Set[EventType]] = {}
        
        # Event handlers - event tipine göre handler fonksiyonları
        self.event_handlers: Dict[EventType, List[Callable]] = {}
        
        # Active transactions - şu an devam eden transaction'lar
        self.active_transactions: Dict[str, TransactionContext] = {}
        
        # Service states - her servisin mevcut durumu
        self.service_states: Dict[str, Dict[str, Any]] = {}
        
        # Event queues - her servis için event kuyruğu
        self.service_queues: Dict[str, Queue] = {}
        
        # Performance metrics - sistem performans metrikleri
        self.metrics = {
            "total_events": 0,              # Toplam işlenen event sayısı
            "successful_events": 0,         # Başarıyla işlenen event sayısı
            "failed_events": 0,             # Başarısız event sayısı
            "active_transactions": 0,       # Aktif transaction sayısı
            "successful_transactions": 0,   # Başarılı transaction sayısı
            "failed_transactions": 0,       # Başarısız transaction sayısı
            "average_event_processing_time": 0.0,  # Ortalama event işleme süresi
            "service_communication_count": {}       # Servisler arası iletişim sayısı
        }
        
        # Event processing tasks - background tasks
        self.event_processing_tasks = []
        
        logger.info("🎭 Service Choreography Manager initialized")
    
    async def initialize(self):
        """
        Manager'ı başlat - Redis bağlantısı kur ve background tasks'ları başlat.
        """
        try:
            # Redis bağlantısını kur
            self.redis_client = await aioredis.from_url(self.redis_url, decode_responses=True)
            await self.redis_client.ping()  # Bağlantıyı test et
            
            logger.info("✅ Redis connection established")
            
            # Background event processing task'ını başlat
            self.event_processing_tasks.append(
                asyncio.create_task(self._process_events_background())
            )
            
            # Transaction timeout checker task'ını başlat
            self.event_processing_tasks.append(
                asyncio.create_task(self._check_transaction_timeouts())
            )
            
            logger.info("🚀 Service Choreography Manager started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Service Choreography Manager: {str(e)}")
            raise
    
    async def shutdown(self):
        """
        Manager'ı kapat - bağlantıları sonlandır ve tasks'ları temizle.
        """
        # Background tasks'ları iptal et
        for task in self.event_processing_tasks:
            task.cancel()
        
        # Redis bağlantısını kapat
        if self.redis_client:
            await self.redis_client.close()
        
        logger.info("🛑 Service Choreography Manager shutdown completed")
    
    def register_service(self, service_name: str, event_types: List[EventType]):
        """
        Bir servisi event subscription'larıyla birlikte kaydet.
        
        Args:
            service_name: Servis adı
            event_types: Dinlenecek event tipleri
        """
        self.event_subscriptions[service_name] = set(event_types)
        self.service_queues[service_name] = Queue()
        self.service_states[service_name] = {"status": "active", "last_seen": datetime.now()}
        
        # İletişim sayacını başlat
        if service_name not in self.metrics["service_communication_count"]:
            self.metrics["service_communication_count"][service_name] = 0
        
        logger.info(f"📝 Registered service '{service_name}' with {len(event_types)} event subscriptions")
    
    def register_event_handler(self, event_type: EventType, handler: Callable):
        """
        Belirli bir event tipi için handler fonksiyonu kaydet.
        
        Args:
            event_type: Event tipi
            handler: Handler fonksiyonu
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
        logger.info(f"🔧 Registered handler for event type '{event_type.value}'")
    
    async def publish_event(self, event: ServiceEvent):
        """
        Yeni bir event yayınla - tüm ilgili servislere dağıt.
        
        Args:
            event: Yayınlanacak event
        """
        try:
            # Event'i Redis'e kaydet (persistence için)
            await self._store_event_in_redis(event)
            
            # Metrics'i güncelle
            self.metrics["total_events"] += 1
            
            # Event'i ilgili servislere dağıt
            if event.target_service:
                # Specific target service
                if event.target_service in self.service_queues:
                    await self.service_queues[event.target_service].put(event)
                    self.metrics["service_communication_count"][event.target_service] += 1
            else:
                # Broadcast to all subscribed services
                for service_name, subscribed_events in self.event_subscriptions.items():
                    if event.event_type in subscribed_events:
                        await self.service_queues[service_name].put(event)
                        self.metrics["service_communication_count"][service_name] += 1
            
            logger.info(f"📢 Published event '{event.event_type.value}' from '{event.source_service}'")
            
        except Exception as e:
            self.metrics["failed_events"] += 1
            logger.error(f"❌ Failed to publish event: {str(e)}")
            raise
    
    async def _store_event_in_redis(self, event: ServiceEvent):
        """
        Event'i Redis'e kalıcı olarak kaydet.
        
        Args:
            event: Kaydedilecek event
        """
        if self.redis_client:
            event_data = {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "source_service": event.source_service,
                "target_service": event.target_service,
                "payload": event.payload,
                "correlation_id": event.correlation_id,
                "timestamp": event.timestamp.isoformat(),
                "ttl": event.ttl,
                "retry_count": event.retry_count,
                "metadata": event.metadata
            }
            
            # Event'i hash olarak kaydet
            await self.redis_client.hset(f"event:{event.event_id}", mapping=event_data)
            
            # TTL ayarla
            await self.redis_client.expire(f"event:{event.event_id}", event.ttl)
            
            # Event stream'e ekle
            await self.redis_client.xadd("events_stream", event_data)
    
    async def _process_events_background(self):
        """
        Background task - event'leri sürekli işle.
        """
        logger.info("🔄 Started background event processing")
        
        while True:
            try:
                # Her serviste bekleyen event'leri işle
                for service_name, queue in self.service_queues.items():
                    if not queue.empty():
                        try:
                            # Queue'dan event al
                            event = await asyncio.wait_for(queue.get(), timeout=0.1)
                            
                            # Event'i işle
                            await self._process_single_event(event, service_name)
                            
                        except asyncio.TimeoutError:
                            continue  # Queue boş, devam et
                        except Exception as e:
                            logger.error(f"❌ Error processing event for service '{service_name}': {str(e)}")
                
                # Kısa bekleme
                await asyncio.sleep(0.01)
                
            except Exception as e:
                logger.error(f"❌ Background event processing error: {str(e)}")
                await asyncio.sleep(1)  # Hata durumunda biraz daha bekle
    
    async def _process_single_event(self, event: ServiceEvent, target_service: str):
        """
        Tek bir event'i işle.
        
        Args:
            event: İşlenecek event
            target_service: Hedef servis
        """
        start_time = datetime.now()
        
        try:
            # Event handler'ları çalıştır
            if event.event_type in self.event_handlers:
                for handler in self.event_handlers[event.event_type]:
                    try:
                        await handler(event, target_service)
                    except Exception as e:
                        logger.error(f"❌ Event handler error: {str(e)}")
            
            # Servis state'ini güncelle
            if target_service in self.service_states:
                self.service_states[target_service]["last_seen"] = datetime.now()
            
            # Başarılı işleme
            self.metrics["successful_events"] += 1
            
            # İşleme süresini hesapla
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_average_processing_time(processing_time)
            
            logger.debug(f"✅ Processed event '{event.event_type.value}' for service '{target_service}' in {processing_time:.3f}s")
            
        except Exception as e:
            self.metrics["failed_events"] += 1
            logger.error(f"❌ Failed to process event '{event.event_type.value}' for service '{target_service}': {str(e)}")
    
    def _update_average_processing_time(self, processing_time: float):
        """
        Ortalama event işleme süresini güncelle.
        
        Args:
            processing_time: Bu event'in işleme süresi
        """
        current_avg = self.metrics["average_event_processing_time"]
        total_events = self.metrics["successful_events"]
        
        if total_events > 0:
            self.metrics["average_event_processing_time"] = (
                (current_avg * (total_events - 1) + processing_time) / total_events
            )
    
    async def start_distributed_transaction(self, transaction_context: TransactionContext) -> bool:
        """
        Distributed transaction başlat - Two-Phase Commit protokolü.
        
        Args:
            transaction_context: Transaction bağlam bilgileri
            
        Returns:
            bool: Transaction başarıyla başlatıldı mı
        """
        try:
            # Transaction'ı aktif listesine ekle
            self.active_transactions[transaction_context.transaction_id] = transaction_context
            self.metrics["active_transactions"] += 1
            
            logger.info(f"🚀 Starting distributed transaction '{transaction_context.transaction_id}' with {len(transaction_context.participants)} participants")
            
            # Phase 1: Prepare - tüm katılımcıları hazırla
            transaction_context.status = TransactionStatus.PREPARING
            prepare_success = await self._execute_prepare_phase(transaction_context)
            
            if prepare_success:
                # Phase 2: Commit - tüm katılımcılarda commit et
                transaction_context.status = TransactionStatus.COMMITTING
                commit_success = await self._execute_commit_phase(transaction_context)
                
                if commit_success:
                    transaction_context.status = TransactionStatus.COMMITTED
                    self.metrics["successful_transactions"] += 1
                    logger.info(f"✅ Transaction '{transaction_context.transaction_id}' committed successfully")
                    return True
                else:
                    # Commit başarısız, abort et
                    await self._execute_abort_phase(transaction_context)
                    return False
            else:
                # Prepare başarısız, abort et
                await self._execute_abort_phase(transaction_context)
                return False
                
        except Exception as e:
            logger.error(f"❌ Transaction '{transaction_context.transaction_id}' failed: {str(e)}")
            await self._execute_abort_phase(transaction_context)
            return False
        finally:
            # Transaction'ı aktif listesinden çıkar
            if transaction_context.transaction_id in self.active_transactions:
                del self.active_transactions[transaction_context.transaction_id]
                self.metrics["active_transactions"] -= 1
    
    async def _execute_prepare_phase(self, transaction_context: TransactionContext) -> bool:
        """
        Two-Phase Commit'in Prepare fazını çalıştır.
        
        Args:
            transaction_context: Transaction bağlamı
            
        Returns:
            bool: Tüm katılımcılar hazır mı
        """
        prepare_tasks = []
        
        # Her katılımcı servise prepare eventi gönder
        for participant in transaction_context.participants:
            event = ServiceEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.SERVICE_REQUEST,
                source_service=transaction_context.coordinator_service,
                target_service=participant,
                payload={
                    "action": "prepare_transaction",
                    "transaction_id": transaction_context.transaction_id,
                    "operations": transaction_context.operations.get(participant, {})
                },
                correlation_id=transaction_context.transaction_id
            )
            
            prepare_tasks.append(self._send_prepare_request(event, participant))
        
        # Tüm prepare yanıtlarını bekle
        results = await asyncio.gather(*prepare_tasks, return_exceptions=True)
        
        # Tüm katılımcılar hazır mı kontrol et
        all_prepared = all(
            isinstance(result, bool) and result for result in results
        )
        
        if all_prepared:
            transaction_context.status = TransactionStatus.PREPARED
            logger.info(f"✅ All participants prepared for transaction '{transaction_context.transaction_id}'")
        else:
            failed_participants = [
                transaction_context.participants[i] for i, result in enumerate(results)
                if not (isinstance(result, bool) and result)
            ]
            logger.warning(f"⚠️ Prepare failed for participants: {failed_participants}")
        
        return all_prepared
    
    async def _send_prepare_request(self, event: ServiceEvent, participant: str) -> bool:
        """
        Tek bir katılımcıya prepare isteği gönder.
        
        Args:
            event: Prepare eventi
            participant: Katılımcı servis
            
        Returns:
            bool: Katılımcı hazır mı
        """
        try:
            # Event'i publish et
            await self.publish_event(event)
            
            # Yanıt bekle (timeout ile)
            timeout_seconds = 10
            start_time = datetime.now()
            
            while (datetime.now() - start_time).seconds < timeout_seconds:
                # Redis'den yanıt kontrol et
                response_key = f"prepare_response:{event.correlation_id}:{participant}"
                response = await self.redis_client.get(response_key)
                
                if response:
                    response_data = json.loads(response)
                    return response_data.get("prepared", False)
                
                await asyncio.sleep(0.1)
            
            # Timeout
            logger.warning(f"⏰ Prepare timeout for participant '{participant}'")
            return False
            
        except Exception as e:
            logger.error(f"❌ Prepare request failed for participant '{participant}': {str(e)}")
            return False
    
    async def _execute_commit_phase(self, transaction_context: TransactionContext) -> bool:
        """
        Two-Phase Commit'in Commit fazını çalıştır.
        
        Args:
            transaction_context: Transaction bağlamı
            
        Returns:
            bool: Tüm katılımcılarda commit başarılı mı
        """
        commit_tasks = []
        
        # Her katılımcı servise commit eventi gönder
        for participant in transaction_context.participants:
            event = ServiceEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.SERVICE_REQUEST,
                source_service=transaction_context.coordinator_service,
                target_service=participant,
                payload={
                    "action": "commit_transaction",
                    "transaction_id": transaction_context.transaction_id
                },
                correlation_id=transaction_context.transaction_id
            )
            
            commit_tasks.append(self._send_commit_request(event, participant))
        
        # Tüm commit yanıtlarını bekle
        results = await asyncio.gather(*commit_tasks, return_exceptions=True)
        
        # Tüm katılımcılar commit etti mi kontrol et
        all_committed = all(
            isinstance(result, bool) and result for result in results
        )
        
        if all_committed:
            logger.info(f"✅ All participants committed transaction '{transaction_context.transaction_id}'")
        else:
            failed_participants = [
                transaction_context.participants[i] for i, result in enumerate(results)
                if not (isinstance(result, bool) and result)
            ]
            logger.error(f"❌ Commit failed for participants: {failed_participants}")
        
        return all_committed
    
    async def _send_commit_request(self, event: ServiceEvent, participant: str) -> bool:
        """
        Tek bir katılımcıya commit isteği gönder.
        
        Args:
            event: Commit eventi
            participant: Katılımcı servis
            
        Returns:
            bool: Katılımcı commit etti mi
        """
        try:
            # Event'i publish et
            await self.publish_event(event)
            
            # Yanıt bekle (timeout ile)
            timeout_seconds = 15
            start_time = datetime.now()
            
            while (datetime.now() - start_time).seconds < timeout_seconds:
                # Redis'den yanıt kontrol et
                response_key = f"commit_response:{event.correlation_id}:{participant}"
                response = await self.redis_client.get(response_key)
                
                if response:
                    response_data = json.loads(response)
                    return response_data.get("committed", False)
                
                await asyncio.sleep(0.1)
            
            # Timeout
            logger.warning(f"⏰ Commit timeout for participant '{participant}'")
            return False
            
        except Exception as e:
            logger.error(f"❌ Commit request failed for participant '{participant}': {str(e)}")
            return False
    
    async def _execute_abort_phase(self, transaction_context: TransactionContext):
        """
        Transaction'ı abort et - tüm değişiklikleri geri al.
        
        Args:
            transaction_context: Transaction bağlamı
        """
        transaction_context.status = TransactionStatus.ABORTING
        
        # Her katılımcı servise abort eventi gönder
        for participant in transaction_context.participants:
            event = ServiceEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.SERVICE_REQUEST,
                source_service=transaction_context.coordinator_service,
                target_service=participant,
                payload={
                    "action": "abort_transaction",
                    "transaction_id": transaction_context.transaction_id,
                    "compensation_actions": transaction_context.compensation_actions.get(participant, {})
                },
                correlation_id=transaction_context.transaction_id
            )
            
            try:
                await self.publish_event(event)
            except Exception as e:
                logger.error(f"❌ Failed to send abort to participant '{participant}': {str(e)}")
        
        transaction_context.status = TransactionStatus.ABORTED
        self.metrics["failed_transactions"] += 1
        
        logger.info(f"🔄 Transaction '{transaction_context.transaction_id}' aborted")
    
    async def _check_transaction_timeouts(self):
        """
        Background task - timeout olan transaction'ları kontrol et ve abort et.
        """
        logger.info("⏰ Started transaction timeout checker")
        
        while True:
            try:
                current_time = datetime.now()
                timed_out_transactions = []
                
                # Timeout olan transaction'ları bul
                for transaction_id, context in self.active_transactions.items():
                    elapsed_time = (current_time - context.start_time).seconds
                    if elapsed_time > context.timeout:
                        timed_out_transactions.append(transaction_id)
                
                # Timeout olan transaction'ları abort et
                for transaction_id in timed_out_transactions:
                    if transaction_id in self.active_transactions:
                        context = self.active_transactions[transaction_id]
                        logger.warning(f"⏰ Transaction '{transaction_id}' timed out after {context.timeout}s")
                        await self._execute_abort_phase(context)
                
                # 5 saniye bekle
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"❌ Transaction timeout checker error: {str(e)}")
                await asyncio.sleep(5)
    
    def get_service_state(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Servisin mevcut durumunu getir.
        
        Args:
            service_name: Servis adı
            
        Returns:
            Optional[Dict[str, Any]]: Servis durumu veya None
        """
        return self.service_states.get(service_name)
    
    def update_service_state(self, service_name: str, state_data: Dict[str, Any]):
        """
        Servis durumunu güncelle.
        
        Args:
            service_name: Servis adı
            state_data: Yeni durum verisi
        """
        if service_name in self.service_states:
            self.service_states[service_name].update(state_data)
            self.service_states[service_name]["last_updated"] = datetime.now()
        else:
            state_data["last_updated"] = datetime.now()
            self.service_states[service_name] = state_data
        
        logger.debug(f"🔄 Updated state for service '{service_name}'")
    
    def get_choreography_metrics(self) -> Dict[str, Any]:
        """
        Service choreography performans metriklerini getir.
        
        Returns:
            Dict[str, Any]: Detaylı metrik bilgileri
        """
        return {
            "choreography_metrics": self.metrics.copy(),
            "active_services": len(self.service_states),
            "registered_services": list(self.service_states.keys()),
            "active_transactions": len(self.active_transactions),
            "event_subscriptions": {
                service: [event_type.value for event_type in events]
                for service, events in self.event_subscriptions.items()
            },
            "service_health_status": {
                service: {
                    "status": state.get("status", "unknown"),
                    "last_seen": state.get("last_seen", datetime.now()).isoformat()
                }
                for service, state in self.service_states.items()
            }
        }

# Global choreography manager instance
choreography_manager = ServiceChoreographyManager()

# Helper fonksiyonlar
async def initialize_choreography():
    """Choreography manager'ı başlat."""
    await choreography_manager.initialize()

async def shutdown_choreography():
    """Choreography manager'ı kapat."""
    await choreography_manager.shutdown()

async def publish_service_event(event_type: EventType, source: str, target: str, payload: Dict[str, Any]):
    """
    Kolay kullanım için event publish helper fonksiyonu.
    
    Args:
        event_type: Event tipi
        source: Kaynak servis
        target: Hedef servis  
        payload: Event verisi
    """
    event = ServiceEvent(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        source_service=source,
        target_service=target,
        payload=payload,
        correlation_id=str(uuid.uuid4())
    )
    
    await choreography_manager.publish_event(event)

# Test fonksiyonu
async def test_choreography():
    """
    Service choreography'nin temel işlevlerini test et.
    """
    logger.info("🧪 Testing Service Choreography Manager...")
    
    try:
        # Manager'ı başlat
        await choreography_manager.initialize()
        
        # Test servisleri kaydet
        choreography_manager.register_service(
            "test_service_1", 
            [EventType.SERVICE_REQUEST, EventType.WORKFLOW_STARTED]
        )
        choreography_manager.register_service(
            "test_service_2", 
            [EventType.SERVICE_RESPONSE, EventType.DATA_UPDATED]
        )
        
        # Test event'i publish et
        test_event = ServiceEvent(
            event_id=str(uuid.uuid4()),
            event_type=EventType.WORKFLOW_STARTED,
            source_service="orchestrator",
            target_service=None,  # Broadcast
            payload={"workflow_id": "test_workflow", "data": "test_data"},
            correlation_id=str(uuid.uuid4())
        )
        
        await choreography_manager.publish_event(test_event)
        
        # Kısa bekleme
        await asyncio.sleep(2)
        
        # Metrikleri göster
        metrics = choreography_manager.get_choreography_metrics()
        logger.info(f"📊 Choreography metrics: {metrics}")
        
        # Test transaction
        transaction_context = TransactionContext(
            transaction_id=str(uuid.uuid4()),
            coordinator_service="orchestrator",
            participants=["test_service_1", "test_service_2"],
            status=TransactionStatus.PENDING,
            operations={
                "test_service_1": {"action": "update_data", "data": "value1"},
                "test_service_2": {"action": "update_data", "data": "value2"}
            }
        )
        
        # Transaction'ı başlat (fail edecek çünkü servisler gerçek değil)
        logger.info("🧪 Testing distributed transaction...")
        result = await choreography_manager.start_distributed_transaction(transaction_context)
        logger.info(f"📊 Transaction result: {result}")
        
        logger.info("✅ Choreography test completed")
        
    except Exception as e:
        logger.error(f"❌ Choreography test failed: {str(e)}")
    finally:
        await choreography_manager.shutdown()

if __name__ == "__main__":
    # Test çalıştır
    asyncio.run(test_choreography())
