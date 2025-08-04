# 🧠 AURA AI - INTELLIGENT WORKFLOW OPTIMIZER (PHASE 8)
# Bu modül, makine öğrenmesi ile akıllı iş akışı optimizasyonu sağlar
# ML-powered workflow routing ve performance optimization yapar

# asyncio - asenkron ML optimization operations için temel kütüphane
import asyncio
# aiohttp - asenkron HTTP client ML model communication için
import aiohttp
# json - JSON veri işleme ve ML model configuration için
import json
# uuid - unique identifier generation for optimization sessions
import uuid
# time - timing and performance measurement for optimization analysis
import time
# datetime - timestamp creation for optimization tracking and analytics
from datetime import datetime, timedelta
# typing - type hints for ML optimization components and data structures
from typing import Dict, List, Any, Optional, Union, Tuple
# dataclasses - structured data classes for optimization results and metrics
from dataclasses import dataclass, field
# enum - enumeration types for optimization strategies and decision types
from enum import Enum
# logging - comprehensive logging system for optimization operations
import logging
# threading - thread management for parallel optimization analysis
import threading
# statistics - statistical functions for performance analysis and predictions
import statistics
# random - random sampling for ML training and optimization experiments
import random
# math - mathematical functions for optimization algorithms
import math

# Import ML infrastructure components for model integration
from ml_infrastructure import (
    AuraMLInfrastructure, AuraMLModel, MLModelType, MLFeatureSet,
    aura_ml_infrastructure, create_workflow_optimizer
)

# Import workflow orchestration components for optimization integration
from workflow_orchestrator import (
    AuraWorkflowOrchestrator, WorkflowDefinition, WorkflowStep, WorkflowContext,
    aura_orchestrator
)

# Set up comprehensive logging for intelligent workflow optimization
# This logger tracks all ML-powered optimization decisions and performance improvements
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('aura_intelligent_workflow_optimizer')

class OptimizationStrategy(Enum):
    """
    Enumeration of optimization strategies for intelligent workflow management.
    Each strategy represents a different approach to workflow performance improvement.
    """
    # Minimize end-to-end latency for fastest response times
    LATENCY_MINIMIZATION = "latency_minimization"
    # Maximize throughput for highest request processing capacity
    THROUGHPUT_MAXIMIZATION = "throughput_maximization"
    # Optimize resource utilization for cost efficiency
    RESOURCE_EFFICIENCY = "resource_efficiency"
    # Balance performance and cost for optimal business value
    BALANCED_OPTIMIZATION = "balanced_optimization"
    # Maximize reliability and success rate
    RELIABILITY_MAXIMIZATION = "reliability_maximization"
    # Optimize for user experience and satisfaction
    USER_EXPERIENCE_OPTIMIZATION = "user_experience_optimization"

class OptimizationDecision(Enum):
    """
    Enumeration of optimization decisions that can be made by the intelligent system.
    Represents actionable recommendations for workflow improvement.
    """
    # Change service routing order for better performance
    REORDER_SERVICES = "reorder_services"
    # Adjust parallelization level for optimal throughput
    ADJUST_PARALLELIZATION = "adjust_parallelization"
    # Modify resource allocation for services
    REALLOCATE_RESOURCES = "reallocate_resources"
    # Switch to alternative service implementation
    SWITCH_SERVICE_IMPLEMENTATION = "switch_service_implementation"
    # Enable or disable caching for specific steps
    MODIFY_CACHING_STRATEGY = "modify_caching_strategy"
    # Adjust timeout values for better reliability
    OPTIMIZE_TIMEOUTS = "optimize_timeouts"
    # Scale service instances up or down
    SCALE_SERVICES = "scale_services"
    # No optimization needed, current configuration is optimal
    NO_OPTIMIZATION_NEEDED = "no_optimization_needed"

@dataclass
class WorkflowPerformanceData:
    """
    Data class containing comprehensive performance data for workflow analysis.
    Used by ML models to make intelligent optimization decisions.
    """
    # Unique identifier for this performance data record
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # Workflow identifier that this performance data relates to
    workflow_id: str = ""
    # Total execution time for the complete workflow in milliseconds
    total_execution_time_ms: float = 0.0
    # Individual service execution times for detailed analysis
    service_execution_times: Dict[str, float] = field(default_factory=dict)
    # Service latencies including network and processing time
    service_latencies: Dict[str, float] = field(default_factory=dict)
    # Success rate for the workflow execution (0.0 to 1.0)
    success_rate: float = 1.0
    # Error count and types encountered during execution
    error_count: int = 0
    error_types: List[str] = field(default_factory=list)
    # Resource utilization metrics for optimization analysis
    resource_utilization: Dict[str, float] = field(default_factory=dict)
    # Parallelization factor used in this execution
    parallelization_factor: float = 1.0
    # User context information for personalized optimization
    user_context: Dict[str, Any] = field(default_factory=dict)
    # Timestamp when this performance data was recorded
    timestamp: datetime = field(default_factory=datetime.now)
    # Business metrics relevant to optimization decisions
    business_metrics: Dict[str, float] = field(default_factory=dict)

@dataclass
class OptimizationRecommendation:
    """
    Data class representing an intelligent optimization recommendation.
    Contains actionable suggestions for improving workflow performance.
    """
    # Unique identifier for this optimization recommendation
    recommendation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # Type of optimization decision being recommended
    decision_type: OptimizationDecision = OptimizationDecision.NO_OPTIMIZATION_NEEDED
    # Optimization strategy this recommendation supports
    strategy: OptimizationStrategy = OptimizationStrategy.BALANCED_OPTIMIZATION
    # Detailed parameters for implementing this recommendation
    optimization_parameters: Dict[str, Any] = field(default_factory=dict)
    # Expected performance improvement from this optimization
    expected_improvement: Dict[str, float] = field(default_factory=dict)
    # Confidence score for this recommendation (0.0 to 1.0)
    confidence_score: float = 0.0
    # Implementation priority (higher values = more important)
    priority: int = 1
    # Estimated implementation effort (1=easy, 5=complex)
    implementation_effort: int = 1
    # Risk assessment for this optimization (1=low risk, 5=high risk)
    risk_level: int = 1
    # Justification explaining why this optimization is recommended
    justification: str = ""
    # Timestamp when this recommendation was generated
    created_at: datetime = field(default_factory=datetime.now)
    # Expected ROI or business value from this optimization
    business_value: Dict[str, float] = field(default_factory=dict)

class IntelligentWorkflowOptimizer:
    """
    Main class for AI-powered workflow optimization using machine learning.
    Analyzes workflow performance and provides intelligent recommendations for improvement.
    """
    
    def __init__(self, optimization_strategy: OptimizationStrategy = OptimizationStrategy.BALANCED_OPTIMIZATION):
        """
        Initialize the intelligent workflow optimizer with ML model integration.
        
        Args:
            optimization_strategy: Primary optimization strategy to focus on
        """
        # Primary optimization strategy guiding all decisions
        self.optimization_strategy = optimization_strategy
        # ML model for workflow optimization predictions and recommendations
        self.ml_model: Optional[AuraMLModel] = None
        # Historical performance data for ML training and analysis
        self.performance_history: List[WorkflowPerformanceData] = []
        # Cache of optimization recommendations for quick lookup
        self.recommendation_cache: Dict[str, OptimizationRecommendation] = {}
        # Thread lock for safe concurrent access to optimizer state
        self._lock = threading.Lock()
        # Optimization metrics and statistics
        self.optimizer_metrics = {
            'total_optimizations': 0,
            'successful_optimizations': 0,
            'average_improvement_percentage': 0.0,
            'total_recommendations': 0,
            'implemented_recommendations': 0,
            'ml_model_accuracy': 0.0,
            'optimization_sessions': 0
        }
        # Integration with workflow orchestrator for real-time optimization
        self.orchestrator_integration = True
        # Background optimization task for continuous improvement
        self.continuous_optimization_enabled = True
        self.optimization_task: Optional[asyncio.Task] = None
        
        # Log optimizer initialization
        logger.info(f"Intelligent Workflow Optimizer initialized with strategy: {optimization_strategy.value}")
    
    async def initialize_ml_model(self, model_id: str = None) -> bool:
        """
        Initialize and train the ML model for workflow optimization.
        Sets up machine learning capabilities for intelligent decision making.
        
        Args:
            model_id: Optional custom model ID for the ML model
            
        Returns:
            bool: True if model initialization successful, False otherwise
        """
        try:
            # Create workflow optimizer ML model
            if model_id is None:
                model_id = f"intelligent_workflow_optimizer_{uuid.uuid4().hex[:8]}"
            
            logger.info(f"Initializing ML model for intelligent workflow optimization: {model_id}")
            
            # Create and register ML model with optimized configuration
            self.ml_model = await create_workflow_optimizer(model_id)
            
            # Generate initial training data if no historical data exists
            if len(self.performance_history) < 50:
                logger.info("Generating synthetic training data for ML model initialization")
                synthetic_training_data = await self._generate_synthetic_training_data(100)
                synthetic_validation_data = await self._generate_synthetic_training_data(30)
                
                # Convert performance data to ML feature sets
                training_features = [self._convert_performance_to_features(data) for data in synthetic_training_data]
                validation_features = [self._convert_performance_to_features(data) for data in synthetic_validation_data]
                
                # Train ML model with synthetic data
                training_success = await aura_ml_infrastructure.train_model(
                    model_id, training_features, validation_features
                )
                
                if training_success:
                    self.optimizer_metrics['ml_model_accuracy'] = self.ml_model.metrics.validation_accuracy
                    logger.info(f"ML model trained successfully - Accuracy: {self.ml_model.metrics.validation_accuracy:.2f}%")
                else:
                    logger.error("Failed to train ML model for workflow optimization")
                    return False
            
            # Start continuous optimization if enabled
            if self.continuous_optimization_enabled:
                await self._start_continuous_optimization()
            
            logger.info("✅ Intelligent Workflow Optimizer ML model initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize ML model for workflow optimization: {str(e)}")
            return False
    
    async def analyze_workflow_performance(self, workflow_id: str, execution_data: Dict[str, Any]) -> WorkflowPerformanceData:
        """
        Analyze workflow execution performance and extract insights for optimization.
        Creates structured performance data for ML model analysis.
        
        Args:
            workflow_id: Identifier of the workflow being analyzed
            execution_data: Raw execution data from workflow orchestrator
            
        Returns:
            WorkflowPerformanceData: Structured performance analysis results
        """
        logger.debug(f"Analyzing workflow performance for: {workflow_id}")
        
        # Extract performance metrics from execution data
        total_execution_time = execution_data.get('total_execution_time_ms', 0.0)
        service_times = execution_data.get('service_execution_times', {})
        service_latencies = execution_data.get('service_latencies', {})
        success_rate = execution_data.get('success_rate', 1.0)
        errors = execution_data.get('errors', [])
        resource_usage = execution_data.get('resource_utilization', {})
        parallelization = execution_data.get('parallelization_factor', 1.0)
        user_context = execution_data.get('user_context', {})
        
        # Create structured performance data
        performance_data = WorkflowPerformanceData(
            workflow_id=workflow_id,
            total_execution_time_ms=total_execution_time,
            service_execution_times=service_times,
            service_latencies=service_latencies,
            success_rate=success_rate,
            error_count=len(errors),
            error_types=[error.get('type', 'unknown') for error in errors],
            resource_utilization=resource_usage,
            parallelization_factor=parallelization,
            user_context=user_context,
            business_metrics=self._calculate_business_metrics(execution_data)
        )
        
        # Store performance data for ML training and analysis
        with self._lock:
            self.performance_history.append(performance_data)
            # Keep only recent performance data to prevent memory bloat
            if len(self.performance_history) > 10000:
                self.performance_history = self.performance_history[-5000:]
        
        logger.debug(f"Performance analysis completed for workflow {workflow_id} - "
                    f"Execution time: {total_execution_time:.2f}ms, Success rate: {success_rate:.2%}")
        
        return performance_data
    
    async def generate_optimization_recommendations(self, workflow_id: str, 
                                                  performance_data: WorkflowPerformanceData) -> List[OptimizationRecommendation]:
        """
        Generate intelligent optimization recommendations using ML analysis.
        Provides actionable suggestions for improving workflow performance.
        
        Args:
            workflow_id: Identifier of the workflow to optimize
            performance_data: Current performance data for analysis
            
        Returns:
            List of optimization recommendations ranked by priority and confidence
        """
        logger.info(f"Generating optimization recommendations for workflow: {workflow_id}")
        
        recommendations = []
        
        try:
            # Use ML model for intelligent optimization if available
            if self.ml_model and self.ml_model.state.value in ['ready', 'serving']:
                ml_recommendations = await self._generate_ml_recommendations(performance_data)
                recommendations.extend(ml_recommendations)
            
            # Generate rule-based recommendations as fallback or supplement
            rule_based_recommendations = await self._generate_rule_based_recommendations(performance_data)
            recommendations.extend(rule_based_recommendations)
            
            # Remove duplicate recommendations and merge similar ones
            recommendations = self._deduplicate_recommendations(recommendations)
            
            # Rank recommendations by priority, confidence, and business value
            recommendations = self._rank_recommendations(recommendations)
            
            # Cache recommendations for quick lookup
            for rec in recommendations:
                self.recommendation_cache[rec.recommendation_id] = rec
            
            # Update optimizer metrics
            self.optimizer_metrics['total_recommendations'] += len(recommendations)
            
            logger.info(f"Generated {len(recommendations)} optimization recommendations for workflow {workflow_id}")
            
            # Log top recommendation for monitoring
            if recommendations:
                top_rec = recommendations[0]
                logger.info(f"Top recommendation: {top_rec.decision_type.value} - "
                          f"Confidence: {top_rec.confidence_score:.2f}, "
                          f"Expected improvement: {top_rec.expected_improvement}")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate optimization recommendations for workflow {workflow_id}: {str(e)}")
            return []
    
    async def implement_optimization(self, recommendation: OptimizationRecommendation, 
                                   workflow_id: str) -> Dict[str, Any]:
        """
        Implement an optimization recommendation in the workflow orchestrator.
        Applies ML-driven improvements to actual workflow configuration.
        
        Args:
            recommendation: Optimization recommendation to implement
            workflow_id: Target workflow for optimization implementation
            
        Returns:
            Dict containing implementation results and status
        """
        logger.info(f"Implementing optimization recommendation: {recommendation.decision_type.value} "
                   f"for workflow {workflow_id}")
        
        implementation_start = time.time()
        
        try:
            # Apply optimization based on decision type
            if recommendation.decision_type == OptimizationDecision.REORDER_SERVICES:
                result = await self._implement_service_reordering(recommendation, workflow_id)
                
            elif recommendation.decision_type == OptimizationDecision.ADJUST_PARALLELIZATION:
                result = await self._implement_parallelization_adjustment(recommendation, workflow_id)
                
            elif recommendation.decision_type == OptimizationDecision.REALLOCATE_RESOURCES:
                result = await self._implement_resource_reallocation(recommendation, workflow_id)
                
            elif recommendation.decision_type == OptimizationDecision.MODIFY_CACHING_STRATEGY:
                result = await self._implement_caching_optimization(recommendation, workflow_id)
                
            elif recommendation.decision_type == OptimizationDecision.OPTIMIZE_TIMEOUTS:
                result = await self._implement_timeout_optimization(recommendation, workflow_id)
                
            elif recommendation.decision_type == OptimizationDecision.SCALE_SERVICES:
                result = await self._implement_service_scaling(recommendation, workflow_id)
                
            else:
                # Handle other optimization types or no optimization needed
                result = {
                    'status': 'skipped',
                    'reason': f'Optimization type {recommendation.decision_type.value} not implemented',
                    'success': True
                }
            
            # Calculate implementation duration
            implementation_duration = time.time() - implementation_start
            
            # Update metrics based on implementation result
            if result.get('success', False):
                self.optimizer_metrics['successful_optimizations'] += 1
                self.optimizer_metrics['implemented_recommendations'] += 1
            
            self.optimizer_metrics['total_optimizations'] += 1
            
            # Create comprehensive implementation result
            implementation_result = {
                'recommendation_id': recommendation.recommendation_id,
                'workflow_id': workflow_id,
                'decision_type': recommendation.decision_type.value,
                'implementation_status': result.get('status', 'unknown'),
                'success': result.get('success', False),
                'implementation_duration_ms': implementation_duration * 1000,
                'changes_applied': result.get('changes_applied', {}),
                'expected_improvement': recommendation.expected_improvement,
                'implementation_timestamp': datetime.now().isoformat(),
                'error_details': result.get('error_details', None)
            }
            
            logger.info(f"Optimization implementation completed - "
                       f"Status: {result.get('status', 'unknown')}, "
                       f"Success: {result.get('success', False)}, "
                       f"Duration: {implementation_duration:.3f}s")
            
            return implementation_result
            
        except Exception as e:
            logger.error(f"Failed to implement optimization recommendation: {str(e)}")
            return {
                'recommendation_id': recommendation.recommendation_id,
                'workflow_id': workflow_id,
                'success': False,
                'error': str(e),
                'implementation_timestamp': datetime.now().isoformat()
            }
    
    async def _generate_ml_recommendations(self, performance_data: WorkflowPerformanceData) -> List[OptimizationRecommendation]:
        """
        Generate optimization recommendations using machine learning model predictions.
        Leverages trained ML model for intelligent optimization decisions.
        
        Args:
            performance_data: Performance data for ML analysis
            
        Returns:
            List of ML-generated optimization recommendations
        """
        if not self.ml_model:
            return []
        
        try:
            # Convert performance data to ML feature set
            feature_set = self._convert_performance_to_features(performance_data)
            
            # Get ML model prediction for optimization
            prediction_result = await aura_ml_infrastructure.predict(self.ml_model.model_id, feature_set)
            
            # Extract prediction and confidence
            prediction = prediction_result['prediction']
            confidence = prediction_result['confidence']
            
            recommendations = []
            
            # Interpret ML prediction and create recommendations
            if 'optimal_routing' in prediction:
                # Service reordering recommendation
                rec = OptimizationRecommendation(
                    decision_type=OptimizationDecision.REORDER_SERVICES,
                    strategy=self.optimization_strategy,
                    optimization_parameters={
                        'new_service_order': prediction['optimal_routing'],
                        'current_order': list(performance_data.service_execution_times.keys())
                    },
                    expected_improvement={
                        'latency_reduction_ms': prediction.get('expected_latency_ms', 0) - performance_data.total_execution_time_ms,
                        'latency_reduction_percentage': (
                            (performance_data.total_execution_time_ms - prediction.get('expected_latency_ms', performance_data.total_execution_time_ms)) /
                            performance_data.total_execution_time_ms * 100
                        )
                    },
                    confidence_score=confidence,
                    priority=3,
                    implementation_effort=2,
                    risk_level=1,
                    justification=f"ML model predicts {prediction.get('expected_latency_ms', 0):.0f}ms execution time with reordered services"
                )
                recommendations.append(rec)
            
            if 'resource_allocation' in prediction:
                # Resource reallocation recommendation
                rec = OptimizationRecommendation(
                    decision_type=OptimizationDecision.REALLOCATE_RESOURCES,
                    strategy=self.optimization_strategy,
                    optimization_parameters={
                        'cpu_cores': prediction['resource_allocation'].get('cpu_cores', 2),
                        'memory_gb': prediction['resource_allocation'].get('memory_gb', 4)
                    },
                    expected_improvement={
                        'resource_efficiency_improvement': 15.0,
                        'cost_reduction_percentage': 10.0
                    },
                    confidence_score=confidence * 0.9,  # Slightly lower confidence for resource changes
                    priority=2,
                    implementation_effort=3,
                    risk_level=2,
                    justification="ML model recommends resource reallocation for optimal performance"
                )
                recommendations.append(rec)
            
            if 'parallelization_factor' in prediction:
                # Parallelization adjustment recommendation
                target_parallelization = prediction['parallelization_factor']
                if abs(target_parallelization - performance_data.parallelization_factor) > 0.2:
                    rec = OptimizationRecommendation(
                        decision_type=OptimizationDecision.ADJUST_PARALLELIZATION,
                        strategy=self.optimization_strategy,
                        optimization_parameters={
                            'new_parallelization_factor': target_parallelization,
                            'current_parallelization_factor': performance_data.parallelization_factor
                        },
                        expected_improvement={
                            'throughput_improvement_percentage': (target_parallelization - performance_data.parallelization_factor) * 25,
                            'latency_reduction_ms': max(0, (performance_data.parallelization_factor - target_parallelization) * 50)
                        },
                        confidence_score=confidence,
                        priority=2,
                        implementation_effort=1,
                        risk_level=1,
                        justification=f"ML model recommends parallelization factor of {target_parallelization:.1f}"
                    )
                    recommendations.append(rec)
            
            logger.debug(f"Generated {len(recommendations)} ML-based recommendations with average confidence {confidence:.2f}")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate ML recommendations: {str(e)}")
            return []
    
    async def _generate_rule_based_recommendations(self, performance_data: WorkflowPerformanceData) -> List[OptimizationRecommendation]:
        """
        Generate optimization recommendations using rule-based analysis.
        Provides fallback recommendations when ML model is not available.
        
        Args:
            performance_data: Performance data for rule-based analysis
            
        Returns:
            List of rule-based optimization recommendations
        """
        recommendations = []
        
        # Analyze execution time for latency optimization
        if performance_data.total_execution_time_ms > 500:  # Above 500ms threshold
            if self.optimization_strategy in [OptimizationStrategy.LATENCY_MINIMIZATION, OptimizationStrategy.BALANCED_OPTIMIZATION]:
                # Recommend service reordering based on execution times
                service_times = performance_data.service_execution_times
                if service_times:
                    # Sort services by execution time (fastest first)
                    optimal_order = sorted(service_times.keys(), key=lambda x: service_times[x])
                    current_order = list(service_times.keys())
                    
                    if optimal_order != current_order:
                        rec = OptimizationRecommendation(
                            decision_type=OptimizationDecision.REORDER_SERVICES,
                            strategy=self.optimization_strategy,
                            optimization_parameters={
                                'new_service_order': optimal_order,
                                'current_order': current_order
                            },
                            expected_improvement={
                                'latency_reduction_ms': performance_data.total_execution_time_ms * 0.15,
                                'latency_reduction_percentage': 15.0
                            },
                            confidence_score=0.75,
                            priority=3,
                            implementation_effort=2,
                            risk_level=1,
                            justification="Reorder services by execution time for better pipeline efficiency"
                        )
                        recommendations.append(rec)
        
        # Analyze resource utilization for efficiency optimization
        resource_usage = performance_data.resource_utilization
        if resource_usage:
            cpu_usage = resource_usage.get('cpu', 0.0)
            memory_usage = resource_usage.get('memory', 0.0)
            
            # High resource usage optimization
            if cpu_usage > 0.8 or memory_usage > 0.85:
                rec = OptimizationRecommendation(
                    decision_type=OptimizationDecision.SCALE_SERVICES,
                    strategy=self.optimization_strategy,
                    optimization_parameters={
                        'scale_direction': 'up',
                        'scale_factor': 1.5,
                        'target_cpu_usage': 0.7,
                        'target_memory_usage': 0.75
                    },
                    expected_improvement={
                        'latency_reduction_ms': performance_data.total_execution_time_ms * 0.25,
                        'throughput_improvement_percentage': 30.0
                    },
                    confidence_score=0.85,
                    priority=4,
                    implementation_effort=3,
                    risk_level=2,
                    justification=f"High resource usage detected - CPU: {cpu_usage:.1%}, Memory: {memory_usage:.1%}"
                )
                recommendations.append(rec)
            
            # Low resource usage optimization (scale down)
            elif cpu_usage < 0.3 and memory_usage < 0.4:
                rec = OptimizationRecommendation(
                    decision_type=OptimizationDecision.SCALE_SERVICES,
                    strategy=self.optimization_strategy,
                    optimization_parameters={
                        'scale_direction': 'down',
                        'scale_factor': 0.8,
                        'target_cpu_usage': 0.6,
                        'target_memory_usage': 0.6
                    },
                    expected_improvement={
                        'cost_reduction_percentage': 20.0,
                        'resource_efficiency_improvement': 25.0
                    },
                    confidence_score=0.70,
                    priority=2,
                    implementation_effort=2,
                    risk_level=1,
                    justification=f"Low resource usage detected - CPU: {cpu_usage:.1%}, Memory: {memory_usage:.1%}"
                )
                recommendations.append(rec)
        
        # Analyze parallelization for throughput optimization
        if performance_data.parallelization_factor < 2.0 and len(performance_data.service_execution_times) > 2:
            if self.optimization_strategy in [OptimizationStrategy.THROUGHPUT_MAXIMIZATION, OptimizationStrategy.BALANCED_OPTIMIZATION]:
                rec = OptimizationRecommendation(
                    decision_type=OptimizationDecision.ADJUST_PARALLELIZATION,
                    strategy=self.optimization_strategy,
                    optimization_parameters={
                        'new_parallelization_factor': min(3.0, len(performance_data.service_execution_times)),
                        'current_parallelization_factor': performance_data.parallelization_factor
                    },
                    expected_improvement={
                        'throughput_improvement_percentage': 40.0,
                        'latency_reduction_ms': performance_data.total_execution_time_ms * 0.2
                    },
                    confidence_score=0.80,
                    priority=3,
                    implementation_effort=1,
                    risk_level=1,
                    justification="Increase parallelization to improve throughput"
                )
                recommendations.append(rec)
        
        # Analyze error rate for reliability optimization
        if performance_data.success_rate < 0.95:  # Below 95% success rate
            rec = OptimizationRecommendation(
                decision_type=OptimizationDecision.OPTIMIZE_TIMEOUTS,
                strategy=self.optimization_strategy,
                optimization_parameters={
                    'increase_timeout_percentage': 25.0,
                    'add_retry_logic': True,
                    'retry_count': 3
                },
                expected_improvement={
                    'success_rate_improvement': (0.98 - performance_data.success_rate) * 100,
                    'reliability_score_improvement': 15.0
                },
                confidence_score=0.85,
                priority=5,
                implementation_effort=2,
                risk_level=1,
                justification=f"Low success rate ({performance_data.success_rate:.1%}) requires timeout and retry optimization"
            )
            recommendations.append(rec)
        
        logger.debug(f"Generated {len(recommendations)} rule-based recommendations")
        
        return recommendations
    
    def _convert_performance_to_features(self, performance_data: WorkflowPerformanceData) -> MLFeatureSet:
        """
        Convert workflow performance data to ML feature set for model training/inference.
        Transforms business metrics into ML-compatible feature format.
        
        Args:
            performance_data: Raw performance data to convert
            
        Returns:
            MLFeatureSet: Structured feature set for ML model consumption
        """
        # Extract and normalize features for ML model
        features = {
            'execution_time': performance_data.total_execution_time_ms,
            'service_latencies': list(performance_data.service_latencies.values()),
            'success_rate': performance_data.success_rate,
            'resource_usage': performance_data.resource_utilization,
            'workflow_complexity': len(performance_data.service_execution_times),
            'parallelization_factor': performance_data.parallelization_factor,
            'error_count': performance_data.error_count,
            'average_service_time': statistics.mean(performance_data.service_execution_times.values()) if performance_data.service_execution_times else 0.0,
            'max_service_time': max(performance_data.service_execution_times.values()) if performance_data.service_execution_times else 0.0,
            'min_service_time': min(performance_data.service_execution_times.values()) if performance_data.service_execution_times else 0.0
        }
        
        # Add derived features for better ML model performance
        if performance_data.service_execution_times:
            service_times = list(performance_data.service_execution_times.values())
            features['service_time_variance'] = statistics.variance(service_times) if len(service_times) > 1 else 0.0
            features['service_time_std_dev'] = statistics.stdev(service_times) if len(service_times) > 1 else 0.0
        
        # Add resource efficiency metrics
        if performance_data.resource_utilization:
            cpu_usage = performance_data.resource_utilization.get('cpu', 0.0)
            memory_usage = performance_data.resource_utilization.get('memory', 0.0)
            features['resource_efficiency_score'] = (cpu_usage + memory_usage) / 2.0
            features['resource_imbalance'] = abs(cpu_usage - memory_usage)
        
        # Create ML feature set
        feature_set = MLFeatureSet(
            feature_set_id=f"workflow_perf_{performance_data.record_id}",
            name=f"Workflow Performance Features - {performance_data.workflow_id}",
            description="Performance features extracted from workflow execution for optimization analysis",
            features=features,
            timestamp=performance_data.timestamp
        )
        
        return feature_set
    
    async def _generate_synthetic_training_data(self, num_samples: int) -> List[WorkflowPerformanceData]:
        """
        Generate synthetic training data for ML model initialization.
        Creates realistic performance data for model training when historical data is insufficient.
        
        Args:
            num_samples: Number of synthetic samples to generate
            
        Returns:
            List of synthetic workflow performance data
        """
        synthetic_data = []
        
        for i in range(num_samples):
            # Generate realistic performance metrics
            base_execution_time = random.uniform(200, 800)  # 200-800ms base time
            num_services = random.randint(3, 6)
            
            # Generate service execution times that sum to approximately base time
            service_times = {}
            service_latencies = {}
            for j in range(num_services):
                service_name = f"service_{j+1}"
                exec_time = random.uniform(30, 150)
                service_times[service_name] = exec_time
                service_latencies[service_name] = exec_time + random.uniform(5, 25)  # Add network latency
            
            # Adjust total time to match base time approximately
            time_adjustment = base_execution_time / sum(service_times.values())
            service_times = {k: v * time_adjustment for k, v in service_times.items()}
            service_latencies = {k: v * time_adjustment for k, v in service_latencies.items()}
            
            # Generate other realistic metrics
            success_rate = random.uniform(0.85, 1.0)
            error_count = 0 if success_rate > 0.95 else random.randint(1, 5)
            resource_usage = {
                'cpu': random.uniform(0.2, 0.9),
                'memory': random.uniform(0.3, 0.85),
                'network': random.uniform(0.1, 0.6)
            }
            parallelization = random.uniform(1.0, 3.0)
            
            # Create synthetic performance data
            perf_data = WorkflowPerformanceData(
                workflow_id=f"synthetic_workflow_{i}",
                total_execution_time_ms=sum(service_times.values()),
                service_execution_times=service_times,
                service_latencies=service_latencies,
                success_rate=success_rate,
                error_count=error_count,
                error_types=['timeout', 'connection_error', 'validation_error'][:error_count],
                resource_utilization=resource_usage,
                parallelization_factor=parallelization,
                user_context={'context': random.choice(['casual', 'formal', 'sport'])},
                timestamp=datetime.now() - timedelta(minutes=random.randint(0, 10080))  # Within last week
            )
            
            synthetic_data.append(perf_data)
        
        logger.debug(f"Generated {num_samples} synthetic training data samples")
        return synthetic_data
    
    def _calculate_business_metrics(self, execution_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate business impact metrics from execution data.
        Translates technical performance into business value measurements.
        
        Args:
            execution_data: Raw execution data from workflow
            
        Returns:
            Dict containing business impact metrics
        """
        business_metrics = {}
        
        # User satisfaction score based on response time
        response_time = execution_data.get('total_execution_time_ms', 0.0)
        if response_time <= 200:
            user_satisfaction = 1.0
        elif response_time <= 500:
            user_satisfaction = 0.9 - (response_time - 200) / 300 * 0.2
        else:
            user_satisfaction = max(0.5, 0.7 - (response_time - 500) / 1000 * 0.2)
        
        business_metrics['user_satisfaction_score'] = user_satisfaction
        
        # Cost efficiency based on resource usage
        resource_usage = execution_data.get('resource_utilization', {})
        if resource_usage:
            avg_resource_usage = statistics.mean(resource_usage.values())
            # Optimal usage around 70% - calculate efficiency
            optimal_usage = 0.7
            efficiency = 1.0 - abs(avg_resource_usage - optimal_usage) / optimal_usage
            business_metrics['cost_efficiency_score'] = max(0.0, efficiency)
        
        # Revenue impact based on success rate and speed
        success_rate = execution_data.get('success_rate', 1.0)
        speed_factor = max(0.5, 1.0 - response_time / 2000)  # Normalize speed impact
        business_metrics['revenue_impact_score'] = (success_rate * 0.7) + (speed_factor * 0.3)
        
        return business_metrics
    
    def _deduplicate_recommendations(self, recommendations: List[OptimizationRecommendation]) -> List[OptimizationRecommendation]:
        """
        Remove duplicate and conflicting optimization recommendations.
        Ensures recommendation list contains only unique, non-conflicting suggestions.
        
        Args:
            recommendations: List of recommendations to deduplicate
            
        Returns:
            List of unique, non-conflicting recommendations
        """
        # Group recommendations by decision type
        grouped_recs = {}
        for rec in recommendations:
            decision_type = rec.decision_type
            if decision_type not in grouped_recs:
                grouped_recs[decision_type] = []
            grouped_recs[decision_type].append(rec)
        
        # Keep only the highest confidence recommendation for each decision type
        deduplicated = []
        for decision_type, recs in grouped_recs.items():
            best_rec = max(recs, key=lambda r: r.confidence_score)
            deduplicated.append(best_rec)
        
        return deduplicated
    
    def _rank_recommendations(self, recommendations: List[OptimizationRecommendation]) -> List[OptimizationRecommendation]:
        """
        Rank optimization recommendations by priority, confidence, and business value.
        Orders recommendations to maximize implementation impact and success probability.
        
        Args:
            recommendations: List of recommendations to rank
            
        Returns:
            List of recommendations sorted by ranking score (highest first)
        """
        def ranking_score(rec: OptimizationRecommendation) -> float:
            # Composite ranking score based on multiple factors
            confidence_weight = 0.3
            priority_weight = 0.25
            business_value_weight = 0.25
            implementation_ease_weight = 0.1
            risk_weight = -0.1  # Lower risk is better
            
            # Normalize priority (1-5 scale)
            priority_score = rec.priority / 5.0
            
            # Calculate business value score from expected improvements
            business_value = 0.0
            if rec.expected_improvement:
                for metric, value in rec.expected_improvement.items():
                    if 'percentage' in metric or 'improvement' in metric:
                        business_value += value
                business_value = min(business_value / 100.0, 1.0)  # Normalize to 0-1
            
            # Implementation ease (inverse of effort)
            implementation_ease = (6 - rec.implementation_effort) / 5.0
            
            # Risk factor (inverse - lower risk is better)
            risk_factor = (6 - rec.risk_level) / 5.0
            
            # Calculate composite score
            total_score = (
                rec.confidence_score * confidence_weight +
                priority_score * priority_weight +
                business_value * business_value_weight +
                implementation_ease * implementation_ease_weight +
                risk_factor * risk_weight
            )
            
            return total_score
        
        # Sort recommendations by ranking score (highest first)
        ranked_recommendations = sorted(recommendations, key=ranking_score, reverse=True)
        
        return ranked_recommendations
    
    async def _implement_service_reordering(self, recommendation: OptimizationRecommendation, workflow_id: str) -> Dict[str, Any]:
        """
        Implement service reordering optimization in workflow configuration.
        Updates workflow definition with optimized service execution order.
        
        Args:
            recommendation: Service reordering recommendation
            workflow_id: Target workflow identifier
            
        Returns:
            Dict containing implementation results
        """
        try:
            new_order = recommendation.optimization_parameters.get('new_service_order', [])
            current_order = recommendation.optimization_parameters.get('current_order', [])
            
            logger.info(f"Implementing service reordering for workflow {workflow_id}: {current_order} -> {new_order}")
            
            # In a real implementation, this would update the workflow definition
            # For simulation, we'll just log the change and return success
            changes_applied = {
                'previous_service_order': current_order,
                'new_service_order': new_order,
                'reordered_services': len(new_order)
            }
            
            # Simulate implementation delay
            await asyncio.sleep(0.1)
            
            return {
                'status': 'completed',
                'success': True,
                'changes_applied': changes_applied,
                'optimization_type': 'service_reordering'
            }
            
        except Exception as e:
            logger.error(f"Failed to implement service reordering: {str(e)}")
            return {
                'status': 'failed',
                'success': False,
                'error_details': str(e)
            }
    
    async def _implement_parallelization_adjustment(self, recommendation: OptimizationRecommendation, workflow_id: str) -> Dict[str, Any]:
        """
        Implement parallelization adjustment optimization in workflow configuration.
        Updates workflow parallel execution settings for optimal throughput.
        
        Args:
            recommendation: Parallelization adjustment recommendation
            workflow_id: Target workflow identifier
            
        Returns:
            Dict containing implementation results
        """
        try:
            new_factor = recommendation.optimization_parameters.get('new_parallelization_factor', 1.0)
            current_factor = recommendation.optimization_parameters.get('current_parallelization_factor', 1.0)
            
            logger.info(f"Implementing parallelization adjustment for workflow {workflow_id}: {current_factor:.1f} -> {new_factor:.1f}")
            
            changes_applied = {
                'previous_parallelization_factor': current_factor,
                'new_parallelization_factor': new_factor,
                'improvement_factor': new_factor / current_factor
            }
            
            # Simulate implementation delay
            await asyncio.sleep(0.05)
            
            return {
                'status': 'completed',
                'success': True,
                'changes_applied': changes_applied,
                'optimization_type': 'parallelization_adjustment'
            }
            
        except Exception as e:
            logger.error(f"Failed to implement parallelization adjustment: {str(e)}")
            return {
                'status': 'failed', 
                'success': False,
                'error_details': str(e)
            }
    
    async def _implement_resource_reallocation(self, recommendation: OptimizationRecommendation, workflow_id: str) -> Dict[str, Any]:
        """
        Implement resource reallocation optimization for workflow services.
        Updates resource allocation settings for optimal performance and cost.
        
        Args:
            recommendation: Resource reallocation recommendation
            workflow_id: Target workflow identifier
            
        Returns:
            Dict containing implementation results
        """
        try:
            cpu_cores = recommendation.optimization_parameters.get('cpu_cores', 2)
            memory_gb = recommendation.optimization_parameters.get('memory_gb', 4)
            
            logger.info(f"Implementing resource reallocation for workflow {workflow_id}: CPU={cpu_cores}, Memory={memory_gb}GB")
            
            changes_applied = {
                'new_cpu_allocation': cpu_cores,
                'new_memory_allocation_gb': memory_gb,
                'resource_optimization': True
            }
            
            # Simulate implementation delay
            await asyncio.sleep(0.2)
            
            return {
                'status': 'completed',
                'success': True,
                'changes_applied': changes_applied,
                'optimization_type': 'resource_reallocation'
            }
            
        except Exception as e:
            logger.error(f"Failed to implement resource reallocation: {str(e)}")
            return {
                'status': 'failed',
                'success': False,
                'error_details': str(e)
            }
    
    async def _implement_caching_optimization(self, recommendation: OptimizationRecommendation, workflow_id: str) -> Dict[str, Any]:
        """
        Implement caching strategy optimization for improved performance.
        Updates caching configuration based on optimization recommendations.
        
        Args:
            recommendation: Caching optimization recommendation
            workflow_id: Target workflow identifier
            
        Returns:
            Dict containing implementation results
        """
        try:
            logger.info(f"Implementing caching optimization for workflow {workflow_id}")
            
            changes_applied = {
                'caching_enabled': True,
                'cache_strategy': 'intelligent',
                'cache_ttl_seconds': 300
            }
            
            # Simulate implementation delay
            await asyncio.sleep(0.1)
            
            return {
                'status': 'completed',
                'success': True,
                'changes_applied': changes_applied,
                'optimization_type': 'caching_optimization'
            }
            
        except Exception as e:
            logger.error(f"Failed to implement caching optimization: {str(e)}")
            return {
                'status': 'failed',
                'success': False,
                'error_details': str(e)
            }
    
    async def _implement_timeout_optimization(self, recommendation: OptimizationRecommendation, workflow_id: str) -> Dict[str, Any]:
        """
        Implement timeout optimization for improved reliability.
        Updates timeout and retry configuration based on recommendations.
        
        Args:
            recommendation: Timeout optimization recommendation
            workflow_id: Target workflow identifier
            
        Returns:
            Dict containing implementation results
        """
        try:
            timeout_increase = recommendation.optimization_parameters.get('increase_timeout_percentage', 25.0)
            add_retry = recommendation.optimization_parameters.get('add_retry_logic', True)
            retry_count = recommendation.optimization_parameters.get('retry_count', 3)
            
            logger.info(f"Implementing timeout optimization for workflow {workflow_id}: +{timeout_increase}% timeout, retries={retry_count}")
            
            changes_applied = {
                'timeout_increase_percentage': timeout_increase,
                'retry_logic_enabled': add_retry,
                'max_retry_count': retry_count
            }
            
            # Simulate implementation delay
            await asyncio.sleep(0.1)
            
            return {
                'status': 'completed',
                'success': True,
                'changes_applied': changes_applied,
                'optimization_type': 'timeout_optimization'
            }
            
        except Exception as e:
            logger.error(f"Failed to implement timeout optimization: {str(e)}")
            return {
                'status': 'failed',
                'success': False,
                'error_details': str(e)
            }
    
    async def _implement_service_scaling(self, recommendation: OptimizationRecommendation, workflow_id: str) -> Dict[str, Any]:
        """
        Implement service scaling optimization for performance and cost efficiency.
        Updates service instance scaling based on predicted demand.
        
        Args:
            recommendation: Service scaling recommendation
            workflow_id: Target workflow identifier
            
        Returns:
            Dict containing implementation results
        """
        try:
            scale_direction = recommendation.optimization_parameters.get('scale_direction', 'maintain')
            scale_factor = recommendation.optimization_parameters.get('scale_factor', 1.0)
            
            logger.info(f"Implementing service scaling for workflow {workflow_id}: {scale_direction} by {scale_factor}x")
            
            changes_applied = {
                'scaling_direction': scale_direction,
                'scaling_factor': scale_factor,
                'auto_scaling_enabled': True
            }
            
            # Simulate implementation delay
            await asyncio.sleep(0.3)
            
            return {
                'status': 'completed',
                'success': True,
                'changes_applied': changes_applied,
                'optimization_type': 'service_scaling'
            }
            
        except Exception as e:
            logger.error(f"Failed to implement service scaling: {str(e)}")
            return {
                'status': 'failed',
                'success': False,
                'error_details': str(e)
            }
    
    async def _start_continuous_optimization(self):
        """
        Start background continuous optimization process.
        Monitors performance and applies optimizations automatically.
        """
        if self.optimization_task and not self.optimization_task.done():
            return  # Already running
        
        self.optimization_task = asyncio.create_task(self._continuous_optimization_loop())
        logger.info("Started continuous workflow optimization process")
    
    async def _continuous_optimization_loop(self):
        """
        Background loop for continuous workflow optimization.
        Periodically analyzes performance and applies improvements.
        """
        logger.info("Continuous optimization loop started")
        
        while self.continuous_optimization_enabled:
            try:
                # Wait for optimization interval
                await asyncio.sleep(300)  # 5 minutes between optimization cycles
                
                # Analyze recent performance data
                if len(self.performance_history) > 10:
                    recent_data = self.performance_history[-10:]  # Last 10 executions
                    
                    # Look for optimization opportunities
                    for perf_data in recent_data:
                        if perf_data.total_execution_time_ms > 400:  # Above threshold
                            recommendations = await self.generate_optimization_recommendations(
                                perf_data.workflow_id, perf_data
                            )
                            
                            # Implement high-confidence, low-risk recommendations automatically
                            for rec in recommendations:
                                if rec.confidence_score > 0.85 and rec.risk_level <= 2:
                                    await self.implement_optimization(rec, perf_data.workflow_id)
                                    break  # Implement one optimization at a time
                
                self.optimizer_metrics['optimization_sessions'] += 1
                
            except Exception as e:
                logger.error(f"Error in continuous optimization loop: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying
    
    def get_optimizer_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive metrics for the intelligent workflow optimizer.
        Provides performance statistics and optimization effectiveness data.
        
        Returns:
            Dict containing all optimizer metrics and statistics
        """
        with self._lock:
            metrics = self.optimizer_metrics.copy()
            
            # Calculate derived metrics
            if metrics['total_optimizations'] > 0:
                success_rate = metrics['successful_optimizations'] / metrics['total_optimizations'] * 100
            else:
                success_rate = 0.0
            
            if metrics['total_recommendations'] > 0:
                implementation_rate = metrics['implemented_recommendations'] / metrics['total_recommendations'] * 100
            else:
                implementation_rate = 0.0
            
            # Add current state information
            metrics.update({
                'optimizer_strategy': self.optimization_strategy.value,
                'ml_model_available': self.ml_model is not None,
                'ml_model_state': self.ml_model.state.value if self.ml_model else 'not_available',
                'performance_history_size': len(self.performance_history),
                'cached_recommendations': len(self.recommendation_cache),
                'continuous_optimization_enabled': self.continuous_optimization_enabled,
                'optimization_success_rate': success_rate,
                'recommendation_implementation_rate': implementation_rate,
                'timestamp': datetime.now().isoformat()
            })
            
            return metrics

# Global intelligent workflow optimizer instance
# This provides centralized AI-powered workflow optimization for AURA system
aura_intelligent_optimizer = IntelligentWorkflowOptimizer()

# Helper functions for easy optimization integration

async def optimize_workflow_performance(workflow_id: str, execution_data: Dict[str, Any]) -> List[OptimizationRecommendation]:
    """
    Convenience function to analyze workflow performance and get optimization recommendations.
    Provides simple interface for workflow optimization integration.
    
    Args:
        workflow_id: Identifier of the workflow to optimize
        execution_data: Performance data from workflow execution
        
    Returns:
        List of optimization recommendations for the workflow
    """
    # Analyze performance data
    performance_data = await aura_intelligent_optimizer.analyze_workflow_performance(workflow_id, execution_data)
    
    # Generate optimization recommendations
    recommendations = await aura_intelligent_optimizer.generate_optimization_recommendations(workflow_id, performance_data)
    
    return recommendations

async def apply_best_optimization(workflow_id: str, recommendations: List[OptimizationRecommendation]) -> Optional[Dict[str, Any]]:
    """
    Convenience function to apply the best optimization recommendation.
    Automatically selects and implements the highest-priority recommendation.
    
    Args:
        workflow_id: Target workflow for optimization
        recommendations: List of available optimization recommendations
        
    Returns:
        Implementation result for the applied optimization, or None if no optimization applied
    """
    if not recommendations:
        return None
    
    # Get the best recommendation (list is already sorted by priority)
    best_recommendation = recommendations[0]
    
    # Implement the best recommendation
    result = await aura_intelligent_optimizer.implement_optimization(best_recommendation, workflow_id)
    
    return result

# Main execution function for testing intelligent workflow optimizer
async def main():
    """
    Main function demonstrating intelligent workflow optimizer capabilities.
    Shows ML-powered workflow analysis and optimization recommendations.
    """
    logger.info("🧠 AURA AI - PHASE 8: INTELLIGENT WORKFLOW OPTIMIZER DEMONSTRATION")
    logger.info("=" * 80)
    
    try:
        # Initialize ML model for optimization
        logger.info("Initializing ML model for intelligent optimization...")
        ml_init_success = await aura_intelligent_optimizer.initialize_ml_model()
        
        if ml_init_success:
            logger.info("✅ ML model initialized successfully for workflow optimization")
        else:
            logger.warning("⚠️ ML model initialization failed, using rule-based optimization")
        
        # Simulate workflow performance data for demonstration
        logger.info("Simulating workflow performance analysis...")
        
        sample_execution_data = {
            'total_execution_time_ms': 650.0,
            'service_execution_times': {
                'image_processing': 180.0,
                'nlu_service': 150.0,
                'style_profile': 120.0,
                'combination_engine': 110.0,
                'recommendation_engine': 90.0
            },
            'service_latencies': {
                'image_processing': 195.0,
                'nlu_service': 165.0,
                'style_profile': 135.0,
                'combination_engine': 125.0,
                'recommendation_engine': 105.0
            },
            'success_rate': 0.92,
            'errors': [
                {'type': 'timeout', 'service': 'image_processing'},
                {'type': 'validation_error', 'service': 'nlu_service'}
            ],
            'resource_utilization': {
                'cpu': 0.85,
                'memory': 0.78,
                'network': 0.45
            },
            'parallelization_factor': 1.5,
            'user_context': {
                'context': 'casual',
                'user_type': 'premium'
            }
        }
        
        # Analyze workflow performance
        performance_data = await aura_intelligent_optimizer.analyze_workflow_performance(
            "demo_complete_fashion_analysis", sample_execution_data
        )
        
        logger.info(f"Performance analysis completed - "
                   f"Execution time: {performance_data.total_execution_time_ms:.1f}ms, "
                   f"Success rate: {performance_data.success_rate:.1%}")
        
        # Generate optimization recommendations
        logger.info("Generating intelligent optimization recommendations...")
        recommendations = await aura_intelligent_optimizer.generate_optimization_recommendations(
            "demo_complete_fashion_analysis", performance_data
        )
        
        # Display recommendations
        logger.info(f"Generated {len(recommendations)} optimization recommendations:")
        for i, rec in enumerate(recommendations, 1):
            logger.info(f"  {i}. {rec.decision_type.value}")
            logger.info(f"     Confidence: {rec.confidence_score:.2f}, Priority: {rec.priority}")
            logger.info(f"     Expected improvement: {rec.expected_improvement}")
            logger.info(f"     Justification: {rec.justification}")
        
        # Implement best recommendation
        if recommendations:
            logger.info("Implementing best optimization recommendation...")
            best_rec = recommendations[0]
            implementation_result = await aura_intelligent_optimizer.implement_optimization(
                best_rec, "demo_complete_fashion_analysis"
            )
            
            logger.info(f"Implementation result: {implementation_result['implementation_status']}")
            logger.info(f"Success: {implementation_result['success']}")
            if implementation_result.get('changes_applied'):
                logger.info(f"Changes applied: {implementation_result['changes_applied']}")
        
        # Display optimizer metrics
        logger.info("Getting optimizer performance metrics...")
        metrics = aura_intelligent_optimizer.get_optimizer_metrics()
        
        logger.info("🏆 INTELLIGENT OPTIMIZER METRICS:")
        logger.info(f"  Optimization Strategy: {metrics['optimizer_strategy']}")
        logger.info(f"  ML Model Available: {metrics['ml_model_available']}")
        logger.info(f"  Total Optimizations: {metrics['total_optimizations']}")
        logger.info(f"  Success Rate: {metrics['optimization_success_rate']:.1f}%")
        logger.info(f"  Total Recommendations: {metrics['total_recommendations']}")
        logger.info(f"  Implementation Rate: {metrics['recommendation_implementation_rate']:.1f}%")
        logger.info(f"  Performance History: {metrics['performance_history_size']} records")
        
        logger.info("✅ Intelligent Workflow Optimizer demonstration completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Intelligent Workflow Optimizer demonstration error: {str(e)}")
        raise

if __name__ == "__main__":
    # Run the intelligent workflow optimizer demonstration
    asyncio.run(main())
