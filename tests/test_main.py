import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# src klasörünü path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import trigger_n8n_webhook

def test_trigger_n8n_webhook_success():
    """Tetikleyici başarılı olduğunda True dönmeli."""
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = MagicMock()
        
        # Test verisi
        test_data = {"test": "data"}
        
        # Env mock
        with patch.dict(os.environ, {"N8N_WEBHOOK_URL": "http://mock-n8n/webhook"}):
            result = trigger_n8n_webhook(test_data)
            assert result is True
            mock_post.assert_called_once()

def test_trigger_n8n_webhook_failure():
    """Tetikleyici hata aldığında False dönmeli."""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Connection Error")
        
        # Test verisi
        test_data = {"test": "data"}
        
        # Env mock
        with patch.dict(os.environ, {"N8N_WEBHOOK_URL": "http://mock-n8n/webhook"}):
            result = trigger_n8n_webhook(test_data)
            assert result is False
