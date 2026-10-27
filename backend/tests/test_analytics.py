from datetime import date
from app.analytics import analyze, decision_window

def test_latest_eligible_forecast_and_no_future_leakage():
    actual = [{'startTime': '2026-01-16T00:00:00Z', 'fuelType': 'WIND', 'generation': 100}]
    forecasts = [
        {'startTime': '2026-01-16T00:00:00Z', 'publishTime': '2026-01-15T08:00:00Z', 'generation': 90},
        {'startTime': '2026-01-16T00:00:00Z', 'publishTime': '2026-01-15T10:30:00Z', 'generation': 95},
        {'startTime': '2026-01-16T00:00:00Z', 'publishTime': '2026-01-15T12:00:00Z', 'generation': 110},
    ]
    result = analyze(actual, forecasts, date(2026, 1, 15))
    assert result['intervals'][0]['forecastMW'] == 95
    assert result['metrics']['maeMW'] == 5
    assert result['metrics']['biasMW'] == -5
    assert result['metrics']['matchedIntervals'] == 1

def test_missing_is_not_zero():
    result = analyze([], [], date(2026, 1, 15))
    assert result['metrics']['maeMW'] is None
    assert result['metrics']['coveragePercent'] == 0
    assert len(result['intervals']) == 48

def test_january_31_decision_delivers_february_1():
    _, start, _ = decision_window(date(2026, 1, 31))
    assert start.date().isoformat() == '2026-02-01'

def test_wind_filter_and_missing_forecast():
    actual = [{'startTime': '2026-01-16T00:00:00Z', 'fuelType': 'SOLAR', 'generation': 500},
              {'startTime': '2026-01-16T00:00:00Z', 'fuelType': 'WIND', 'generation': 100}]
    result = analyze(actual, [], date(2026, 1, 15))
    assert result['intervals'][0]['actualMW'] == 100
    assert result['intervals'][0]['forecastMW'] is None
    assert result['metrics']['matchedIntervals'] == 0
