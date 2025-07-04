"""
Agent cache module for storing VacationChatAgent instances with TTL.
"""
import time
import asyncio
from typing import Dict, Tuple, Optional
import logging

from agents.vacation_agent import VacationChatAgent

logger = logging.getLogger(__name__)

class AgentCache:
    """Cache for VacationChatAgent instances with TTL."""
    
    def __init__(self, ttl_seconds: int = 3600):
        """Initialize the agent cache.
        
        Args:
            ttl_seconds: Time to live in seconds for each agent instance (default: 1 hour)
        """
        self._cache: Dict[str, Tuple[VacationChatAgent, float]] = {}
        self._ttl_seconds = ttl_seconds
        self._lock = asyncio.Lock()
        
    async def get(self, session_id: str) -> VacationChatAgent:
        """Get an agent instance from the cache or create a new one if not exists.
        
        Args:
            session_id: The session ID to look up
            
        Returns:
            The agent instance (either existing or newly created)
        """
        async with self._lock:
            # Check if we have a cached agent
            if session_id in self._cache:
                agent, timestamp = self._cache[session_id]
                current_time = time.time()
                
                # Check if the agent has expired
                if current_time - timestamp > self._ttl_seconds:
                    logger.info(f"Agent for session {session_id} has expired")
                    del self._cache[session_id]
                else:
                    # Update the timestamp to extend the TTL
                    self._cache[session_id] = (agent, current_time)
                    return agent
            
            # Create new agent if not found or expired
            logger.info(f"Creating new agent for session {session_id}")
            agent = VacationChatAgent()
            self._cache[session_id] = (agent, time.time())
            return agent
    
    async def put(self, session_id: str, agent: VacationChatAgent) -> None:
        """Store an agent instance in the cache.
        
        Args:
            session_id: The session ID to associate with the agent
            agent: The agent instance to store
        """
        async with self._lock:
            self._cache[session_id] = (agent, time.time())
            logger.info(f"Stored agent for session {session_id}")
    
    async def exists(self, session_id: str) -> bool:
        """Check if a session exists in the cache.
        
        Args:
            session_id: The session ID to check
            
        Returns:
            True if the session exists and is not expired, False otherwise
        """
        async with self._lock:
            if session_id in self._cache:
                _, timestamp = self._cache[session_id]
                current_time = time.time()
                # Check if the agent has expired
                if current_time - timestamp > self._ttl_seconds:
                    return False
                return True
            return False
        
    async def cleanup_expired(self) -> None:
        """Remove expired agent instances from the cache."""
        current_time = time.time()
        expired_keys = []
        
        async with self._lock:
            for session_id, (_, timestamp) in self._cache.items():
                if current_time - timestamp > self._ttl_seconds:
                    expired_keys.append(session_id)
            
            for session_id in expired_keys:
                del self._cache[session_id]
                
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired agent instances")
    
    @property
    def size(self) -> int:
        """Get the current number of agent instances in the cache."""
        return len(self._cache)

class AgentCacheManager:
    """Manager for agent cache with background cleanup task."""
    
    def __init__(self):
        self.cache = AgentCache()
        self._cleanup_task = None
        
    async def get(self, session_id: str) -> VacationChatAgent:
        """Get an agent instance from the cache."""
        return await self.cache.get(session_id)
        
    async def put(self, session_id: str, agent: VacationChatAgent) -> None:
        """Store an agent instance in the cache."""
        await self.cache.put(session_id, agent)
    
    async def exists(self, session_id: str) -> bool:
        """Check if a session exists in the cache."""
        return await self.cache.exists(session_id)
        
    async def cleanup_expired(self) -> None:
        """Remove expired agent instances from the cache."""
        await self.cache.cleanup_expired()
        
    @property
    def size(self) -> int:
        """Get the current number of agent instances in the cache."""
        return self.cache.size
        
    def start_cleanup_task(self, app=None):
        """Start background task for cache cleanup."""
        async def cleanup_loop():
            while True:
                await asyncio.sleep(300)  # Run every 5 minutes
                await self.cleanup_expired()
                logger.info(f"Cache cleanup complete. Current size: {self.size}")
                
        if app:
            # Register with FastAPI app lifecycle
            @app.on_event("startup")
            async def start_cache_cleanup():
                self._cleanup_task = asyncio.create_task(cleanup_loop())
                logger.info("Started agent cache cleanup task")
                
            @app.on_event("shutdown")
            async def stop_cache_cleanup():
                if self._cleanup_task:
                    self._cleanup_task.cancel()
                    logger.info("Stopped agent cache cleanup task")
        else:
            # Start immediately without FastAPI
            self._cleanup_task = asyncio.create_task(cleanup_loop())
            logger.info("Started agent cache cleanup task")
            
    def stop_cleanup_task(self):
        """Stop the background cleanup task."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None
            logger.info("Stopped agent cache cleanup task")

# Singleton instance
agent_cache = AgentCacheManager()
