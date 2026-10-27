from datetime import date
from app.analytics import analyze, decision_window

def test_dst_spring_forward_day_has_46_intervals():
    result = analyze([], [], date(2026, 3, 28))
    assert result['metrics']['totalIntervals'] == 46

def test_dst_fall_back_day_has_50_intervals():
    result = analyze([], [], date(2026, 10, 24))
    assert result['metrics']['totalIntervals'] == 50

def test_future_forecast_rejected_and_invalid_values_ignored():
    actual = [{'startTime': '2026-01-16T00:00:00Z', 'fuelType': 'WIND', 'generation': 'NaN'}]
    forecast = [{'startTime': '2026-01-16T00:00:00Z', 'publishTime': '2026-01-15T12:00:00Z', 'generation': 500}]
    result = analyze(actual, forecast, date(2026, 1, 15))
    assert result['metrics']['matchedIntervals'] == 0
    assert result['intervals'][0]['actualMW'] is None
    assert result['intervals'][0]['forecastMW'] is None

def test_zero_actual_is_valid_observation():
    actual = [{'startTime': '2026-01-16T00:00:00Z', 'fuelType': 'WIND', 'generation': 0}]
    forecast = [{'startTime': '2026-01-16T00:00:00Z', 'publishTime': '2026-01-15T10:00:00Z', 'generation': 10}]
    result = analyze(actual, forecast, date(2026, 1, 15))
    assert result['metrics']['matchedIntervals'] == 1
    assert result['metrics']['wapePercent'] is None
