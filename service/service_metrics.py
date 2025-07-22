import requests
from datetime import datetime
from config.database import db

metrics_collection = db["metrics"]

PROMETHEUS_URL = "http://localhost:9091/api/v1/query"

QUERIES = {
    "total_requests": 'sum by (path) (http_requests_total)',
    "avg_duration": 'rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])',
    "by_status": 'sum by (status) (http_requests_total)',
    "post_calls": 'sum(http_requests_total{method="POST"})'
}


def query_prometheus(promql: str):
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": promql})
        response.raise_for_status()
        return response.json().get("data", {}).get("result", [])
    except Exception as e:
        print(f"[ERROR] Prometheus query failed: {promql}\n{e}")
        return []


def store_prometheus_metrics():
    timestamp = datetime.utcnow()

    for name, promql in QUERIES.items():
        results = query_prometheus(promql)

        for item in results:
            entry = {
                "query": name,
                "metric": item.get("metric", {}),
                "value": item.get("value", []),
                "fetched_at": timestamp
            }
            metrics_collection.insert_one(entry)

        print(f"[INFO] Stored {len(results)} metrics for '{name}'")
