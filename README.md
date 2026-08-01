**Folder Structure**

docs/
  intern_project_2026.pdf
  
data/
  sensor_data_2yr.csv

backend/
  main.py
  RuleBasedDetector.py

frontend/
  index.html
  ui.html
  compact.html
  live_chart.html
  simulator.html

**Main Files**

data/sensor_data_2yr.csv: full labeled training/evaluation dataset.
backend/main.py: FastAPI app serving frontend pages and exposing /predict.
frontend/index.html: simple form UI for calling /predict.

**Useful Commands**
Install API dependencies:

python -m pip install -r requirements.txt

Run the app:

uvicorn main:app --host 0.0.0.0 --reload
The FastAPI app serves both the frontend and the /predict API, so a separate frontend HTTP server is not needed.

Open the API docs:

http://127.0.0.1:8000/docs
Open the frontend:

http://127.0.0.1:8000/
Open the other frontend pages:

http://127.0.0.1:8000/compact
http://127.0.0.1:8000/live-chart
http://127.0.0.1:8000/simulator
