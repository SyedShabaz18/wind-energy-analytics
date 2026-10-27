from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
import pytest
from app.elexon import fetch_actuals, fetch_forecasts

@pytest.mark.asyncio
async def test_query_parameter_contract():
    with patch('app.elexon.request_records', new_callable=AsyncMock, return_value=[]) as call:
        a = datetime(2026, 1, 16, tzinfo=timezone.utc)
        b = datetime(2026, 1, 17, tzinfo=timezone.utc)
        await fetch_actuals(a, b)
        assert call.call_args.args[1] == 'datasets/FUELHH'
        assert call.call_args.args[2]['settlementDateFrom'] == '2026-01-16'
        await fetch_forecasts(a, b)
        assert call.call_args.args[1] == 'datasets/WINDFOR/stream'
        assert 'publishDateTimeFrom' in call.call_args.args[2]
