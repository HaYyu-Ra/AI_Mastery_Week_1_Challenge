# Deployment Guide — Render

## Service configuration
The service is configured in the repository-root `render.yaml`.

- Service: `nova-financial-insights`
- Runtime: Python
- Build: `pip install -r requirements.txt`
- Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Health endpoint: `/_stcore/health`
- Branch: `deployment`

## Manual deployment
1. Open the Render service dashboard.
2. Confirm the repository is `HaYyu-Ra/AI_Mastery_Week_1_Challenge`.
3. Confirm branch `deployment` is selected.
4. Check the latest deploy build and runtime logs.
5. Open the public service URL after the deploy reports Live.
6. Upload the AAPL/AMZN CSV files in the dashboard sidebar.
7. Upload the actual financial-news CSV in the News Analysis tab to enable news analysis.

## Local run
```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

## Notes
The free Render service may spin down after inactivity and take time to wake up. Do not put secrets or restricted raw datasets in the public repository. The application uses uploaded CSVs and does not require API keys.
