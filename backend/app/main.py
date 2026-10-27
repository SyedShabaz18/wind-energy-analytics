"""WindCast API. January 2026 decision-date scope per assignment."""
from __future__ import annotations
import os
from datetime import date, datetime, timedelta, timezone
import asyncio
import time
from collections import OrderedDict
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .analytics import analyze, decision_window
from .elexon import fetch_actuals, fetch_forecasts, ElexonError

app = FastAPI(title='WindCast Analytics API', version='1.1.0')
_CACHE = OrderedDict()
_CACHE_TTL_SECONDS = 3600
_CACHE_MAX_ITEMS = 64
_LOCK = asyncio.Lock()
origins = [s.strip() for s in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',') if s.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=['GET'], allow_headers=['*'])

@app.get('/api/health')
def health():
    return {'status': 'ok', 'service': 'WindCast Analytics API'}

@app.get('/api/analysis')
async def get_analysis(decision_date: date = Query(default=date(2026, 1, 15)), cutoff_hour: int = Query(default=11, ge=0, le=23)):
    if not (date(2022, 1, 1) <= decision_date <= date(2026, 12, 31)):
        raise HTTPException(400, 'Choose a date between January 2022 and December 2026. The assignment scope remains January 2026.')
    key = (decision_date.isoformat(), cutoff_hour)
    async with _LOCK:
        cached = _CACHE.get(key)
        if cached and time.monotonic() - cached[0] < _CACHE_TTL_SECONDS:
            return cached[1]
    cutoff, delivery_start, delivery_end = decision_window(decision_date, cutoff_hour)
    # Forecasts may have been published several days before the cutoff.
    # A 7-day lookback is a documented analytical assumption, not an Elexon guarantee.
    forecast_from = cutoff - timedelta(days=7)
    try:
        actual_rows, forecast_rows = await asyncio.gather(
            fetch_actuals(delivery_start, delivery_end),
            fetch_forecasts(forecast_from, cutoff),
        )
    except ElexonError as exc:
        raise HTTPException(status_code=502, detail='Elexon data could not be loaded. Please try again later.') from exc
    result = analyze(actual_rows, forecast_rows, decision_date, cutoff_hour)
    result['source'] = 'Elexon BMRS FUELHH + WINDFOR'
    result['mode'] = 'live'
    result['forecastLookbackDays'] = 7
    result['recordCounts'] = {'actualRaw': len(actual_rows), 'forecastRaw': len(forecast_rows)}
    result['dataWarning'] = ('No matched forecast/actual observations. Check Elexon availability and raw record counts.' if result['metrics']['matchedIntervals'] == 0 else None)
    async with _LOCK:
        _CACHE[key] = (time.monotonic(), result)
        _CACHE.move_to_end(key)
        while len(_CACHE) > _CACHE_MAX_ITEMS:
            _CACHE.popitem(last=False)
    return result
