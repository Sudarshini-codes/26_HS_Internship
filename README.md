uvicorn main:app --host 0.0.0.0 --reload

**Folder Structure**

docs/
  intern_project_2026.pdf
  intern_workflow_brief.md
  project_review_and_api_contract.md

data/
  sensor_data_2yr.csv

backend/
  main.py
  RuleBasedDetector.py
  visualize_sensor_data.py

frontend/
  index.html
  ui.html
  compact.html
  live_chart.html
  simulator.html

**Main Files**

data/sensor_data_2yr.csv: full labeled training/evaluation dataset.
data/ui_demo_sensor_input_500.csv: small unlabeled CSV for the UI demo.
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
