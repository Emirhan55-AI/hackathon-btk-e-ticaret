from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
import logging

logger = logging.getLogger("app.core.di")


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container for the application."""
    
    # Wire the container to modules that need dependencies
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.features.wardrobe.presentation.routers",
            "app.features.style_quiz.presentation.routers",
            "app.features.recommendations.presentation.routers",
            "app.features.ecommerce.presentation.routers",
            "app.features.ecommerce.presentation.cart_routers",
        ]
    )
    
    # Configuration
    config = providers.Configuration()
    
    # Database
    database = providers.Singleton(
        "app.core.database.Database",
        url=config.database_url,
    )
    
    # HTTP Client
    http_client = providers.Singleton(
        "httpx.AsyncClient",
        timeout=30.0,
    )
    
    # Repositories
    auth_repository = providers.Factory(
        "app.features.auth.infrastructure.repositories.AuthRepositoryImpl",
        session_factory=database.provided.session_factory,
    )
    
    wardrobe_repository = providers.Factory(
        "app.features.wardrobe.infrastructure.repositories.WardrobeRepositoryImpl",
        session_factory=database.provided.session_factory,
    )
    
    style_dna_repository = providers.Factory(
        "app.features.style_quiz.infrastructure.repositories.SqlAlchemyStyleDNARepository",
        session_factory=database.provided.session_factory,
    )
    
    recommendations_repository = providers.Factory(
        "app.features.recommendations.infrastructure.repositories.SqlAlchemyRecommendationsRepository",
        session_factory=database.provided.session_factory,
    )
    
    # Use Cases
    login_usecase = providers.Factory(
        "app.features.auth.application.use_cases.LoginUseCase",
        repository=auth_repository,
    )
    
    register_usecase = providers.Factory(
        "app.features.auth.application.use_cases.RegisterUseCase",
        repository=auth_repository,
    )
    
    logout_usecase = providers.Factory(
        "app.features.auth.application.use_cases.LogoutUseCase",
        repository=auth_repository,
    )
    
    refresh_token_usecase = providers.Factory(
        "app.features.auth.application.use_cases.RefreshTokenUseCase",
        repository=auth_repository,
    )
    
    get_current_user_usecase = providers.Factory(
        "app.features.auth.application.use_cases.GetCurrentUserUseCase",
        repository=auth_repository,
    )
    
    update_user_usecase = providers.Factory(
        "app.features.auth.application.use_cases.UpdateUserUseCase",
        repository=auth_repository,
    )
    
    upload_clothing_usecase = providers.Factory(
        "app.features.wardrobe.application.use_cases.UploadClothingUseCase",
        repository=wardrobe_repository,
        http_client=http_client,
    )
    
    get_clothing_list_usecase = providers.Factory(
        "app.features.wardrobe.application.use_cases.GetClothingListUseCase",
        repository=wardrobe_repository,
    )
    
    # Style Quiz Use Cases
    submit_quiz_usecase = providers.Factory(
        "app.features.style_quiz.application.use_cases.SubmitQuizUseCase",
        repository=style_dna_repository,
    )
    
    get_style_dna_usecase = providers.Factory(
        "app.features.style_quiz.application.use_cases.GetStyleDNAUseCase",
        repository=style_dna_repository,
    )
    
    update_style_dna_usecase = providers.Factory(
        "app.features.style_quiz.application.use_cases.UpdateStyleDNAUseCase",
        repository=style_dna_repository,
    )
    
    delete_style_dna_usecase = providers.Factory(
        "app.features.style_quiz.application.use_cases.DeleteStyleDNAUseCase",
        repository=style_dna_repository,
    )
    
    # AI Service Clients
    ai_service_client = providers.Factory(
        "app.features.recommendations.infrastructure.ai_service_client.AIServiceClient",
        base_url=config.ai_service_url,
        api_key=config.ai_service_api_key,
    )
    
    # Recommendations Use Cases
    generate_recommendations_usecase = providers.Factory(
        "app.features.recommendations.application.use_cases.GenerateRecommendationsUseCase",
        ai_client=ai_service_client,
        style_dna_repository=style_dna_repository,
        wardrobe_repository=wardrobe_repository,
    )
    
    generate_quick_recommendations_usecase = providers.Factory(
        "app.features.recommendations.application.use_cases.GenerateQuickRecommendationsUseCase",
        ai_client=ai_service_client,
        style_dna_repository=style_dna_repository,
    )
    
    # E-commerce Repository
    ecommerce_repository = providers.Factory(
        "app.features.ecommerce.infrastructure.repositories.HttpEcommerceRepository",
        base_url=config.ecommerce_api_url,
        api_key=config.ecommerce_api_key,
    )
    
    # Cart Repository
    cart_repository = providers.Factory(
        "app.features.ecommerce.infrastructure.cart_repositories.SqlAlchemyCartRepository",
        session_factory=database.provided.session_factory,
    )
    
    # E-commerce Use Cases
    search_products_use_case = providers.Factory(
        "app.features.ecommerce.application.use_cases.SearchProductsUseCase",
        repository=ecommerce_repository,
    )
    
    get_product_by_id_use_case = providers.Factory(
        "app.features.ecommerce.application.use_cases.GetProductByIdUseCase",
        repository=ecommerce_repository,
    )
    
    get_trending_products_use_case = providers.Factory(
        "app.features.ecommerce.application.use_cases.GetTrendingProductsUseCase",
        repository=ecommerce_repository,
    )
    
    get_product_recommendations_use_case = providers.Factory(
        "app.features.ecommerce.application.use_cases.GetProductRecommendationsUseCase",
        repository=ecommerce_repository,
    )
    
    # Cart Use Cases
    add_to_cart_use_case = providers.Factory(
        "app.features.ecommerce.application.cart_use_cases.AddToCartUseCase",
        repository=cart_repository,
    )
    
    get_cart_use_case = providers.Factory(
        "app.features.ecommerce.application.cart_use_cases.GetCartUseCase",
        repository=cart_repository,
    )
    
    update_cart_item_use_case = providers.Factory(
        "app.features.ecommerce.application.cart_use_cases.UpdateCartItemUseCase",
        repository=cart_repository,
    )
    
    remove_from_cart_use_case = providers.Factory(
        "app.features.ecommerce.application.cart_use_cases.RemoveFromCartUseCase",
        repository=cart_repository,
    )
    
    clear_cart_use_case = providers.Factory(
        "app.features.ecommerce.application.cart_use_cases.ClearCartUseCase",
        repository=cart_repository,
    )


# Global container instance
container = Container()


def setup_container() -> None:
    """Setup and configure the DI container."""
    try:
        from app.core.config import settings
        
        # Configure the container with settings
        container.config.from_dict({
            "database_url": settings.database_url,
            "ai_service_url": settings.ai_service_url,
            "ai_service_api_key": settings.ai_service_api_key,
            "ecommerce_api_url": settings.ecommerce_api_url,
            "ecommerce_api_key": settings.ecommerce_api_key,
        })
        
        # Wire the container
        container.wire(modules=[
            "app.features.auth.presentation.routers",
            "app.features.wardrobe.presentation.routers",
            "app.features.style_quiz.presentation.routers",
            "app.features.recommendations.presentation.routers",
            "app.features.ecommerce.presentation.routers",
            "app.features.ecommerce.presentation.cart_routers",
        ])
        
        logger.info("Dependency injection container configured successfully")
        
    except Exception as e:
        logger.error(f"Failed to setup DI container: {e}")
        raise


def get_container() -> Container:
    """Get the global container instance."""
    return container


# Helper functions for accessing use cases (for dependencies)
def get_auth_repository():
    """Get auth repository instance."""
    return container.auth_repository()


def get_login_usecase():
    """Get login use case instance."""
    return container.login_usecase()


def get_register_usecase():
    """Get register use case instance."""
    return container.register_usecase()


def get_logout_usecase():
    """Get logout use case instance."""
    return container.logout_usecase()


def get_refresh_token_usecase():
    """Get refresh token use case instance."""
    return container.refresh_token_usecase()


def get_get_current_user_usecase():
    """Get current user use case instance."""
    return container.get_current_user_usecase()


def get_update_user_usecase():
    """Get update user use case instance."""
    return container.update_user_usecase()
