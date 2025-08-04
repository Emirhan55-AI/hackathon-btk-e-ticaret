# Phase 8: Feedback Loop Implementation with Advanced Learning Capabilities
# This module implements intelligent feedback collection, analysis, and system adaptation
# Integrates all previous phases to create a self-improving AI style assistant

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
import asyncio
import json
from datetime import datetime, timedelta
import uuid
from enum import Enum
from dataclasses import dataclass, asdict
import requests
from collections import defaultdict, deque
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import sqlite3
from contextlib import contextmanager
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import warnings
warnings.filterwarnings("ignore")

# Configure comprehensive logging for the feedback loop system
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """
    Enumeration for different types of user feedback.
    Categorizes feedback for appropriate processing and learning.
    """
    EXPLICIT_RATING = "explicit_rating"          # Direct user ratings (1-5 stars)
    IMPLICIT_ENGAGEMENT = "implicit_engagement"  # Usage patterns, time spent
    BEHAVIORAL_SIGNALS = "behavioral_signals"    # Clicks, saves, shares
    PREFERENCE_UPDATES = "preference_updates"    # Direct preference changes
    REJECTION_FEEDBACK = "rejection_feedback"    # Explicit rejection of recommendations
    ACCEPTANCE_FEEDBACK = "acceptance_feedback"  # Acceptance/usage of recommendations
    CONTEXTUAL_FEEDBACK = "contextual_feedback"  # Context-specific feedback

class LearningObjective(Enum):
    """
    Enumeration for different learning objectives in the feedback system.
    Defines what aspects of the system should be improved.
    """
    RECOMMENDATION_ACCURACY = "recommendation_accuracy"
    STYLE_PROFILING_PRECISION = "style_profiling_precision"
    COMBINATION_QUALITY = "combination_quality"
    CONTEXT_UNDERSTANDING = "context_understanding"
    USER_SATISFACTION = "user_satisfaction"
    ENGAGEMENT_OPTIMIZATION = "engagement_optimization"

@dataclass
class FeedbackEntry:
    """
    Data class representing a single feedback entry from a user.
    Contains all information needed for learning and adaptation.
    """
    feedback_id: str
    user_id: str
    session_id: str
    feedback_type: FeedbackType
    learning_objective: LearningObjective
    feedback_data: Dict[str, Any]
    context: Dict[str, Any]
    timestamp: datetime
    service_source: str  # Which service generated the content being rated
    confidence: float = 1.0
    processed: bool = False
    learning_applied: bool = False

@dataclass
class LearningInsight:
    """
    Data class representing insights learned from feedback analysis.
    Contains actionable intelligence for system improvement.
    """
    insight_id: str
    learning_objective: LearningObjective
    user_segment: Optional[str]
    insight_data: Dict[str, Any]
    confidence_score: float
    impact_estimate: float
    action_recommendations: List[str]
    created_at: datetime
    applied_at: Optional[datetime] = None

class AdvancedFeedbackProcessor:
    """
    Advanced feedback processing and learning system for the Aura AI platform.
    
    This processor implements:
    - Multi-modal feedback collection from all services
    - Advanced machine learning for pattern recognition
    - Real-time system adaptation based on user behavior
    - Personalized learning for individual users
    - Aggregate learning for system-wide improvements
    - Continuous model updating and optimization
    """
    
    def __init__(self, 
                 orchestrator_url: str = "http://localhost:8006",
                 database_path: str = "feedback_system.db"):
        """
        Initialize the advanced feedback processing system.
        Sets up ML models, database connections, and service integrations.
        
        Args:
            orchestrator_url: URL of the Phase 7 orchestration service
            database_path: Path to the SQLite database for feedback storage
        """
        logger.info("Initializing Advanced Feedback Processing System - Phase 8")
        
        # Service integration URLs
        self.orchestrator_url = orchestrator_url
        self.service_urls = {
            'image_processing': 'http://localhost:8001',
            'nlu_service': 'http://localhost:8002',
            'style_profile': 'http://localhost:8003',
            'combination_engine': 'http://localhost:8004',
            'recommendation_engine': 'http://localhost:8005',
            'orchestrator': orchestrator_url
        }
        
        # Database setup for persistent feedback storage
        self.database_path = database_path
        self._initialize_database()
        
        # Machine learning models for different learning objectives
        self.ml_models = {
            'recommendation_accuracy': RandomForestRegressor(n_estimators=100, random_state=42),
            'style_profiling_precision': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'combination_quality': RandomForestRegressor(n_estimators=100, random_state=42),
            'user_satisfaction': GradientBoostingClassifier(n_estimators=50, random_state=42),
            'engagement_optimization': RandomForestRegressor(n_estimators=75, random_state=42)
        }
        
        # Feature scalers for each model
        self.feature_scalers = {
            objective.value: StandardScaler() 
            for objective in LearningObjective
        }
        
        # Label encoders for categorical data
        self.label_encoders = {
            'user_segments': LabelEncoder(),
            'contexts': LabelEncoder(),
            'feedback_types': LabelEncoder()
        }
        
        # Real-time feedback processing queue
        self.feedback_queue = deque(maxlen=10000)
        self.processing_thread = None
        self.processing_active = False
        
        # Learning insights storage
        self.learning_insights: Dict[str, LearningInsight] = {}
        self.user_adaptations: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Performance metrics tracking
        self.learning_metrics = {
            'total_feedback_processed': 0,
            'learning_insights_generated': 0,
            'adaptations_applied': 0,
            'model_improvements': 0,
            'user_satisfaction_trend': [],
            'engagement_improvements': []
        }
        
        # Thread pool for concurrent processing
        self.executor = ThreadPoolExecutor(max_workers=5)
        
        # Model training history
        self.training_history = {
            objective.value: {
                'last_trained': None,
                'training_samples': 0,
                'accuracy_history': [],
                'improvement_rate': 0.0
            }
            for objective in LearningObjective
        }
        
        logger.info("✅ Advanced Feedback Processing System initialized successfully")
        logger.info(f"   Connected to Orchestrator: {orchestrator_url}")
        logger.info(f"   Database: {database_path}")
        logger.info(f"   ML Models: {len(self.ml_models)} learning objectives")
        logger.info(f"   Ready for multi-modal feedback processing and learning")
    
    def _initialize_database(self):
        """
        Initialize SQLite database for persistent feedback storage.
        Creates tables for feedback entries, learning insights, and user adaptations.
        """
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                
                # Feedback entries table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS feedback_entries (
                        feedback_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        session_id TEXT NOT NULL,
                        feedback_type TEXT NOT NULL,
                        learning_objective TEXT NOT NULL,
                        feedback_data TEXT NOT NULL,
                        context TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        service_source TEXT NOT NULL,
                        confidence REAL DEFAULT 1.0,
                        processed INTEGER DEFAULT 0,
                        learning_applied INTEGER DEFAULT 0
                    )
                ''')
                
                # Learning insights table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS learning_insights (
                        insight_id TEXT PRIMARY KEY,
                        learning_objective TEXT NOT NULL,
                        user_segment TEXT,
                        insight_data TEXT NOT NULL,
                        confidence_score REAL NOT NULL,
                        impact_estimate REAL NOT NULL,
                        action_recommendations TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        applied_at TEXT
                    )
                ''')
                
                # User adaptations table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_adaptations (
                        adaptation_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        adaptation_type TEXT NOT NULL,
                        adaptation_data TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        effectiveness_score REAL DEFAULT 0.0
                    )
                ''')
                
                # Performance metrics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        metric_id TEXT PRIMARY KEY,
                        metric_name TEXT NOT NULL,
                        metric_value REAL NOT NULL,
                        timestamp TEXT NOT NULL,
                        context TEXT
                    )
                ''')
                
                conn.commit()
                logger.info("✅ Database initialized successfully")
                
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    @contextmanager
    def get_database_connection(self):
        """
        Context manager for database connections with proper cleanup.
        Ensures thread-safe database access.
        """
        conn = sqlite3.connect(self.database_path, timeout=30.0)
        try:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        finally:
            conn.close()
    
    async def collect_feedback(self, feedback_data: Dict[str, Any]) -> str:
        """
        Collect and process user feedback from any service in the Aura ecosystem.
        
        Args:
            feedback_data: Dictionary containing feedback information
            
        Returns:
            String feedback ID for tracking
        """
        try:
            # Generate unique feedback ID
            feedback_id = f"feedback_{uuid.uuid4().hex[:12]}_{int(time.time())}"
            
            # Validate required feedback fields
            required_fields = ['user_id', 'feedback_type', 'learning_objective', 'service_source']
            for field in required_fields:
                if field not in feedback_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Create feedback entry
            feedback_entry = FeedbackEntry(
                feedback_id=feedback_id,
                user_id=feedback_data['user_id'],
                session_id=feedback_data.get('session_id', f"session_{int(time.time())}"),
                feedback_type=FeedbackType(feedback_data['feedback_type']),
                learning_objective=LearningObjective(feedback_data['learning_objective']),
                feedback_data=feedback_data.get('data', {}),
                context=feedback_data.get('context', {}),
                timestamp=datetime.now(),
                service_source=feedback_data['service_source'],
                confidence=feedback_data.get('confidence', 1.0)
            )
            
            # Store in database
            await self._store_feedback_entry(feedback_entry)
            
            # Add to processing queue for real-time processing
            self.feedback_queue.append(feedback_entry)
            
            # Start processing thread if not active
            if not self.processing_active:
                await self._start_feedback_processing()
            
            logger.info(f"✅ Feedback collected: {feedback_id} from {feedback_entry.service_source}")
            
            # Update metrics
            self.learning_metrics['total_feedback_processed'] += 1
            
            return feedback_id
            
        except Exception as e:
            logger.error(f"❌ Error collecting feedback: {e}")
            raise
    
    async def _store_feedback_entry(self, feedback_entry: FeedbackEntry):
        """
        Store feedback entry in persistent database.
        
        Args:
            feedback_entry: FeedbackEntry object to store
        """
        try:
            with self.get_database_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO feedback_entries 
                    (feedback_id, user_id, session_id, feedback_type, learning_objective,
                     feedback_data, context, timestamp, service_source, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    feedback_entry.feedback_id,
                    feedback_entry.user_id,
                    feedback_entry.session_id,
                    feedback_entry.feedback_type.value,
                    feedback_entry.learning_objective.value,
                    json.dumps(feedback_entry.feedback_data),
                    json.dumps(feedback_entry.context),
                    feedback_entry.timestamp.isoformat(),
                    feedback_entry.service_source,
                    feedback_entry.confidence
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"❌ Error storing feedback entry: {e}")
            raise
    
    async def _start_feedback_processing(self):
        """
        Start the real-time feedback processing thread.
        Processes feedback queue continuously for immediate learning.
        """
        if self.processing_active:
            return
        
        self.processing_active = True
        self.processing_thread = threading.Thread(
            target=self._process_feedback_queue,
            daemon=True
        )
        self.processing_thread.start()
        logger.info("🔄 Real-time feedback processing started")
    
    def _process_feedback_queue(self):
        """
        Process feedback queue in real-time.
        Runs in separate thread for continuous processing.
        """
        while self.processing_active:
            try:
                if self.feedback_queue:
                    # Process batch of feedback entries
                    batch_size = min(10, len(self.feedback_queue))
                    batch = []
                    
                    for _ in range(batch_size):
                        if self.feedback_queue:
                            batch.append(self.feedback_queue.popleft())
                    
                    if batch:
                        asyncio.run(self._process_feedback_batch(batch))
                
                # Sleep briefly to prevent excessive CPU usage
                time.sleep(1.0)
                
            except Exception as e:
                logger.error(f"❌ Error in feedback processing queue: {e}")
                time.sleep(5.0)  # Wait longer on error
    
    async def _process_feedback_batch(self, feedback_batch: List[FeedbackEntry]):
        """
        Process a batch of feedback entries for learning insights.
        
        Args:
            feedback_batch: List of feedback entries to process
        """
        try:
            logger.info(f"🔄 Processing feedback batch: {len(feedback_batch)} entries")
            
            # Group feedback by learning objective
            objective_groups = defaultdict(list)
            for feedback in feedback_batch:
                objective_groups[feedback.learning_objective].append(feedback)
            
            # Process each learning objective group
            for objective, feedback_list in objective_groups.items():
                await self._process_objective_feedback(objective, feedback_list)
            
            # Update processed status in database
            for feedback in feedback_batch:
                await self._mark_feedback_processed(feedback.feedback_id)
            
            logger.info(f"✅ Feedback batch processed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error processing feedback batch: {e}")
    
    async def _process_objective_feedback(self, objective: LearningObjective, 
                                        feedback_list: List[FeedbackEntry]):
        """
        Process feedback for a specific learning objective.
        
        Args:
            objective: Learning objective to process
            feedback_list: List of feedback entries for this objective
        """
        try:
            logger.info(f"🎯 Processing {len(feedback_list)} feedback entries for {objective.value}")
            
            # Extract features and targets from feedback
            features, targets, user_data = await self._extract_learning_features(feedback_list)
            
            if len(features) == 0:
                logger.warning(f"⚠️ No valid features extracted for {objective.value}")
                return
            
            # Check if we have enough data for learning
            if len(features) < 5:
                logger.info(f"📊 Insufficient data for learning ({len(features)} samples), storing for future training")
                return
            
            # Perform incremental learning
            await self._perform_incremental_learning(objective, features, targets, user_data)
            
            # Generate learning insights
            insights = await self._generate_learning_insights(objective, feedback_list, features, targets)
            
            # Apply immediate adaptations if confidence is high
            for insight in insights:
                if insight.confidence_score > 0.8:
                    await self._apply_learning_insight(insight)
            
        except Exception as e:
            logger.error(f"❌ Error processing objective feedback for {objective.value}: {e}")
    
    async def _extract_learning_features(self, feedback_list: List[FeedbackEntry]) -> Tuple[List[List[float]], List[float], List[Dict]]:
        """
        Extract machine learning features from feedback entries.
        
        Args:
            feedback_list: List of feedback entries to process
            
        Returns:
            Tuple of (features, targets, user_data)
        """
        features = []
        targets = []
        user_data = []
        
        try:
            for feedback in feedback_list:
                # Extract feature vector from feedback data
                feature_vector = await self._create_feature_vector(feedback)
                if feature_vector is not None:
                    features.append(feature_vector)
                    
                    # Extract target value based on feedback type
                    target = self._extract_target_value(feedback)
                    targets.append(target)
                    
                    # Store user context data
                    user_data.append({
                        'user_id': feedback.user_id,
                        'context': feedback.context,
                        'timestamp': feedback.timestamp
                    })
            
            return features, targets, user_data
            
        except Exception as e:
            logger.error(f"❌ Error extracting learning features: {e}")
            return [], [], []
    
    async def _create_feature_vector(self, feedback: FeedbackEntry) -> Optional[List[float]]:
        """
        Create a feature vector from a feedback entry.
        
        Args:
            feedback: Feedback entry to process
            
        Returns:
            List of feature values or None if extraction fails
        """
        try:
            feature_vector = []
            
            # Basic feedback features
            feature_vector.extend([
                feedback.confidence,
                hash(feedback.feedback_type.value) % 1000 / 1000.0,  # Normalized hash
                hash(feedback.service_source) % 1000 / 1000.0,
                len(feedback.feedback_data),
                len(feedback.context)
            ])
            
            # Context-specific features
            context = feedback.context
            feature_vector.extend([
                context.get('session_duration', 0) / 3600.0,  # Normalize to hours
                context.get('items_viewed', 0) / 100.0,  # Normalize
                context.get('previous_interactions', 0) / 50.0,  # Normalize
                1.0 if context.get('returning_user', False) else 0.0,
                context.get('time_of_day', 12) / 24.0  # Normalize to 0-1
            ])
            
            # Feedback data features
            feedback_data = feedback.feedback_data
            if feedback.feedback_type == FeedbackType.EXPLICIT_RATING:
                feature_vector.append(feedback_data.get('rating', 3) / 5.0)  # Normalize 1-5 to 0-1
            else:
                feature_vector.append(0.5)  # Default neutral value
            
            # Service-specific features
            if feedback.service_source == 'recommendation_engine':
                feature_vector.extend([
                    feedback_data.get('recommendation_relevance', 0.5),
                    feedback_data.get('diversity_score', 0.5),
                    feedback_data.get('novelty_score', 0.5)
                ])
            elif feedback.service_source == 'combination_engine':
                feature_vector.extend([
                    feedback_data.get('style_coherence', 0.5),
                    feedback_data.get('color_harmony', 0.5),
                    feedback_data.get('context_appropriateness', 0.5)
                ])
            else:
                feature_vector.extend([0.5, 0.5, 0.5])  # Default values
            
            # Pad or truncate to fixed size (20 features)
            target_size = 20
            if len(feature_vector) < target_size:
                feature_vector.extend([0.0] * (target_size - len(feature_vector)))
            else:
                feature_vector = feature_vector[:target_size]
            
            return feature_vector
            
        except Exception as e:
            logger.error(f"❌ Error creating feature vector: {e}")
            return None
    
    def _extract_target_value(self, feedback: FeedbackEntry) -> float:
        """
        Extract target value for supervised learning from feedback.
        
        Args:
            feedback: Feedback entry to process
            
        Returns:
            Float target value for learning
        """
        try:
            if feedback.feedback_type == FeedbackType.EXPLICIT_RATING:
                # Direct rating (1-5) normalized to 0-1
                return (feedback.feedback_data.get('rating', 3) - 1) / 4.0
            
            elif feedback.feedback_type == FeedbackType.ACCEPTANCE_FEEDBACK:
                # Binary acceptance
                return 1.0 if feedback.feedback_data.get('accepted', False) else 0.0
            
            elif feedback.feedback_type == FeedbackType.REJECTION_FEEDBACK:
                # Binary rejection (inverted)
                return 0.0 if feedback.feedback_data.get('rejected', False) else 1.0
            
            elif feedback.feedback_type == FeedbackType.IMPLICIT_ENGAGEMENT:
                # Engagement score (already 0-1)
                return feedback.feedback_data.get('engagement_score', 0.5)
            
            elif feedback.feedback_type == FeedbackType.BEHAVIORAL_SIGNALS:
                # Behavioral score based on actions
                actions = feedback.feedback_data.get('actions', [])
                positive_actions = sum(1 for action in actions if action in ['like', 'save', 'share', 'purchase'])
                total_actions = len(actions)
                return positive_actions / total_actions if total_actions > 0 else 0.5
            
            else:
                # Default neutral value
                return 0.5
                
        except Exception as e:
            logger.error(f"❌ Error extracting target value: {e}")
            return 0.5
    
    async def _perform_incremental_learning(self, objective: LearningObjective, 
                                          features: List[List[float]], 
                                          targets: List[float],
                                          user_data: List[Dict]):
        """
        Perform incremental learning to update ML models.
        
        Args:
            objective: Learning objective to update
            features: Feature vectors for training
            targets: Target values for supervised learning
            user_data: User context data
        """
        try:
            logger.info(f"🧠 Performing incremental learning for {objective.value}")
            
            # Get the model for this objective
            model = self.ml_models.get(objective.value)
            if model is None:
                logger.warning(f"⚠️ No model found for objective: {objective.value}")
                return
            
            # Convert to numpy arrays
            X = np.array(features)
            y = np.array(targets)
            
            # Scale features
            scaler = self.feature_scalers[objective.value]
            if hasattr(scaler, 'n_features_in_') and scaler.n_features_in_ > 0:
                # Scaler is already fitted, transform features
                X_scaled = scaler.transform(X)
            else:
                # First time fitting scaler
                X_scaled = scaler.fit_transform(X)
            
            # Check if model is already trained
            training_history = self.training_history[objective.value]
            if training_history['last_trained'] is None:
                # Initial training
                logger.info(f"🎯 Initial training for {objective.value}")
                
                # Split data for validation
                if len(X_scaled) > 10:
                    X_train, X_val, y_train, y_val = train_test_split(
                        X_scaled, y, test_size=0.2, random_state=42
                    )
                else:
                    X_train, X_val, y_train, y_val = X_scaled, X_scaled, y, y
                
                # Train model
                model.fit(X_train, y_train)
                
                # Evaluate performance
                if len(X_val) > 0:
                    predictions = model.predict(X_val)
                    if hasattr(model, 'predict_proba'):  # Classification model
                        accuracy = accuracy_score(y_val, predictions > 0.5)
                        training_history['accuracy_history'].append(accuracy)
                        logger.info(f"📊 Initial accuracy for {objective.value}: {accuracy:.3f}")
                    else:  # Regression model
                        mse = mean_squared_error(y_val, predictions)
                        training_history['accuracy_history'].append(1.0 / (1.0 + mse))  # Convert to accuracy-like metric
                        logger.info(f"📊 Initial MSE for {objective.value}: {mse:.3f}")
                
                training_history['last_trained'] = datetime.now()
                training_history['training_samples'] = len(X_scaled)
                
            else:
                # Incremental learning (retrain with new data)
                logger.info(f"🔄 Incremental learning for {objective.value}")
                
                # For tree-based models, we retrain with combined data
                # In a production system, you might use online learning algorithms
                previous_samples = training_history['training_samples']
                
                # Simulate incremental learning by retraining
                model.fit(X_scaled, y)
                
                # Update training history
                training_history['last_trained'] = datetime.now()
                training_history['training_samples'] = previous_samples + len(X_scaled)
                
                # Calculate improvement rate
                if len(training_history['accuracy_history']) > 0:
                    # Simple improvement estimation
                    recent_performance = np.mean(training_history['accuracy_history'][-5:])
                    training_history['improvement_rate'] = min(0.1, recent_performance * 0.05)
            
            # Update metrics
            self.learning_metrics['model_improvements'] += 1
            
            logger.info(f"✅ Incremental learning completed for {objective.value}")
            
        except Exception as e:
            logger.error(f"❌ Error in incremental learning for {objective.value}: {e}")
    
    async def _generate_learning_insights(self, objective: LearningObjective,
                                        feedback_list: List[FeedbackEntry],
                                        features: List[List[float]],
                                        targets: List[float]) -> List[LearningInsight]:
        """
        Generate actionable learning insights from processed feedback.
        
        Args:
            objective: Learning objective being analyzed
            feedback_list: Original feedback entries
            features: Extracted feature vectors
            targets: Target values
            
        Returns:
            List of learning insights with action recommendations
        """
        insights = []
        
        try:
            logger.info(f"💡 Generating learning insights for {objective.value}")
            
            # Analyze user behavior patterns
            user_patterns = self._analyze_user_patterns(feedback_list)
            
            # Analyze feature importance
            feature_importance = self._analyze_feature_importance(objective, features, targets)
            
            # Analyze temporal patterns
            temporal_patterns = self._analyze_temporal_patterns(feedback_list)
            
            # Generate insights based on patterns
            
            # 1. User Segment Insights
            for segment, pattern in user_patterns.items():
                if pattern['confidence'] > 0.7:
                    insight = LearningInsight(
                        insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                        learning_objective=objective,
                        user_segment=segment,
                        insight_data={
                            'pattern_type': 'user_behavior',
                            'pattern_data': pattern,
                            'sample_size': pattern['sample_size']
                        },
                        confidence_score=pattern['confidence'],
                        impact_estimate=pattern['impact_estimate'],
                        action_recommendations=self._generate_user_segment_actions(segment, pattern),
                        created_at=datetime.now()
                    )
                    insights.append(insight)
            
            # 2. Feature Importance Insights
            if feature_importance:
                insight = LearningInsight(
                    insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                    learning_objective=objective,
                    user_segment=None,
                    insight_data={
                        'pattern_type': 'feature_importance',
                        'important_features': feature_importance[:5],  # Top 5 features
                        'total_features': len(feature_importance)
                    },
                    confidence_score=0.8,
                    impact_estimate=0.6,
                    action_recommendations=self._generate_feature_importance_actions(feature_importance),
                    created_at=datetime.now()
                )
                insights.append(insight)
            
            # 3. Temporal Pattern Insights
            for pattern_type, pattern_data in temporal_patterns.items():
                if pattern_data['significance'] > 0.6:
                    insight = LearningInsight(
                        insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                        learning_objective=objective,
                        user_segment=None,
                        insight_data={
                            'pattern_type': f"temporal_{pattern_type}",
                            'pattern_data': pattern_data
                        },
                        confidence_score=pattern_data['significance'],
                        impact_estimate=pattern_data.get('impact_estimate', 0.5),
                        action_recommendations=self._generate_temporal_actions(pattern_type, pattern_data),
                        created_at=datetime.now()
                    )
                    insights.append(insight)
            
            # Store insights in database
            for insight in insights:
                await self._store_learning_insight(insight)
            
            # Update metrics
            self.learning_metrics['learning_insights_generated'] += len(insights)
            
            logger.info(f"✅ Generated {len(insights)} learning insights for {objective.value}")
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ Error generating learning insights: {e}")
            return []
    
    def _analyze_user_patterns(self, feedback_list: List[FeedbackEntry]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze user behavior patterns from feedback data.
        
        Args:
            feedback_list: List of feedback entries to analyze
            
        Returns:
            Dictionary mapping user segments to behavior patterns
        """
        try:
            patterns = {}
            
            # Group feedback by user
            user_feedback = defaultdict(list)
            for feedback in feedback_list:
                user_feedback[feedback.user_id].append(feedback)
            
            # Analyze patterns for users with sufficient data
            for user_id, user_feedbacks in user_feedback.items():
                if len(user_feedbacks) >= 3:  # Minimum feedback for pattern analysis
                    # Calculate user satisfaction trend
                    ratings = []
                    for feedback in user_feedbacks:
                        if feedback.feedback_type == FeedbackType.EXPLICIT_RATING:
                            ratings.append(feedback.feedback_data.get('rating', 3))
                    
                    if ratings:
                        avg_rating = np.mean(ratings)
                        rating_trend = np.polyfit(range(len(ratings)), ratings, 1)[0] if len(ratings) > 1 else 0
                        
                        # Determine user segment based on behavior
                        if avg_rating >= 4.0:
                            segment = 'highly_satisfied'
                        elif avg_rating >= 3.0:
                            segment = 'moderately_satisfied'
                        else:
                            segment = 'low_satisfaction'
                        
                        if segment not in patterns:
                            patterns[segment] = {
                                'users': [],
                                'avg_satisfaction': 0,
                                'satisfaction_trend': 0,
                                'feedback_frequency': 0,
                                'sample_size': 0,
                                'confidence': 0,
                                'impact_estimate': 0
                            }
                        
                        patterns[segment]['users'].append(user_id)
                        patterns[segment]['avg_satisfaction'] += avg_rating
                        patterns[segment]['satisfaction_trend'] += rating_trend
                        patterns[segment]['feedback_frequency'] += len(user_feedbacks)
                        patterns[segment]['sample_size'] += 1
            
            # Calculate averages and confidence scores
            for segment, pattern in patterns.items():
                if pattern['sample_size'] > 0:
                    pattern['avg_satisfaction'] /= pattern['sample_size']
                    pattern['satisfaction_trend'] /= pattern['sample_size']
                    pattern['feedback_frequency'] /= pattern['sample_size']
                    pattern['confidence'] = min(1.0, pattern['sample_size'] / 10.0)  # Higher confidence with more users
                    pattern['impact_estimate'] = pattern['confidence'] * (pattern['avg_satisfaction'] / 5.0)
            
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Error analyzing user patterns: {e}")
            return {}
    
    def _analyze_feature_importance(self, objective: LearningObjective,
                                  features: List[List[float]],
                                  targets: List[float]) -> List[Tuple[int, float]]:
        """
        Analyze feature importance for the given learning objective.
        
        Args:
            objective: Learning objective being analyzed
            features: Feature vectors
            targets: Target values
            
        Returns:
            List of (feature_index, importance_score) tuples sorted by importance
        """
        try:
            model = self.ml_models.get(objective.value)
            if model is None or not hasattr(model, 'feature_importances_'):
                return []
            
            # Get feature importances from the trained model
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                
                # Create list of (index, importance) tuples
                feature_importance = [(i, importance) for i, importance in enumerate(importances)]
                
                # Sort by importance (descending)
                feature_importance.sort(key=lambda x: x[1], reverse=True)
                
                return feature_importance
            
            return []
            
        except Exception as e:
            logger.error(f"❌ Error analyzing feature importance: {e}")
            return []
    
    def _analyze_temporal_patterns(self, feedback_list: List[FeedbackEntry]) -> Dict[str, Dict[str, Any]]:
        """
        Analyze temporal patterns in feedback data.
        
        Args:
            feedback_list: List of feedback entries to analyze
            
        Returns:
            Dictionary mapping pattern types to pattern data
        """
        try:
            patterns = {}
            
            # Convert timestamps to hours of day
            hours = []
            ratings = []
            for feedback in feedback_list:
                if feedback.feedback_type == FeedbackType.EXPLICIT_RATING:
                    hours.append(feedback.timestamp.hour)
                    ratings.append(feedback.feedback_data.get('rating', 3))
            
            if len(hours) >= 5:  # Minimum data for temporal analysis
                # Analyze hourly patterns
                hourly_ratings = defaultdict(list)
                for hour, rating in zip(hours, ratings):
                    hourly_ratings[hour].append(rating)
                
                # Calculate average rating by hour
                hourly_averages = {}
                for hour, hour_ratings in hourly_ratings.items():
                    if len(hour_ratings) >= 2:  # Minimum samples per hour
                        hourly_averages[hour] = np.mean(hour_ratings)
                
                if len(hourly_averages) >= 3:  # Minimum hours with data
                    # Calculate pattern significance
                    avg_ratings = list(hourly_averages.values())
                    pattern_variance = np.var(avg_ratings)
                    significance = min(1.0, pattern_variance / 0.5)  # Normalize variance
                    
                    patterns['hourly_satisfaction'] = {
                        'hourly_averages': hourly_averages,
                        'pattern_variance': pattern_variance,
                        'significance': significance,
                        'impact_estimate': significance * 0.3,  # Temporal patterns have moderate impact
                        'sample_size': len(ratings)
                    }
            
            # Analyze weekly patterns (if enough data)
            if len(feedback_list) >= 10:
                weekdays = []
                weekday_ratings = []
                for feedback in feedback_list:
                    if feedback.feedback_type == FeedbackType.EXPLICIT_RATING:
                        weekdays.append(feedback.timestamp.weekday())
                        weekday_ratings.append(feedback.feedback_data.get('rating', 3))
                
                if len(weekdays) >= 7:
                    weekly_ratings = defaultdict(list)
                    for weekday, rating in zip(weekdays, weekday_ratings):
                        weekly_ratings[weekday].append(rating)
                    
                    weekly_averages = {}
                    for weekday, day_ratings in weekly_ratings.items():
                        if len(day_ratings) >= 2:
                            weekly_averages[weekday] = np.mean(day_ratings)
                    
                    if len(weekly_averages) >= 3:
                        avg_ratings = list(weekly_averages.values())
                        pattern_variance = np.var(avg_ratings)
                        significance = min(1.0, pattern_variance / 0.5)
                        
                        patterns['weekly_satisfaction'] = {
                            'weekly_averages': weekly_averages,
                            'pattern_variance': pattern_variance,
                            'significance': significance,
                            'impact_estimate': significance * 0.2,
                            'sample_size': len(weekday_ratings)
                        }
            
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Error analyzing temporal patterns: {e}")
            return {}
    
    def _generate_user_segment_actions(self, segment: str, pattern: Dict[str, Any]) -> List[str]:
        """
        Generate action recommendations for user segment insights.
        
        Args:
            segment: User segment identifier
            pattern: Pattern data for the segment
            
        Returns:
            List of action recommendation strings
        """
        actions = []
        
        try:
            if segment == 'highly_satisfied':
                actions.extend([
                    "Maintain current service quality for this segment",
                    "Consider using these users as brand advocates",
                    "Explore premium feature offerings",
                    "Gather detailed feedback on success factors"
                ])
            
            elif segment == 'moderately_satisfied':
                actions.extend([
                    "Identify specific pain points for improvement",
                    "Implement targeted engagement campaigns",
                    "Enhance personalization for this segment",
                    "Monitor satisfaction trend changes"
                ])
            
            elif segment == 'low_satisfaction':
                actions.extend([
                    "Immediate intervention required for retention",
                    "Conduct detailed user experience review",
                    "Implement service recovery strategies",
                    "Consider personalized support outreach"
                ])
            
            # Add trend-specific actions
            trend = pattern.get('satisfaction_trend', 0)
            if trend > 0.1:
                actions.append("Capitalize on positive satisfaction trend")
            elif trend < -0.1:
                actions.append("Address declining satisfaction trend urgently")
            
            return actions[:4]  # Limit to top 4 actions
            
        except Exception as e:
            logger.error(f"❌ Error generating user segment actions: {e}")
            return ["Review user segment behavior patterns"]
    
    def _generate_feature_importance_actions(self, feature_importance: List[Tuple[int, float]]) -> List[str]:
        """
        Generate action recommendations based on feature importance analysis.
        
        Args:
            feature_importance: List of (feature_index, importance) tuples
            
        Returns:
            List of action recommendation strings
        """
        actions = []
        
        try:
            if not feature_importance:
                return ["Continue monitoring feature importance"]
            
            # Feature names mapping (based on _create_feature_vector)
            feature_names = [
                'confidence', 'feedback_type', 'service_source', 'feedback_data_size', 'context_size',
                'session_duration', 'items_viewed', 'previous_interactions', 'returning_user', 'time_of_day',
                'rating', 'service_specific_1', 'service_specific_2', 'service_specific_3'
            ]
            
            # Get top 3 most important features
            top_features = feature_importance[:3]
            
            actions.append("Focus optimization efforts on high-impact features:")
            
            for feature_idx, importance in top_features:
                if feature_idx < len(feature_names):
                    feature_name = feature_names[feature_idx]
                    actions.append(f"- Optimize {feature_name} (importance: {importance:.3f})")
            
            # Check for unexpected patterns
            if len(feature_importance) > 5:
                low_importance_features = feature_importance[-3:]
                if any(importance > 0.1 for _, importance in low_importance_features):
                    actions.append("Review unexpectedly important low-priority features")
            
            return actions[:5]  # Limit to top 5 actions
            
        except Exception as e:
            logger.error(f"❌ Error generating feature importance actions: {e}")
            return ["Review feature importance analysis"]
    
    def _generate_temporal_actions(self, pattern_type: str, pattern_data: Dict[str, Any]) -> List[str]:
        """
        Generate action recommendations based on temporal pattern analysis.
        
        Args:
            pattern_type: Type of temporal pattern
            pattern_data: Pattern analysis data
            
        Returns:
            List of action recommendation strings
        """
        actions = []
        
        try:
            if pattern_type == 'hourly_satisfaction':
                hourly_averages = pattern_data.get('hourly_averages', {})
                
                if hourly_averages:
                    # Find best and worst hours
                    best_hour = max(hourly_averages.items(), key=lambda x: x[1])
                    worst_hour = min(hourly_averages.items(), key=lambda x: x[1])
                    
                    actions.extend([
                        f"Peak satisfaction at hour {best_hour[0]} (rating: {best_hour[1]:.2f})",
                        f"Address low satisfaction at hour {worst_hour[0]} (rating: {worst_hour[1]:.2f})",
                        "Consider time-based personalization strategies",
                        "Optimize service availability during peak hours"
                    ])
            
            elif pattern_type == 'weekly_satisfaction':
                weekly_averages = pattern_data.get('weekly_averages', {})
                
                if weekly_averages:
                    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    best_day = max(weekly_averages.items(), key=lambda x: x[1])
                    worst_day = min(weekly_averages.items(), key=lambda x: x[1])
                    
                    best_day_name = weekday_names[best_day[0]] if best_day[0] < 7 else f"Day {best_day[0]}"
                    worst_day_name = weekday_names[worst_day[0]] if worst_day[0] < 7 else f"Day {worst_day[0]}"
                    
                    actions.extend([
                        f"Peak satisfaction on {best_day_name} (rating: {best_day[1]:.2f})",
                        f"Address low satisfaction on {worst_day_name} (rating: {worst_day[1]:.2f})",
                        "Implement day-of-week specific optimizations",
                        "Consider weekly usage pattern adaptations"
                    ])
            
            return actions[:4]  # Limit to top 4 actions
            
        except Exception as e:
            logger.error(f"❌ Error generating temporal actions: {e}")
            return ["Review temporal pattern analysis"]
    
    async def _store_learning_insight(self, insight: LearningInsight):
        """
        Store learning insight in persistent database.
        
        Args:
            insight: LearningInsight object to store
        """
        try:
            with self.get_database_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO learning_insights 
                    (insight_id, learning_objective, user_segment, insight_data,
                     confidence_score, impact_estimate, action_recommendations, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    insight.insight_id,
                    insight.learning_objective.value,
                    insight.user_segment,
                    json.dumps(insight.insight_data),
                    insight.confidence_score,
                    insight.impact_estimate,
                    json.dumps(insight.action_recommendations),
                    insight.created_at.isoformat()
                ))
                conn.commit()
                
                # Store in memory for quick access
                self.learning_insights[insight.insight_id] = insight
                
        except Exception as e:
            logger.error(f"❌ Error storing learning insight: {e}")
    
    async def _apply_learning_insight(self, insight: LearningInsight):
        """
        Apply a learning insight by making adaptive changes to the system.
        
        Args:
            insight: Learning insight to apply
        """
        try:
            logger.info(f"🔧 Applying learning insight: {insight.insight_id}")
            
            # Apply insight based on learning objective
            if insight.learning_objective == LearningObjective.RECOMMENDATION_ACCURACY:
                await self._apply_recommendation_improvements(insight)
            
            elif insight.learning_objective == LearningObjective.STYLE_PROFILING_PRECISION:
                await self._apply_style_profiling_improvements(insight)
            
            elif insight.learning_objective == LearningObjective.COMBINATION_QUALITY:
                await self._apply_combination_improvements(insight)
            
            elif insight.learning_objective == LearningObjective.USER_SATISFACTION:
                await self._apply_satisfaction_improvements(insight)
            
            elif insight.learning_objective == LearningObjective.ENGAGEMENT_OPTIMIZATION:
                await self._apply_engagement_improvements(insight)
            
            # Mark insight as applied
            insight.applied_at = datetime.now()
            await self._update_insight_applied_status(insight.insight_id)
            
            # Update metrics
            self.learning_metrics['adaptations_applied'] += 1
            
            logger.info(f"✅ Learning insight applied successfully: {insight.insight_id}")
            
        except Exception as e:
            logger.error(f"❌ Error applying learning insight: {e}")
    
    async def _apply_recommendation_improvements(self, insight: LearningInsight):
        """
        Apply improvements to the recommendation engine based on learning insights.
        
        Args:
            insight: Learning insight for recommendation improvements
        """
        try:
            # Send adaptation parameters to recommendation engine
            adaptation_data = {
                'insight_id': insight.insight_id,
                'improvement_type': 'accuracy_optimization',
                'parameters': insight.insight_data,
                'confidence': insight.confidence_score
            }
            
            # Make API call to recommendation engine
            response = requests.post(
                f"{self.service_urls['recommendation_engine']}/adapt",
                json=adaptation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Recommendation engine adaptation applied")
            else:
                logger.warning(f"⚠️ Recommendation adaptation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error applying recommendation improvements: {e}")
    
    async def _apply_style_profiling_improvements(self, insight: LearningInsight):
        """
        Apply improvements to style profiling based on learning insights.
        
        Args:
            insight: Learning insight for style profiling improvements
        """
        try:
            # Send adaptation parameters to style profile service
            adaptation_data = {
                'insight_id': insight.insight_id,
                'improvement_type': 'precision_optimization',
                'parameters': insight.insight_data,
                'confidence': insight.confidence_score
            }
            
            response = requests.post(
                f"{self.service_urls['style_profile']}/adapt",
                json=adaptation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Style profiling adaptation applied")
            else:
                logger.warning(f"⚠️ Style profiling adaptation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error applying style profiling improvements: {e}")
    
    async def _apply_combination_improvements(self, insight: LearningInsight):
        """
        Apply improvements to combination engine based on learning insights.
        
        Args:
            insight: Learning insight for combination improvements
        """
        try:
            # Send adaptation parameters to combination engine
            adaptation_data = {
                'insight_id': insight.insight_id,
                'improvement_type': 'quality_optimization',
                'parameters': insight.insight_data,
                'confidence': insight.confidence_score
            }
            
            response = requests.post(
                f"{self.service_urls['combination_engine']}/adapt",
                json=adaptation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Combination engine adaptation applied")
            else:
                logger.warning(f"⚠️ Combination adaptation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error applying combination improvements: {e}")
    
    async def _apply_satisfaction_improvements(self, insight: LearningInsight):
        """
        Apply system-wide improvements to enhance user satisfaction.
        
        Args:
            insight: Learning insight for satisfaction improvements
        """
        try:
            # Apply satisfaction improvements across multiple services
            services_to_update = ['recommendation_engine', 'combination_engine', 'style_profile']
            
            for service in services_to_update:
                adaptation_data = {
                    'insight_id': insight.insight_id,
                    'improvement_type': 'satisfaction_optimization',
                    'parameters': insight.insight_data,
                    'confidence': insight.confidence_score
                }
                
                try:
                    response = requests.post(
                        f"{self.service_urls[service]}/adapt",
                        json=adaptation_data,
                        timeout=5
                    )
                    
                    if response.status_code == 200:
                        logger.info(f"✅ Satisfaction improvement applied to {service}")
                    else:
                        logger.warning(f"⚠️ Satisfaction improvement failed for {service}")
                
                except Exception as service_error:
                    logger.warning(f"⚠️ Could not reach {service} for satisfaction improvement: {service_error}")
                
        except Exception as e:
            logger.error(f"❌ Error applying satisfaction improvements: {e}")
    
    async def _apply_engagement_improvements(self, insight: LearningInsight):
        """
        Apply improvements to optimize user engagement.
        
        Args:
            insight: Learning insight for engagement improvements
        """
        try:
            # Send engagement optimization to orchestrator
            adaptation_data = {
                'insight_id': insight.insight_id,
                'improvement_type': 'engagement_optimization',
                'parameters': insight.insight_data,
                'confidence': insight.confidence_score
            }
            
            response = requests.post(
                f"{self.orchestrator_url}/adapt",
                json=adaptation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Engagement optimization applied to orchestrator")
            else:
                logger.warning(f"⚠️ Engagement optimization failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Error applying engagement improvements: {e}")
    
    async def _mark_feedback_processed(self, feedback_id: str):
        """
        Mark feedback entry as processed in the database.
        
        Args:
            feedback_id: ID of the feedback entry to mark
        """
        try:
            with self.get_database_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE feedback_entries 
                    SET processed = 1 
                    WHERE feedback_id = ?
                ''', (feedback_id,))
                conn.commit()
                
        except Exception as e:
            logger.error(f"❌ Error marking feedback as processed: {e}")
    
    async def _update_insight_applied_status(self, insight_id: str):
        """
        Update learning insight applied status in database.
        
        Args:
            insight_id: ID of the insight to update
        """
        try:
            with self.get_database_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE learning_insights 
                    SET applied_at = ? 
                    WHERE insight_id = ?
                ''', (datetime.now().isoformat(), insight_id))
                conn.commit()
                
        except Exception as e:
            logger.error(f"❌ Error updating insight applied status: {e}")
    
    async def get_learning_analytics(self) -> Dict[str, Any]:
        """
        Get comprehensive learning analytics and system improvement metrics.
        
        Returns:
            Dictionary containing learning performance and improvement data
        """
        try:
            # Get recent feedback statistics
            with self.get_database_connection() as conn:
                cursor = conn.cursor()
                
                # Total feedback count
                cursor.execute('SELECT COUNT(*) FROM feedback_entries')
                total_feedback = cursor.fetchone()[0]
                
                # Processed feedback count
                cursor.execute('SELECT COUNT(*) FROM feedback_entries WHERE processed = 1')
                processed_feedback = cursor.fetchone()[0]
                
                # Learning insights count
                cursor.execute('SELECT COUNT(*) FROM learning_insights')
                total_insights = cursor.fetchone()[0]
                
                # Applied insights count
                cursor.execute('SELECT COUNT(*) FROM learning_insights WHERE applied_at IS NOT NULL')
                applied_insights = cursor.fetchone()[0]
                
                # Recent satisfaction trend
                cursor.execute('''
                    SELECT AVG(CAST(json_extract(feedback_data, '$.rating') AS REAL))
                    FROM feedback_entries 
                    WHERE feedback_type = 'explicit_rating' 
                    AND datetime(timestamp) > datetime('now', '-7 days')
                ''')
                recent_satisfaction = cursor.fetchone()[0] or 0
            
            # Model performance metrics
            model_performance = {}
            for objective in LearningObjective:
                history = self.training_history[objective.value]
                model_performance[objective.value] = {
                    'last_trained': history['last_trained'].isoformat() if history['last_trained'] else None,
                    'training_samples': history['training_samples'],
                    'recent_accuracy': history['accuracy_history'][-1] if history['accuracy_history'] else 0,
                    'improvement_rate': history['improvement_rate']
                }
            
            analytics = {
                'feedback_analytics': {
                    'total_feedback_collected': total_feedback,
                    'processed_feedback': processed_feedback,
                    'processing_rate': (processed_feedback / total_feedback) if total_feedback > 0 else 0,
                    'recent_satisfaction_avg': recent_satisfaction,
                    'feedback_queue_size': len(self.feedback_queue)
                },
                'learning_analytics': {
                    'total_insights_generated': total_insights,
                    'applied_insights': applied_insights,
                    'application_rate': (applied_insights / total_insights) if total_insights > 0 else 0,
                    'active_learning_objectives': len([obj for obj in LearningObjective]),
                    'model_performance': model_performance
                },
                'system_improvements': {
                    'total_adaptations_applied': self.learning_metrics['adaptations_applied'],
                    'model_improvements': self.learning_metrics['model_improvements'],
                    'satisfaction_improvements': len(self.learning_metrics['user_satisfaction_trend']),
                    'engagement_improvements': len(self.learning_metrics['engagement_improvements'])
                },
                'real_time_metrics': {
                    'processing_active': self.processing_active,
                    'learning_insights_in_memory': len(self.learning_insights),
                    'user_adaptations': len(self.user_adaptations),
                    'last_learning_cycle': datetime.now().isoformat()
                }
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"❌ Error generating learning analytics: {e}")
            return {'error': f'Analytics generation failed: {str(e)}'}
    
    async def shutdown(self):
        """
        Gracefully shutdown the feedback processing system.
        Ensures all queued feedback is processed and resources are cleaned up.
        """
        try:
            logger.info("🔄 Shutting down feedback processing system")
            
            # Stop processing thread
            self.processing_active = False
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=10)
            
            # Process remaining feedback in queue
            if self.feedback_queue:
                logger.info(f"🔄 Processing remaining {len(self.feedback_queue)} feedback entries")
                remaining_feedback = list(self.feedback_queue)
                await self._process_feedback_batch(remaining_feedback)
            
            # Shutdown thread pool
            self.executor.shutdown(wait=True)
            
            logger.info("✅ Feedback processing system shutdown complete")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")
