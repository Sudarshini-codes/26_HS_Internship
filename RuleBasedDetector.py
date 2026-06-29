import pandas as pd

# Configurable pressure thresholds (adjustable)
# Rows with pressure < PRESSURE_DROPOUT_CUTOFF are treated as pressure dropouts.
# For point spikes we require pressure >= POINT_SPIKE_PRESSURE_MIN and a channel
# value outside its normal range.
PRESSURE_DROPOUT_CUTOFF = 95.8
POINT_SPIKE_PRESSURE_MIN = 101.8


def detect_anomaly(row: dict,
                   pressure_dropout_cutoff: float = PRESSURE_DROPOUT_CUTOFF,
                   point_spike_pressure_min: float = POINT_SPIKE_PRESSURE_MIN) -> dict:
    """Detect a single anomaly in a row dictionary.

    Returns a dictionary with keys:
    - is_anomaly: bool
    - fault_type: 'point_spike' | 'pressure_dropout' | 'None'
    - reason: str
    """
    pressure = row.get('pressure_kpa')

    # Pressure-based dropout takes precedence
    if pressure is not None and pressure < pressure_dropout_cutoff:
        return {
            'is_anomaly': True,
            'fault_type': 'pressure_dropout',
            'reason': f'pressure_kpa is below {pressure_dropout_cutoff}',
        }

    # Only classify point spikes when the row is NOT a pressure dropout
    # (i.e. pressure is None or pressure >= pressure_dropout_cutoff).
    # The POINT_SPIKE_PRESSURE_MIN is informational but not a hard gate.
    if pressure is None or pressure >= pressure_dropout_cutoff:
        if row.get('temperature_c') is not None and (row['temperature_c'] > 32.0 or row['temperature_c'] < 7.0):
            if row['temperature_c'] > 32.0:
                return {
                    'is_anomaly': True,
                    'fault_type': 'point_spike',
                    'reason': 'temperature_c is above 32.0',
                }
            if row['temperature_c'] < 7.0:
                return {
                    'is_anomaly': True,
                    'fault_type': 'point_spike',
                    'reason': 'temperature_c is below 7.0',
                }
        if row.get('vibration_mm_s') is not None and (row['vibration_mm_s'] > 5.5 or row['vibration_mm_s'] < 1.5) :
            if row['vibration_mm_s'] > 5.5:
                return {
                    'is_anomaly': True,
                    'fault_type': 'point_spike',
                    'reason': 'vibration_mm_s is above 5.5',
                }
            if row['vibration_mm_s'] < 1.5:
                return {
                    'is_anomaly': True,
                    'fault_type': 'point_spike',
                    'reason': 'vibration_mm_s is below 1.5',
                }
        if row.get('current_a') is not None and (row['current_a'] > 8.8 or row['current_a'] < 4.2):
            if row['current_a'] > 8.8:
                return {
                    'is_anomaly': True,
                    'fault_type': 'point_spike',
                    'reason': 'current_a is above 8.8',
                }
            if row['current_a'] < 4.2:
                return {
                    'is_anomaly': True,
                    'fault_type': 'point_spike',
                    'reason': 'current_a is below 4.2',
                }

    return {
        'is_anomaly': False,
        'fault_type': 'None',
        'reason': 'None',
    }


if __name__ == '__main__':
    df = pd.read_csv('sensor_data_2yr.csv', parse_dates=['timestamp'])

    detected_counts = {
        'point_spike': 0,
        'pressure_dropout': 0,
        'no_fault': 0,
    }

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        result = detect_anomaly(row_dict)
        if row_dict.get('anomaly') == 1 and result['is_anomaly']:
            detected_counts[result['fault_type']] += 1
        elif row_dict.get('anomaly') == 1 and not result['is_anomaly']:
            detected_counts['no_fault'] += 1

    sample_anomalous = {
        'timestamp': '2025-07-30 09:20:00',
        'temperature_c': 38.5,
        'vibration_mm_s': 2.41,
        'pressure_kpa': 101.28,
        'current_a': 5.92,
    }
    print('\nSample anomalous input result:')
    print(detect_anomaly(sample_anomalous))

    sample_normal = {
        'timestamp': '2025-07-30 09:25:00',
        'temperature_c': 25.0,
        'vibration_mm_s': 3.0,
        'pressure_kpa': 101.0,
        'current_a': 6.0,
    }
    print('\nSample normal input result:')
    print(detect_anomaly(sample_normal))


    
