## How to use
1. Install the script by executing `bash install.sh`.
2. Change `/etc/prometheus/prometheus.yml` like the following:

```yaml
scrape_configs:
  - job_name: 'ping_exporter'
    static_configs:
      - targets: ['localhost:8406']
```
