import os
import sys
import json
import time

class MetricCollector:
    def __init__(self, interval=60):
        self.interval = interval

    def get_system_metrics(self):
        metrics = {
            "timestamp": time.time(),
            "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None,
            "platform": sys.platform
        }
        return metrics

    def run(self):
        try:
            while True:
                data = self.get_system_metrics()
                print(json.dumps(data))
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Collector stopped.")

if __name__ == '__main__':
    collector = MetricCollector()
    collector.run()