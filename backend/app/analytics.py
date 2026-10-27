"""Pure analytics functions: deterministic and independently testable."""
from __future__ import annotations
from datetime import datetime, date, time, timedelta, timezone
from zoneinfo import ZoneInfo
from math import sqrt, isfinite

LONDON = ZoneInfo('Europe/London')


def parse_time(value: str) -> datetime:
    if not value:
        raise ValueError('Missing timestamp')
    parsed = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        # Elexon timestamps are normally UTC; treat naive API timestamps as UTC.
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def decision_window(day: date, hour: int = 11):
    """Illustrative business assumption: 11:00 UK local time on decision day.

    Delivery is the following UK calendar day. UTC bounds account for DST.
    """
    cutoff = datetime.combine(day, time(hour), LONDON).astimezone(timezone.utc)
    delivery_day = day + timedelta(days=1)
    start = datetime.combine(delivery_day, time.min, LONDON).astimezone(timezone.utc)
    end = datetime.combine(delivery_day + timedelta(days=1), time.min, LONDON).astimezone(timezone.utc)
    return cutoff, start, end


def analyze(actual_rows: list[dict], forecast_rows: list[dict], day: date, hour: int = 11):
    cutoff, start, end = decision_window(day, hour)
    actual = {}
    for r in actual_rows:
        if str(r.get('fuelType', '')).upper() != 'WIND':
            continue
        try:
            t = parse_time(r['startTime'])
            value = float(r['generation'])
            if start <= t < end and isfinite(value) and value >= 0:
                actual[t] = value
        except (ValueError, TypeError, KeyError):
            continue

    latest = {}
    for r in forecast_rows:
        try:
            t = parse_time(r['startTime'])
            published = parse_time(r['publishTime'])
            value = float(r['generation'])
        except (ValueError, TypeError, KeyError):
            continue
        if start <= t < end and published <= cutoff and isfinite(value) and value >= 0:
            if t not in latest or published > latest[t][0]:
                latest[t] = (published, value)

    intervals = []
    for i in range(int((end - start).total_seconds() // 1800)):
        t = start + timedelta(minutes=30*i)
        forecast = latest.get(t)
        actual_value = actual.get(t)
        error = (forecast[1] - actual_value) if forecast and actual_value is not None else None
        intervals.append({
            'startTime': t.isoformat().replace('+00:00', 'Z'),
            'localTime': t.astimezone(LONDON).strftime('%d %b %H:%M %Z'),
            'forecastMW': round(forecast[1], 2) if forecast else None,
            'actualMW': round(actual_value, 2) if actual_value is not None else None,
            'errorMW': round(error, 2) if error is not None else None,
            'publishedAt': forecast[0].isoformat().replace('+00:00', 'Z') if forecast else None,
        })

    errors = [r['errorMW'] for r in intervals if r['errorMW'] is not None]
    n = len(errors)
    mae = sum(abs(x) for x in errors) / n if n else None
    rmse = sqrt(sum(x*x for x in errors) / n) if n else None
    bias = sum(errors) / n if n else None
    actual_total = sum(abs(r['actualMW']) for r in intervals if r['errorMW'] is not None)
    wape = sum(abs(x) for x in errors) / actual_total * 100 if actual_total else None
    return {
        'decisionDate': day.isoformat(),
        'decisionCutoff': cutoff.isoformat().replace('+00:00', 'Z'),
        'deliveryDate': (day + timedelta(days=1)).isoformat(),
        'timezone': 'Europe/London',
        'assumption': f'Illustrative decision cutoff: {hour:02d}:00 UK local time; latest forecast published at or before cutoff.',
        'metrics': {
            'maeMW': round(mae, 2) if mae is not None else None,
            'rmseMW': round(rmse, 2) if rmse is not None else None,
            'biasMW': round(bias, 2) if bias is not None else None,
            'wapePercent': round(wape, 2) if wape is not None else None,
            'matchedIntervals': n,
            'totalIntervals': len(intervals),
            'coveragePercent': round(100*n/len(intervals), 1) if intervals else 0,
        },
        'intervals': intervals,
    }
