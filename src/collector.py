import os
import sys
import time
import json

class MetricCollector:
    def __init__(self, log_path='metrics.json'):
        self.log_path = log_path

    def get_cpu_usage(self):
        try:
            if os.path.exists('/proc/stat'):
                with open('/proc/stat', 'r') as f:
                    line = f.readline()
                parts = line.split()
                if len(parts) > 4:
                    idle = float(parts[4])
                    total = sum(float(x) for x in parts[1:5])
                    return {'idle': idle, 'total': total}
        except Exception:
            pass
        return None

    def get_memory_info(self):
        try:
            if os.path.exists('/proc/meminfo'):
                meminfo = {}
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        parts = line.split(':')
                        if len(parts) == 2:
                            meminfo[parts[0].strip()] = parts[1].strip()
                return {
                    'total': meminfo.get('MemTotal', 'N/A'),
                    'free': meminfo.get('MemFree', 'N/A'),
                    'available': meminfo.get('MemAvailable', 'N/A')
                }
        except Exception:
            pass
        return None

    def collect(self):
        metrics = {
            'timestamp': time.time(),
            'cpu': self.get_cpu_usage(),
            'memory': self.get_memory_info()
        }
        return metrics

    def run(self, interval=60):
        while True:
            data = self.collect()
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(data) + '\n')
            time.sleep(interval)

if __name__ == '__main__':
    collector = MetricCollector()
    print('[*] Starting performance metric collector...')
    try:
        collector.run(interval=10)
    except KeyboardInterrupt:
        print('[*] Exiting.')