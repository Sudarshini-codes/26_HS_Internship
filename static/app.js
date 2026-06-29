const form = document.getElementById('anomaly-form');
const resultSection = document.getElementById('result');
const errorSection = document.getElementById('error');
const anomalyField = document.getElementById('result-anomaly');
const typeField = document.getElementById('result-type');
const reasonField = document.getElementById('result-reason');

form.addEventListener('submit', async event => {
  event.preventDefault();
  errorSection.classList.add('hidden');
  resultSection.classList.add('hidden');

  const timestampInput = document.getElementById('timestamp').value;
  const payload = {
    timestamp: timestampInput,
    temperature_c: parseFloat(document.getElementById('temperature').value),
    vibration_mm_s: parseFloat(document.getElementById('vibration').value),
    pressure_kpa: parseFloat(document.getElementById('pressure').value),
    current_a: parseFloat(document.getElementById('current').value),
  };

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'API request failed');
    }

    const data = await response.json();
    anomalyField.textContent = data.is_anomaly ? 'Yes' : 'No';
    typeField.textContent = data.fault_type || 'None';
    reasonField.textContent = data.reason || 'None';
    resultSection.classList.remove('hidden');
  } catch (err) {
    errorSection.textContent = `Error: ${err.message}`;
    errorSection.classList.remove('hidden');
  }
});
