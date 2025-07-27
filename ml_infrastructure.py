# 🤖 AURA AI - MACHINE LEARNING INFRASTRUCTURE (PHASE 8)
# Bu modül, tüm AI optimizasyonu ve makine öğrenmesi altyapısını sağlar
# Advanced ML pipeline framework ile intelligent automation yapar

# asyncio - asenkron ML pipeline işlemleri için temel kütüphane
import asyncio
# aiohttp - asenkron HTTP client ML model servis işlemleri için
import aiohttp
# json - JSON veri işleme ve ML model konfigürasyonu için
import json
# uuid - unique identifier generation for ML experiments and models
import uuid
# time - timing and performance measurement for ML operations
import time
# datetime - timestamp creation for ML model versioning and logging
from datetime import datetime, timedelta
# typing - type hints for ML pipeline components and data structures
from typing import Dict, List, Any, Optional, Union, Callable
# dataclasses - structured data classes for ML models and configurations
from dataclasses import dataclass, field
# enum - enumeration types for ML model states and operation types
from enum import Enum
# logging - comprehensive logging system for ML operations and debugging
import logging
# threading - thread management for parallel ML model training and inference
import threading
# queue - queue management for ML job processing and model serving
import queue
# collections - specialized data structures for ML feature engineering
from collections import defaultdict, deque
# statistics - statistical functions for ML model performance analysis
import statistics
# random - random number generation for ML sampling and experimentation
import random
# math - mathematical functions for ML algorithms and calculations
import math

# Set up comprehensive logging for ML infrastructure operations
# This logger tracks all ML model operations, training progress, and performance metrics
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('aura_ml_infrastructure')

class MLModelType(Enum):
    """
    Enumeration of machine learning model types supported by AURA AI system.
    Each type represents a different AI capability for fashion analysis and optimization.
    """
    # Workflow optimization models for intelligent routing and performance improvement
    WORKFLOW_OPTIMIZER = "workflow_optimizer"
    # Predictive scaling models for resource management and capacity planning
    PREDICTIVE_SCALER = "predictive_scaler"
    # Service health prediction models for proactive failure prevention
    SERVICE_HEALTH_PREDICTOR = "service_health_predictor"
    # User behavior analysis models for personalization and recommendation enhancement
    USER_BEHAVIOR_ANALYZER = "user_behavior_analyzer"
    # Fashion trend prediction models for staying ahead of style changes
    FASHION_TREND_PREDICTOR = "fashion_trend_predictor"
    # Performance anomaly detection models for system health monitoring
    ANOMALY_DETECTOR = "anomaly_detector"
    # Personalization engine models for individualized user experiences
    PERSONALIZATION_ENGINE = "personalization_engine"
    # Style compatibility models for fashion combination recommendations
    STYLE_COMPATIBILITY = "style_compatibility"

class MLModelState(Enum):
    """
    Enumeration of machine learning model states throughout their lifecycle.
    Tracks model status from initialization through production deployment.
    """
    # Model is being initialized with configuration and dependencies
    INITIALIZING = "initializing"
    # Model is currently training on dataset
    TRAINING = "training"
    # Model is being validated against test dataset
    VALIDATING = "validating"
    # Model is ready for inference and serving requests
    READY = "ready"
    # Model is actively serving predictions in production
    SERVING = "serving"
    # Model is being updated with new training data
    UPDATING = "updating"
    # Model has failed and needs attention
    FAILED = "failed"
    # Model is deprecated and being replaced
    DEPRECATED = "deprecated"

@dataclass
class MLModelMetrics:
    """
    Data class containing comprehensive metrics for machine learning model performance.
    Tracks accuracy, latency, throughput, and business impact metrics.
    """
    # Model accuracy percentage (0-100) for prediction correctness
    accuracy: float = 0.0
    # Average prediction latency in milliseconds for performance monitoring
    latency_ms: float = 0.0
    # Predictions per second throughput for capacity planning
    throughput_rps: float = 0.0
    # Total number of predictions made by this model
    prediction_count: int = 0
    # Model training accuracy achieved during last training session
    training_accuracy: float = 0.0
    # Validation accuracy from test dataset evaluation
    validation_accuracy: float = 0.0
    # Memory usage in MB for resource optimization
    memory_usage_mb: float = 0.0
    # CPU utilization percentage during model inference
    cpu_utilization: float = 0.0
    # Model version for tracking updates and improvements
    model_version: str = "1.0.0"
    # Last update timestamp for version control
    last_updated: datetime = field(default_factory=datetime.now)
    # Model confidence scores for prediction reliability assessment
    confidence_scores: List[float] = field(default_factory=list)
    # Business impact metrics specific to fashion AI domain
    business_metrics: Dict[str, float] = field(default_factory=dict)

@dataclass
class MLFeatureSet:
    """
    Data class representing a feature set for machine learning model training and inference.
    Contains structured feature data with metadata for ML pipeline processing.
    """
    # Unique identifier for this feature set
    feature_set_id: str
    # Human-readable name describing the feature set purpose
    name: str
    # Detailed description of what this feature set contains
    description: str
    # Dictionary of feature names and their values for ML model input
    features: Dict[str, Any] = field(default_factory=dict)
    # Feature extraction timestamp for freshness tracking
    timestamp: datetime = field(default_factory=datetime.now)
    # Data source information for lineage tracking
    source: str = "aura_system"
    # Feature version for schema evolution management
    version: str = "1.0.0"
    # Feature importance scores for model interpretation
    importance_scores: Dict[str, float] = field(default_factory=dict)
    # Feature validation status and quality metrics
    validation_status: Dict[str, bool] = field(default_factory=dict)

class AuraMLModel:
    """
    Base class for all AURA AI machine learning models.
    Provides common functionality for model lifecycle management, training, and inference.
    """
    
    def __init__(self, model_id: str, model_type: MLModelType, config: Dict[str, Any]):
        """
        Initialize an AURA ML model with configuration and metadata.
        
        Args:
            model_id: Unique identifier for this model instance
            model_type: Type of ML model from supported types enumeration
            config: Configuration dictionary with model parameters and settings
        """
        # Unique identifier for this specific model instance
        self.model_id = model_id
        # Type of machine learning model from supported enumeration
        self.model_type = model_type
        # Current state of the model in its lifecycle
        self.state = MLModelState.INITIALIZING
        # Configuration parameters for model behavior and performance
        self.config = config
        # Performance metrics tracking for this model
        self.metrics = MLModelMetrics()
        # Model creation timestamp for lifecycle tracking
        self.created_at = datetime.now()
        # Last activity timestamp for model usage monitoring
        self.last_used = datetime.now()
        # Thread lock for safe concurrent access to model state
        self._lock = threading.Lock()
        # Internal model implementation (will be set by subclasses)
        self._model = None
        # Feature set currently used by this model
        self.current_feature_set: Optional[MLFeatureSet] = None
        # Model prediction history for performance analysis
        self.prediction_history: deque = deque(maxlen=1000)
        
        # Log model initialization for monitoring and debugging
        logger.info(f"Initialized ML model {self.model_id} of type {self.model_type.value}")
    
    async def train(self, training_data: List[MLFeatureSet], validation_data: List[MLFeatureSet]) -> bool:
        """
        Train the machine learning model with provided training and validation data.
        Implements async training with progress tracking and performance monitoring.
        
        Args:
            training_data: List of feature sets for model training
            validation_data: List of feature sets for model validation
            
        Returns:
            bool: True if training completed successfully, False otherwise
        """
        # Thread-safe state update to training mode
        with self._lock:
            self.state = MLModelState.TRAINING
        
        try:
            # Log training start with data statistics for monitoring
            logger.info(f"Starting training for model {self.model_id} with {len(training_data)} training samples")
            
            # Simulate ML model training process with realistic timing
            # In production, this would integrate with TensorFlow, PyTorch, or other ML frameworks
            training_start = time.time()
            
            # Feature engineering phase - extract and prepare features for training
            processed_training_features = await self._extract_training_features(training_data)
            processed_validation_features = await self._extract_training_features(validation_data)
            
            # Model training simulation with progress tracking
            # Real implementation would use actual ML training algorithms
            for epoch in range(self.config.get('training_epochs', 10)):
                # Simulate training epoch with batch processing
                epoch_start = time.time()
                
                # Process training batches (simulated)
                batch_size = self.config.get('batch_size', 32)
                num_batches = len(processed_training_features) // batch_size
                
                epoch_loss = 0.0
                for batch_idx in range(num_batches):
                    # Simulate batch training step
                    batch_loss = random.uniform(0.1, 0.5) * (1.0 - epoch / 10.0)  # Decreasing loss
                    epoch_loss += batch_loss
                    
                    # Simulate training progress delay
                    await asyncio.sleep(0.01)
                
                # Calculate epoch metrics
                avg_epoch_loss = epoch_loss / num_batches
                epoch_duration = time.time() - epoch_start
                
                # Update training metrics
                self.metrics.training_accuracy = 85.0 + (epoch * 1.5)  # Simulated improving accuracy
                
                # Log epoch progress for monitoring
                logger.info(f"Model {self.model_id} epoch {epoch + 1}/{self.config.get('training_epochs', 10)} - "
                          f"Loss: {avg_epoch_loss:.4f}, Accuracy: {self.metrics.training_accuracy:.2f}%, "
                          f"Duration: {epoch_duration:.2f}s")
            
            # Validation phase after training completion
            with self._lock:
                self.state = MLModelState.VALIDATING
            
            # Perform model validation on validation dataset
            validation_accuracy = await self._validate_model(processed_validation_features)
            self.metrics.validation_accuracy = validation_accuracy
            
            # Calculate total training time
            training_duration = time.time() - training_start
            
            # Update model state to ready for serving
            with self._lock:
                self.state = MLModelState.READY
                self.metrics.last_updated = datetime.now()
            
            # Log successful training completion
            logger.info(f"Training completed for model {self.model_id} - "
                       f"Training Accuracy: {self.metrics.training_accuracy:.2f}%, "
                       f"Validation Accuracy: {self.metrics.validation_accuracy:.2f}%, "
                       f"Duration: {training_duration:.2f}s")
            
            return True
            
        except Exception as e:
            # Handle training errors with proper logging and state management
            logger.error(f"Training failed for model {self.model_id}: {str(e)}")
            with self._lock:
                self.state = MLModelState.FAILED
            return False
    
    async def predict(self, feature_set: MLFeatureSet) -> Dict[str, Any]:
        """
        Generate predictions using the trained machine learning model.
        Provides async inference with performance tracking and monitoring.
        
        Args:
            feature_set: Input features for model prediction
            
        Returns:
            Dict containing prediction results, confidence scores, and metadata
        """
        # Verify model is ready for inference
        if self.state not in [MLModelState.READY, MLModelState.SERVING]:
            raise ValueError(f"Model {self.model_id} is not ready for prediction. Current state: {self.state}")
        
        # Update model state to serving if not already
        with self._lock:
            if self.state == MLModelState.READY:
                self.state = MLModelState.SERVING
            self.last_used = datetime.now()
        
        try:
            # Start prediction timing for performance monitoring
            prediction_start = time.time()
            
            # Extract and process features for model input
            processed_features = await self._process_features_for_inference(feature_set)
            
            # Generate model prediction based on type
            # Real implementation would use trained ML model for inference
            prediction_result = await self._generate_prediction(processed_features)
            
            # Calculate prediction latency
            prediction_latency = (time.time() - prediction_start) * 1000  # Convert to milliseconds
            
            # Update model metrics with prediction performance
            self.metrics.prediction_count += 1
            self.metrics.latency_ms = (self.metrics.latency_ms * 0.9) + (prediction_latency * 0.1)  # Moving average
            
            # Calculate throughput (predictions per second)
            if len(self.prediction_history) > 0:
                time_window = (datetime.now() - self.prediction_history[0]['timestamp']).total_seconds()
                if time_window > 0:
                    self.metrics.throughput_rps = len(self.prediction_history) / time_window
            
            # Store prediction in history for analysis
            prediction_record = {
                'timestamp': datetime.now(),
                'latency_ms': prediction_latency,
                'feature_set_id': feature_set.feature_set_id,
                'prediction': prediction_result
            }
            self.prediction_history.append(prediction_record)
            
            # Create comprehensive prediction response
            response = {
                'model_id': self.model_id,
                'model_type': self.model_type.value,
                'prediction': prediction_result['prediction'],
                'confidence': prediction_result['confidence'],
                'latency_ms': prediction_latency,
                'timestamp': datetime.now().isoformat(),
                'feature_set_id': feature_set.feature_set_id,
                'model_version': self.metrics.model_version,
                'metadata': {
                    'prediction_count': self.metrics.prediction_count,
                    'average_latency_ms': self.metrics.latency_ms,
                    'throughput_rps': self.metrics.throughput_rps
                }
            }
            
            # Log prediction for monitoring and debugging
            logger.debug(f"Prediction generated by model {self.model_id} - "
                        f"Latency: {prediction_latency:.2f}ms, "
                        f"Confidence: {prediction_result['confidence']:.2f}")
            
            return response
            
        except Exception as e:
            # Handle prediction errors with proper logging
            logger.error(f"Prediction failed for model {self.model_id}: {str(e)}")
            raise
    
    async def _extract_training_features(self, data: List[MLFeatureSet]) -> List[Dict[str, Any]]:
        """
        Extract and preprocess features from training data for model input.
        Implements feature engineering pipeline specific to AURA AI domain.
        
        Args:
            data: List of feature sets from training dataset
            
        Returns:
            List of processed feature dictionaries ready for ML training
        """
        # Process each feature set for training compatibility
        processed_features = []
        
        for feature_set in data:
            # Extract relevant features based on model type
            if self.model_type == MLModelType.WORKFLOW_OPTIMIZER:
                # Extract workflow performance and timing features
                features = {
                    'execution_time': feature_set.features.get('execution_time', 0.0),
                    'service_latencies': feature_set.features.get('service_latencies', []),
                    'success_rate': feature_set.features.get('success_rate', 1.0),
                    'resource_usage': feature_set.features.get('resource_usage', {}),
                    'workflow_complexity': feature_set.features.get('workflow_complexity', 1.0)
                }
            elif self.model_type == MLModelType.USER_BEHAVIOR_ANALYZER:
                # Extract user interaction and preference features
                features = {
                    'session_duration': feature_set.features.get('session_duration', 0.0),
                    'click_patterns': feature_set.features.get('click_patterns', []),
                    'style_preferences': feature_set.features.get('style_preferences', {}),
                    'interaction_history': feature_set.features.get('interaction_history', []),
                    'demographic_data': feature_set.features.get('demographic_data', {})
                }
            else:
                # Default feature extraction for other model types
                features = feature_set.features
            
            # Add temporal features for time-series analysis
            features['hour_of_day'] = feature_set.timestamp.hour
            features['day_of_week'] = feature_set.timestamp.weekday()
            features['month'] = feature_set.timestamp.month
            
            processed_features.append(features)
        
        return processed_features
    
    async def _validate_model(self, validation_features: List[Dict[str, Any]]) -> float:
        """
        Validate trained model performance against validation dataset.
        Calculates accuracy and other performance metrics for model assessment.
        
        Args:
            validation_features: Processed validation dataset features
            
        Returns:
            float: Validation accuracy percentage (0-100)
        """
        # Simulate model validation process
        correct_predictions = 0
        total_predictions = len(validation_features)
        
        for features in validation_features:
            # Simulate prediction accuracy based on model type and complexity
            base_accuracy = 0.85  # Base 85% accuracy
            
            # Adjust accuracy based on model type
            if self.model_type == MLModelType.WORKFLOW_OPTIMIZER:
                accuracy_modifier = 0.05  # Workflow optimization is highly accurate
            elif self.model_type == MLModelType.USER_BEHAVIOR_ANALYZER:
                accuracy_modifier = 0.03  # User behavior has some uncertainty
            else:
                accuracy_modifier = 0.02
            
            # Random validation with bias toward accuracy
            if random.random() < (base_accuracy + accuracy_modifier):
                correct_predictions += 1
            
            # Small delay to simulate validation processing
            await asyncio.sleep(0.001)
        
        # Calculate validation accuracy percentage
        validation_accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0.0
        
        return validation_accuracy
    
    async def _process_features_for_inference(self, feature_set: MLFeatureSet) -> Dict[str, Any]:
        """
        Process input features for model inference, applying same transformations as training.
        Ensures consistent feature format between training and inference phases.
        
        Args:
            feature_set: Input feature set for prediction
            
        Returns:
            Dict containing processed features ready for model inference
        """
        # Apply same feature extraction logic as training
        if self.model_type == MLModelType.WORKFLOW_OPTIMIZER:
            processed_features = {
                'execution_time': feature_set.features.get('execution_time', 0.0),
                'service_latencies': feature_set.features.get('service_latencies', []),
                'success_rate': feature_set.features.get('success_rate', 1.0),
                'resource_usage': feature_set.features.get('resource_usage', {}),
                'workflow_complexity': feature_set.features.get('workflow_complexity', 1.0)
            }
        elif self.model_type == MLModelType.USER_BEHAVIOR_ANALYZER:
            processed_features = {
                'session_duration': feature_set.features.get('session_duration', 0.0),
                'click_patterns': feature_set.features.get('click_patterns', []),
                'style_preferences': feature_set.features.get('style_preferences', {}),
                'interaction_history': feature_set.features.get('interaction_history', []),
                'demographic_data': feature_set.features.get('demographic_data', {})
            }
        else:
            processed_features = feature_set.features.copy()
        
        # Add temporal features consistent with training
        processed_features['hour_of_day'] = feature_set.timestamp.hour
        processed_features['day_of_week'] = feature_set.timestamp.weekday()
        processed_features['month'] = feature_set.timestamp.month
        
        return processed_features
    
    async def _generate_prediction(self, processed_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate actual prediction using processed features and trained model.
        Implements model-specific prediction logic with confidence scoring.
        
        Args:
            processed_features: Features processed for model input
            
        Returns:
            Dict containing prediction result and confidence score
        """
        # Generate prediction based on model type
        if self.model_type == MLModelType.WORKFLOW_OPTIMIZER:
            # Predict optimal workflow configuration
            prediction = {
                'optimal_routing': ['service_1', 'service_3', 'service_2'],
                'expected_latency_ms': random.uniform(180, 220),
                'resource_allocation': {
                    'cpu_cores': random.randint(2, 6),
                    'memory_gb': random.randint(4, 12)
                },
                'parallelization_factor': random.uniform(1.5, 3.0)
            }
            confidence = random.uniform(0.85, 0.95)
            
        elif self.model_type == MLModelType.USER_BEHAVIOR_ANALYZER:
            # Predict user behavior and preferences
            prediction = {
                'preferred_styles': ['casual', 'modern', 'minimalist'],
                'engagement_probability': random.uniform(0.7, 0.95),
                'session_extension_likelihood': random.uniform(0.6, 0.9),
                'recommendation_acceptance_rate': random.uniform(0.75, 0.92)
            }
            confidence = random.uniform(0.80, 0.93)
            
        elif self.model_type == MLModelType.PREDICTIVE_SCALER:
            # Predict resource scaling requirements
            prediction = {
                'scale_direction': random.choice(['up', 'down', 'maintain']),
                'scale_factor': random.uniform(0.8, 2.0),
                'expected_load': random.uniform(0.4, 0.9),
                'scaling_urgency': random.choice(['low', 'medium', 'high'])
            }
            confidence = random.uniform(0.88, 0.96)
            
        else:
            # Generic prediction for other model types
            prediction = {
                'result': f"prediction_for_{self.model_type.value}",
                'value': random.uniform(0.0, 1.0),
                'category': random.choice(['A', 'B', 'C'])
            }
            confidence = random.uniform(0.82, 0.94)
        
        return {
            'prediction': prediction,
            'confidence': confidence
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive performance metrics for this ML model.
        Provides detailed statistics for monitoring and optimization.
        
        Returns:
            Dict containing all model performance metrics and statistics
        """
        with self._lock:
            # Calculate additional derived metrics
            recent_predictions = [p for p in self.prediction_history 
                                if (datetime.now() - p['timestamp']).total_seconds() < 300]  # Last 5 minutes
            
            recent_latencies = [p['latency_ms'] for p in recent_predictions]
            
            metrics_dict = {
                'model_id': self.model_id,
                'model_type': self.model_type.value,
                'state': self.state.value,
                'accuracy': self.metrics.accuracy,
                'training_accuracy': self.metrics.training_accuracy,
                'validation_accuracy': self.metrics.validation_accuracy,
                'average_latency_ms': self.metrics.latency_ms,
                'recent_avg_latency_ms': statistics.mean(recent_latencies) if recent_latencies else 0.0,
                'throughput_rps': self.metrics.throughput_rps,
                'total_predictions': self.metrics.prediction_count,
                'recent_predictions': len(recent_predictions),
                'memory_usage_mb': self.metrics.memory_usage_mb,
                'cpu_utilization': self.metrics.cpu_utilization,
                'model_version': self.metrics.model_version,
                'created_at': self.created_at.isoformat(),
                'last_updated': self.metrics.last_updated.isoformat(),
                'last_used': self.last_used.isoformat(),
                'uptime_seconds': (datetime.now() - self.created_at).total_seconds(),
                'business_metrics': self.metrics.business_metrics.copy()
            }
            
            return metrics_dict

class AuraMLInfrastructure:
    """
    Main infrastructure class for managing all AURA AI machine learning models and operations.
    Provides centralized ML model management, training orchestration, and inference serving.
    """
    
    def __init__(self):
        """
        Initialize the AURA ML infrastructure with model registry and management systems.
        Sets up the foundation for all AI-powered optimizations and intelligent automation.
        """
        # Registry of all ML models managed by this infrastructure
        self.models: Dict[str, AuraMLModel] = {}
        # Model registry organized by type for efficient lookup
        self.models_by_type: Dict[MLModelType, List[str]] = defaultdict(list)
        # Thread lock for safe concurrent access to model registry
        self._lock = threading.Lock()
        # Background tasks queue for async ML operations
        self.task_queue: queue.Queue = queue.Queue()
        # Infrastructure metrics and statistics
        self.infrastructure_metrics = {
            'total_models': 0,
            'active_models': 0,
            'total_predictions': 0,
            'average_latency_ms': 0.0,
            'total_training_jobs': 0,
            'successful_training_jobs': 0,
            'infrastructure_uptime': datetime.now()
        }
        # Background task executor for async operations
        self.executor_running = False
        self.executor_task = None
        
        # Log infrastructure initialization
        logger.info("AURA ML Infrastructure initialized successfully")
    
    async def register_model(self, model_id: str, model_type: MLModelType, config: Dict[str, Any]) -> AuraMLModel:
        """
        Register a new machine learning model in the infrastructure.
        Provides centralized model lifecycle management and configuration.
        
        Args:
            model_id: Unique identifier for the new model
            model_type: Type of ML model from supported enumeration
            config: Configuration parameters for model behavior
            
        Returns:
            AuraMLModel: Newly created and registered model instance
        """
        # Thread-safe model registration
        with self._lock:
            # Check if model ID already exists
            if model_id in self.models:
                raise ValueError(f"Model with ID '{model_id}' already exists")
            
            # Create new model instance
            model = AuraMLModel(model_id, model_type, config)
            
            # Register model in central registry
            self.models[model_id] = model
            self.models_by_type[model_type].append(model_id)
            
            # Update infrastructure metrics
            self.infrastructure_metrics['total_models'] += 1
            if model.state in [MLModelState.READY, MLModelState.SERVING]:
                self.infrastructure_metrics['active_models'] += 1
        
        # Log successful model registration
        logger.info(f"Registered new ML model '{model_id}' of type '{model_type.value}'")
        
        return model
    
    async def train_model(self, model_id: str, training_data: List[MLFeatureSet], 
                         validation_data: List[MLFeatureSet]) -> bool:
        """
        Train a registered machine learning model with provided datasets.
        Manages training process with progress tracking and performance monitoring.
        
        Args:
            model_id: ID of the model to train
            training_data: Training dataset as list of feature sets
            validation_data: Validation dataset for model assessment
            
        Returns:
            bool: True if training completed successfully, False otherwise
        """
        # Retrieve model from registry
        if model_id not in self.models:
            raise ValueError(f"Model '{model_id}' not found in registry")
        
        model = self.models[model_id]
        
        # Update infrastructure training metrics
        self.infrastructure_metrics['total_training_jobs'] += 1
        
        try:
            # Start model training with progress tracking
            logger.info(f"Starting training for model '{model_id}' with {len(training_data)} training samples")
            
            # Execute model training
            training_success = await model.train(training_data, validation_data)
            
            if training_success:
                # Update infrastructure metrics for successful training
                self.infrastructure_metrics['successful_training_jobs'] += 1
                
                # Update active models count if model is now ready
                with self._lock:
                    if model.state == MLModelState.READY:
                        self.infrastructure_metrics['active_models'] += 1
                
                logger.info(f"Successfully trained model '{model_id}' - "
                          f"Training Accuracy: {model.metrics.training_accuracy:.2f}%, "
                          f"Validation Accuracy: {model.metrics.validation_accuracy:.2f}%")
            else:
                logger.error(f"Training failed for model '{model_id}'")
            
            return training_success
            
        except Exception as e:
            logger.error(f"Training error for model '{model_id}': {str(e)}")
            return False
    
    async def predict(self, model_id: str, feature_set: MLFeatureSet) -> Dict[str, Any]:
        """
        Generate prediction using specified trained model.
        Provides centralized inference serving with performance tracking.
        
        Args:
            model_id: ID of the model to use for prediction
            feature_set: Input features for prediction
            
        Returns:
            Dict containing prediction results and metadata
        """
        # Retrieve model from registry
        if model_id not in self.models:
            raise ValueError(f"Model '{model_id}' not found in registry")
        
        model = self.models[model_id]
        
        try:
            # Generate prediction using model
            prediction_result = await model.predict(feature_set)
            
            # Update infrastructure metrics
            self.infrastructure_metrics['total_predictions'] += 1
            
            # Update average latency with moving average
            current_latency = prediction_result['latency_ms']
            if self.infrastructure_metrics['average_latency_ms'] == 0:
                self.infrastructure_metrics['average_latency_ms'] = current_latency
            else:
                # Exponential moving average for latency tracking
                self.infrastructure_metrics['average_latency_ms'] = (
                    self.infrastructure_metrics['average_latency_ms'] * 0.9 + 
                    current_latency * 0.1
                )
            
            return prediction_result
            
        except Exception as e:
            logger.error(f"Prediction error for model '{model_id}': {str(e)}")
            raise
    
    async def get_models_by_type(self, model_type: MLModelType) -> List[AuraMLModel]:
        """
        Retrieve all models of a specific type from the registry.
        Enables type-based model management and load balancing.
        
        Args:
            model_type: Type of models to retrieve
            
        Returns:
            List of models matching the specified type
        """
        with self._lock:
            model_ids = self.models_by_type.get(model_type, [])
            return [self.models[model_id] for model_id in model_ids if model_id in self.models]
    
    async def get_best_model_for_type(self, model_type: MLModelType) -> Optional[AuraMLModel]:
        """
        Get the best performing model of a specific type based on metrics.
        Implements intelligent model selection for optimal performance.
        
        Args:
            model_type: Type of model to find the best instance for
            
        Returns:
            AuraMLModel: Best performing model of the specified type, or None if no models found
        """
        models = await self.get_models_by_type(model_type)
        
        # Filter to only ready/serving models
        available_models = [m for m in models if m.state in [MLModelState.READY, MLModelState.SERVING]]
        
        if not available_models:
            return None
        
        # Select best model based on composite score of accuracy and performance
        def model_score(model: AuraMLModel) -> float:
            # Composite score: accuracy (70%) + speed (30%)
            accuracy_score = model.metrics.validation_accuracy * 0.7
            speed_score = max(0, (1000 - model.metrics.latency_ms) / 1000) * 100 * 0.3
            return accuracy_score + speed_score
        
        best_model = max(available_models, key=model_score)
        
        logger.debug(f"Selected best model '{best_model.model_id}' for type '{model_type.value}' - "
                    f"Score: {model_score(best_model):.2f}")
        
        return best_model
    
    def get_infrastructure_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive infrastructure metrics and statistics.
        Provides system-wide performance monitoring and health information.
        
        Returns:
            Dict containing all infrastructure metrics and model statistics
        """
        with self._lock:
            # Calculate derived metrics
            active_models = sum(1 for model in self.models.values() 
                              if model.state in [MLModelState.READY, MLModelState.SERVING])
            
            total_predictions = sum(model.metrics.prediction_count for model in self.models.values())
            
            # Calculate average model accuracy across all models
            model_accuracies = [model.metrics.validation_accuracy for model in self.models.values()
                              if model.metrics.validation_accuracy > 0]
            avg_model_accuracy = statistics.mean(model_accuracies) if model_accuracies else 0.0
            
            # Infrastructure uptime calculation
            uptime_seconds = (datetime.now() - self.infrastructure_metrics['infrastructure_uptime']).total_seconds()
            
            # Comprehensive metrics dictionary
            metrics = {
                'infrastructure_status': 'operational',
                'total_models': len(self.models),
                'active_models': active_models,
                'models_by_state': {
                    state.value: sum(1 for model in self.models.values() if model.state == state)
                    for state in MLModelState
                },
                'models_by_type': {
                    model_type.value: len(model_ids) 
                    for model_type, model_ids in self.models_by_type.items()
                },
                'total_predictions': total_predictions,
                'average_infrastructure_latency_ms': self.infrastructure_metrics['average_latency_ms'],
                'average_model_accuracy': avg_model_accuracy,
                'total_training_jobs': self.infrastructure_metrics['total_training_jobs'],
                'successful_training_jobs': self.infrastructure_metrics['successful_training_jobs'],
                'training_success_rate': (
                    self.infrastructure_metrics['successful_training_jobs'] / 
                    max(1, self.infrastructure_metrics['total_training_jobs']) * 100
                ),
                'infrastructure_uptime_seconds': uptime_seconds,
                'infrastructure_uptime_hours': uptime_seconds / 3600,
                'timestamp': datetime.now().isoformat()
            }
            
            return metrics

# Global ML infrastructure instance for AURA AI system
# This provides centralized access to all machine learning capabilities
aura_ml_infrastructure = AuraMLInfrastructure()

# Helper functions for easy model management and common ML operations

async def create_workflow_optimizer(model_id: str = None) -> AuraMLModel:
    """
    Create and register a workflow optimization model for intelligent routing.
    Optimizes service orchestration and workflow execution performance.
    
    Args:
        model_id: Optional custom model ID, auto-generated if not provided
        
    Returns:
        AuraMLModel: Newly created workflow optimizer model
    """
    if model_id is None:
        model_id = f"workflow_optimizer_{uuid.uuid4().hex[:8]}"
    
    # Configuration for workflow optimization model
    config = {
        'training_epochs': 15,
        'batch_size': 64,
        'learning_rate': 0.001,
        'optimization_target': 'latency_minimization',
        'feature_engineering': 'automatic',
        'model_architecture': 'gradient_boosting'
    }
    
    # Register and return workflow optimizer model
    model = await aura_ml_infrastructure.register_model(model_id, MLModelType.WORKFLOW_OPTIMIZER, config)
    
    logger.info(f"Created workflow optimizer model '{model_id}' for intelligent routing optimization")
    return model

async def create_user_behavior_analyzer(model_id: str = None) -> AuraMLModel:
    """
    Create and register a user behavior analysis model for personalization.
    Analyzes user patterns and preferences for enhanced recommendation accuracy.
    
    Args:
        model_id: Optional custom model ID, auto-generated if not provided
        
    Returns:
        AuraMLModel: Newly created user behavior analyzer model
    """
    if model_id is None:
        model_id = f"user_behavior_analyzer_{uuid.uuid4().hex[:8]}"
    
    # Configuration for user behavior analysis model
    config = {
        'training_epochs': 20,
        'batch_size': 32,
        'learning_rate': 0.0005,
        'analysis_depth': 'deep_learning',
        'personalization_level': 'high',
        'model_architecture': 'neural_network'
    }
    
    # Register and return user behavior analyzer model
    model = await aura_ml_infrastructure.register_model(model_id, MLModelType.USER_BEHAVIOR_ANALYZER, config)
    
    logger.info(f"Created user behavior analyzer model '{model_id}' for advanced personalization")
    return model

async def create_predictive_scaler(model_id: str = None) -> AuraMLModel:
    """
    Create and register a predictive scaling model for resource optimization.
    Predicts resource demands and automates scaling decisions for optimal performance.
    
    Args:
        model_id: Optional custom model ID, auto-generated if not provided
        
    Returns:
        AuraMLModel: Newly created predictive scaler model
    """
    if model_id is None:
        model_id = f"predictive_scaler_{uuid.uuid4().hex[:8]}"
    
    # Configuration for predictive scaling model
    config = {
        'training_epochs': 12,
        'batch_size': 48,
        'learning_rate': 0.002,
        'prediction_horizon_minutes': 30,
        'scaling_sensitivity': 'medium',
        'model_architecture': 'time_series_lstm'
    }
    
    # Register and return predictive scaler model
    model = await aura_ml_infrastructure.register_model(model_id, MLModelType.PREDICTIVE_SCALER, config)
    
    logger.info(f"Created predictive scaler model '{model_id}' for intelligent resource management")
    return model

# Convenience function for generating sample training data for ML models
def generate_sample_training_data(model_type: MLModelType, num_samples: int = 100) -> List[MLFeatureSet]:
    """
    Generate sample training data for testing and development of ML models.
    Creates realistic feature sets based on model type and AURA AI domain.
    
    Args:
        model_type: Type of model to generate training data for
        num_samples: Number of training samples to generate
        
    Returns:
        List of MLFeatureSet objects suitable for model training
    """
    training_data = []
    
    for i in range(num_samples):
        feature_set_id = f"training_sample_{i}_{uuid.uuid4().hex[:6]}"
        
        if model_type == MLModelType.WORKFLOW_OPTIMIZER:
            # Generate workflow performance training data
            features = {
                'execution_time': random.uniform(200, 800),  # ms
                'service_latencies': [random.uniform(50, 200) for _ in range(5)],
                'success_rate': random.uniform(0.85, 1.0),
                'resource_usage': {
                    'cpu': random.uniform(0.2, 0.8),
                    'memory': random.uniform(0.3, 0.9),
                    'network': random.uniform(0.1, 0.6)
                },
                'workflow_complexity': random.uniform(1.0, 5.0)
            }
            
        elif model_type == MLModelType.USER_BEHAVIOR_ANALYZER:
            # Generate user behavior training data
            features = {
                'session_duration': random.uniform(60, 1800),  # seconds
                'click_patterns': [random.randint(1, 10) for _ in range(3)],
                'style_preferences': {
                    'casual': random.uniform(0.0, 1.0),
                    'formal': random.uniform(0.0, 1.0),
                    'sport': random.uniform(0.0, 1.0)
                },
                'interaction_history': [random.choice(['view', 'like', 'share']) for _ in range(5)],
                'demographic_data': {
                    'age_group': random.choice(['18-25', '26-35', '36-45', '46+']),
                    'location': random.choice(['urban', 'suburban', 'rural'])
                }
            }
            
        else:
            # Generic training data for other model types
            features = {
                'feature_1': random.uniform(0.0, 1.0),
                'feature_2': random.randint(1, 100),
                'feature_3': random.choice(['A', 'B', 'C']),
                'feature_4': [random.uniform(0.0, 1.0) for _ in range(3)]
            }
        
        # Create feature set with realistic timestamp
        feature_set = MLFeatureSet(
            feature_set_id=feature_set_id,
            name=f"Training Sample {i}",
            description=f"Sample training data for {model_type.value}",
            features=features,
            timestamp=datetime.now() - timedelta(minutes=random.randint(0, 1440))  # Random within last day
        )
        
        training_data.append(feature_set)
    
    return training_data

# Main execution function for testing ML infrastructure
async def main():
    """
    Main function demonstrating AURA ML infrastructure capabilities.
    Creates sample models, trains them, and demonstrates inference.
    """
    logger.info("🤖 AURA AI - PHASE 8: ML INFRASTRUCTURE DEMONSTRATION")
    logger.info("=" * 70)
    
    try:
        # Create sample ML models for demonstration
        logger.info("Creating sample ML models...")
        
        # Create workflow optimizer
        workflow_model = await create_workflow_optimizer("demo_workflow_optimizer")
        
        # Create user behavior analyzer
        behavior_model = await create_user_behavior_analyzer("demo_behavior_analyzer")
        
        # Create predictive scaler
        scaler_model = await create_predictive_scaler("demo_predictive_scaler")
        
        # Generate training data for models
        logger.info("Generating training data...")
        
        workflow_training_data = generate_sample_training_data(MLModelType.WORKFLOW_OPTIMIZER, 80)
        workflow_validation_data = generate_sample_training_data(MLModelType.WORKFLOW_OPTIMIZER, 20)
        
        behavior_training_data = generate_sample_training_data(MLModelType.USER_BEHAVIOR_ANALYZER, 80)
        behavior_validation_data = generate_sample_training_data(MLModelType.USER_BEHAVIOR_ANALYZER, 20)
        
        # Train models
        logger.info("Training ML models...")
        
        # Train workflow optimizer
        workflow_success = await aura_ml_infrastructure.train_model(
            "demo_workflow_optimizer", workflow_training_data, workflow_validation_data
        )
        
        # Train behavior analyzer
        behavior_success = await aura_ml_infrastructure.train_model(
            "demo_behavior_analyzer", behavior_training_data, behavior_validation_data
        )
        
        # Demonstrate predictions
        if workflow_success:
            logger.info("Demonstrating workflow optimization predictions...")
            
            # Create sample feature set for prediction
            sample_features = MLFeatureSet(
                feature_set_id="demo_prediction_features",
                name="Demo Prediction",
                description="Sample features for demonstration",
                features={
                    'execution_time': 350.0,
                    'service_latencies': [75, 120, 90, 110, 95],
                    'success_rate': 0.92,
                    'resource_usage': {'cpu': 0.65, 'memory': 0.45, 'network': 0.25},
                    'workflow_complexity': 2.5
                }
            )
            
            # Generate prediction
            prediction_result = await aura_ml_infrastructure.predict("demo_workflow_optimizer", sample_features)
            logger.info(f"Workflow optimization prediction: {prediction_result['prediction']}")
            logger.info(f"Prediction confidence: {prediction_result['confidence']:.2f}")
            logger.info(f"Prediction latency: {prediction_result['latency_ms']:.2f}ms")
        
        # Display infrastructure metrics
        logger.info("Getting infrastructure metrics...")
        metrics = aura_ml_infrastructure.get_infrastructure_metrics()
        
        logger.info("🏆 INFRASTRUCTURE METRICS:")
        logger.info(f"  Total Models: {metrics['total_models']}")
        logger.info(f"  Active Models: {metrics['active_models']}")
        logger.info(f"  Total Predictions: {metrics['total_predictions']}")
        logger.info(f"  Average Latency: {metrics['average_infrastructure_latency_ms']:.2f}ms")
        logger.info(f"  Average Model Accuracy: {metrics['average_model_accuracy']:.2f}%")
        logger.info(f"  Training Success Rate: {metrics['training_success_rate']:.1f}%")
        
        logger.info("✅ AURA ML Infrastructure demonstration completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ ML Infrastructure demonstration error: {str(e)}")
        raise

if __name__ == "__main__":
    # Run the ML infrastructure demonstration
    asyncio.run(main())
