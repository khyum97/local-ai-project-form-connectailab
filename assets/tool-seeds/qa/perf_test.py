#!/usr/bin/env python3
# version: perf_test_v1
"""Create a k6 or Artillery performance test starter script.

config:
  PROJECT_PATH  project root
  TOOL          k6|artillery
  TARGET_URL    endpoint to test
  VUS           virtual users
  DURATION      run duration, e.g. 30s
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "perf_test.json")


def load_config():
    if not os.path.exists(CONFIG):
        return {}
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    cfg = load_config()
    project = os.path.expanduser((cfg.get("PROJECT_PATH") or os.getcwd()).strip())
    tool = (cfg.get("TOOL") or "k6").strip().lower()
    target = (cfg.get("TARGET_URL") or "http://localhost:3000/health").strip()
    vus = int(cfg.get("VUS") or 10)
    duration = (cfg.get("DURATION") or "30s").strip()
    out_dir = os.path.join(project, "tests", "perf")
    os.makedirs(out_dir, exist_ok=True)

    if tool == "artillery":
        out_path = os.path.join(out_dir, "load-test.yml")
        body = f"""config:
  target: "{target}"
  phases:
    - duration: {duration.rstrip("s")}
      arrivalRate: {max(1, vus // 2)}
scenarios:
  - name: health check
    flow:
      - get:
          url: "/"
"""
    else:
        out_path = os.path.join(out_dir, "load-test.js")
        body = f"""import http from 'k6/http';
import {{ check, sleep }} from 'k6';

export const options = {{
  vus: {vus},
  duration: '{duration}',
  thresholds: {{
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  }},
}};

export default function () {{
  const res = http.get('{target}');
  check(res, {{
    'status is 2xx': (r) => r.status >= 200 && r.status < 300,
  }});
  sleep(1);
}}
"""

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
