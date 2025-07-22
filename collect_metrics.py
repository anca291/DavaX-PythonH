from service.service_metrics import store_prometheus_metrics
from config.database import db
from pprint import pprint

metrics_collection = db["metrics"]

def show_latest_metrics(limit=10):
    print(f"\nShowing latest {limit} stored metrics:")
    results = metrics_collection.find().sort("fetched_at", -1).limit(limit)
    for doc in results:
        pprint({
            "query": doc.get("query"),
            "metric": doc.get("metric"),
            "value": doc.get("value"),
            "fetched_at": doc.get("fetched_at")
        })

if __name__ == "__main__":
    store_prometheus_metrics()
    show_latest_metrics()
