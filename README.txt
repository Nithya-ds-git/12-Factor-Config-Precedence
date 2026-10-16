HOW TO RUN (needs Python 3.9+ installed)

Windows: double-click run.bat
Mac/Linux: open Terminal in this folder and run:  ./run.sh

Then open in your browser:
  http://localhost:8080/effective-config
Expected output:
  {"port":8883,"workers":7,"debug":true,"log_level":"info","api_key":"****"}

Try overrides:
  http://localhost:8080/effective-config?set=port=9000&set=debug=off

TO DEPLOY (Render): upload these files to GitHub, then
  Build Command: pip install -r requirements.txt
  Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
  Environment variable: APP_WORKERS = 7
