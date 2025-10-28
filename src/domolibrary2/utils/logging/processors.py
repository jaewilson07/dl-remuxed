"""
Custom logging processors for domolibrary2.

This module contains result processors and extractors specifically designed
for domolibrary2 components to provide better logging integration.
"""

from typing import Any, Optional

from dc_logger.client.extractors import ResultProcessor
from dc_logger.client.models import HTTPDetails

from ...client import response as rgd


class ResponseGetDataProcessor(ResultProcessor):
    """Custom result processor for ResponseGetData objects."""
    
    def _sanitize_headers(self, headers: dict) -> dict:
        """Sanitize sensitive headers for logging."""
        if not headers:
            return headers
        
        sanitized = headers.copy()
        sensitive_headers = [
            'x-domo-developer-token',
            'authorization',
            'x-api-key',
            'cookie',
            'set-cookie'
        ]
        
        for header_name in sensitive_headers:
            # Case-insensitive check
            for key in list(sanitized.keys()):
                if key.lower() == header_name.lower():
                    sanitized[key] = "***"
                    break
        
        return sanitized
    
    def _format_response_body(self, response: Any) -> Any:
        """Format response body appropriately for logging."""
        if isinstance(response, dict):
            # Return dictionary as-is for proper JSON formatting
            return response
        elif isinstance(response, list):
            # Return list as-is for proper JSON formatting
            return response
        elif isinstance(response, (str, bytes)):
            # Try to parse as JSON if it looks like JSON
            try:
                import json
                response_str = str(response)
                # Check if it looks like JSON
                if response_str.strip().startswith(('{', '[')):
                    parsed = json.loads(response_str)
                    return parsed
                else:
                    # Return as string, truncated if too long
                    return response_str[:500] if len(response_str) > 500 else response_str
            except (json.JSONDecodeError, ValueError):
                # If not valid JSON, return as string
                response_str = str(response)
                return response_str[:500] if len(response_str) > 500 else response_str
        elif hasattr(response, '__len__'):
            try:
                return f"<{type(response).__name__} with {len(response)} items>"
            except Exception:
                return f"<{type(response).__name__}>"
        else:
            return f"<{type(response).__name__}>"
    
    def process(self, result: Any, http_details: Optional[HTTPDetails] = None) -> tuple[dict[str, Any], Optional[HTTPDetails]]:
        """Process ResponseGetData result and update HTTP details.
        
        Args:
            result: The function result (should be ResponseGetData)
            http_details: Optional HTTP details to update
            
        Returns:
            Tuple of (result_context dict, updated http_details)
        """
        result_context = {}
        
        if isinstance(result, rgd.ResponseGetData) and http_details:
            # Update HTTP details with response information
            http_details.status_code = result.status
            
            # Extract response size and body
            if hasattr(result, 'response'):
                response = result.response
                http_details.response_body = self._format_response_body(response)
                
                # Calculate response size
                if isinstance(response, (str, bytes)):
                    http_details.response_size = len(response)
                elif hasattr(response, '__len__'):
                    try:
                        http_details.response_size = len(response)
                    except Exception:
                        pass
            
            # Use request metadata if available to fill in missing request details
            if hasattr(result, 'request_metadata') and result.request_metadata:
                metadata = result.request_metadata
                if not http_details.url:
                    http_details.url = metadata.url
                if not http_details.method:
                    http_details.method = metadata.method
                if not http_details.headers:
                    # Sanitize headers before setting
                    http_details.headers = self._sanitize_headers(metadata.headers)
                if not http_details.params:
                    http_details.params = metadata.params
                if not http_details.request_body:
                    http_details.request_body = metadata.body
        
        return result_context, http_details


__all__ = [
    "ResponseGetDataProcessor",
]
