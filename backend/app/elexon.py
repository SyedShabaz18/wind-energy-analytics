"""Elexon BMRS raw datasets: publication-window WINDFOR, settlement-window FUELHH."""
from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
import asyncio
import httpx
import logging

logger = logging.getLogger(__name__)

BASE = 'https://data.elexon.co.uk/bmrs/api/v1'

class ElexonError(Exception):
    pass

def unwrap(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ('data', 'results', 'items'):
            if isinstance(payload.get(key), list):
                return payload[key]
    raise ElexonError('Unexpected Elexon response; expected JSON records.')

def iso(t):
    return t.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')

async def request_records(client, endpoint, params):
    last = None
    for attempt in range(3):
        try:
            r = await client.get(f'{BASE}/{endpoint}', params=params)
            r.raise_for_status()
            return unwrap(r.json())
        except httpx.HTTPStatusError as exc:
            last = exc
            if exc.response.status_code not in (429, 500, 502, 503, 504):
                break
        except (httpx.RequestError, ValueError, ElexonError) as exc:
            last = exc
        if attempt < 2:
            await asyncio.sleep(0.7 * (2 ** attempt))
    logger.warning('Elexon request failed for %s: %s', endpoint, last)
    raise ElexonError('Upstream data service request failed; see backend logs for details.')

async def fetch_actuals(delivery_start: datetime, delivery_end: datetime):
    # FUELHH settlement date filter; end date is inclusive for this dataset.
    start_day = delivery_start.date()
    end_day = (delivery_end - timedelta(microseconds=1)).date()
    async with httpx.AsyncClient(timeout=45.0) as client:
        return await request_records(client, 'datasets/FUELHH', {
            'settlementDateFrom': start_day.isoformat(),
            'settlementDateTo': end_day.isoformat(),
            'format': 'json',
        })

async def fetch_forecasts(start: datetime, cutoff: datetime):
    # WINDFOR raw stream filters by PUBLISH time, not delivery startTime.
    # Fetch every revision up to the cutoff, then select per target interval.
    rows = []
    async with httpx.AsyncClient(timeout=45.0) as client:
        cursor = start
        while cursor < cutoff:
            nxt = min(cursor + timedelta(hours=24), cutoff)
            rows.extend(await request_records(client, 'datasets/WINDFOR/stream', {
                'publishDateTimeFrom': iso(cursor),
                'publishDateTimeTo': iso(nxt),
            }))
            cursor = nxt
    return rows
