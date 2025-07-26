from datetime import datetime
from typing import Dict, Any, Optional
import uuid
import logging

from app.features.style_quiz.domain.entities import StyleDNA
from app.features.style_quiz.infrastructure.repositories import StyleDNARepository

logger = logging.getLogger(__name__)


class SubmitQuizUseCase:
    """Use case for submitting style quiz responses."""
    
    def __init__(self, repository: StyleDNARepository):
        self._repository = repository
    
    async def execute(self, user_id: uuid.UUID, quiz_responses: Dict[str, Any]) -> StyleDNA:
        """
        Execute the submit quiz use case.
        
        Args:
            user_id: The ID of the user submitting the quiz
            quiz_responses: The user's quiz responses
        
        Returns:
            StyleDNA: The created or updated StyleDNA entity
        """
        try:
            logger.info(f"Processing quiz submission for user {user_id}")
            
            # Check if user already has StyleDNA
            existing_style_dna = await self._repository.get_by_user_id(user_id)
            
            if existing_style_dna:
                # Update existing StyleDNA
                logger.info(f"Updating existing StyleDNA for user {user_id}")
                updated_style_dna = existing_style_dna.update_from_quiz(quiz_responses)
                return await self._repository.save(updated_style_dna)
            else:
                # Create new StyleDNA
                logger.info(f"Creating new StyleDNA for user {user_id}")
                new_style_dna = StyleDNA.create_from_quiz(user_id, quiz_responses)
                return await self._repository.save(new_style_dna)
                
        except Exception as e:
            logger.error(f"Error processing quiz submission for user {user_id}: {e}")
            raise


class GetStyleDNAUseCase:
    """Use case for retrieving user's StyleDNA profile."""
    
    def __init__(self, repository: StyleDNARepository):
        self._repository = repository
    
    async def execute(self, user_id: uuid.UUID) -> Optional[StyleDNA]:
        """
        Execute the get StyleDNA use case.
        
        Args:
            user_id: The ID of the user
        
        Returns:
            StyleDNA: The user's StyleDNA if it exists, None otherwise
        """
        try:
            logger.info(f"Retrieving StyleDNA for user {user_id}")
            return await self._repository.get_by_user_id(user_id)
        except Exception as e:
            logger.error(f"Error retrieving StyleDNA for user {user_id}: {e}")
            raise


class UpdateStyleDNAUseCase:
    """Use case for updating user's StyleDNA profile."""
    
    def __init__(self, repository: StyleDNARepository):
        self._repository = repository
    
    async def execute(
        self, 
        user_id: uuid.UUID, 
        updates: Dict[str, Any]
    ) -> Optional[StyleDNA]:
        """
        Execute the update StyleDNA use case.
        
        Args:
            user_id: The ID of the user
            updates: Dictionary of fields to update
        
        Returns:
            StyleDNA: The updated StyleDNA if it exists, None otherwise
        """
        try:
            logger.info(f"Updating StyleDNA for user {user_id}")
            
            existing_style_dna = await self._repository.get_by_user_id(user_id)
            if not existing_style_dna:
                logger.warning(f"No StyleDNA found for user {user_id}")
                return None
            
            # Update the StyleDNA with provided fields
            updated_style_dna = existing_style_dna.update_profile(updates)
            return await self._repository.save(updated_style_dna)
            
        except Exception as e:
            logger.error(f"Error updating StyleDNA for user {user_id}: {e}")
            raise


class DeleteStyleDNAUseCase:
    """Use case for deleting user's StyleDNA profile."""
    
    def __init__(self, repository: StyleDNARepository):
        self._repository = repository
    
    async def execute(self, user_id: uuid.UUID) -> bool:
        """
        Execute the delete StyleDNA use case.
        
        Args:
            user_id: The ID of the user
        
        Returns:
            bool: True if deleted successfully, False if not found
        """
        try:
            logger.info(f"Deleting StyleDNA for user {user_id}")
            return await self._repository.delete_by_user_id(user_id)
        except Exception as e:
            logger.error(f"Error deleting StyleDNA for user {user_id}: {e}")
            raise
