# Smart Traffic Violation Detection System using YOLOv2

A production-style portfolio project for real-time traffic monitoring, evidence capture, violation analytics, and nightly retraining orchestration.

## Highlights
- YOLOv2-ready detection pipeline with OpenCV DNN fallback and a mock mode for local demos
- FastAPI microservices for camera stream ingestion, frame analysis, violation reporting, and health checks
- PostgreSQL analytics with SQLAlchemy models and REST endpoints
- S3-compatible evidence storage abstraction
- Dockerized services with local `docker-compose` support
- Airflow DAG for nightly retraining, metrics export, and dashboard refresh
- AWS EC2 deployment notes and GitHub Actions CI

> Note: pretrained YOLOv2 weights are **not** bundled in this repository. The code is ready for them, but you must download the weights/config yourself and place them in `weights/`.

## Architecture

```text
RTSP / Video Feed
      |
      v
FastAPI Inference Service ----> YOLOv2 Detector ----> Violation Engine
      |                               |                    |
      |                               |                    v
      |                               |              Evidence Snapshot
      |                               v                    |
      +------------------------> PostgreSQL <--------------+
                                      |
                                      v
                                 Reporting APIs
                                      |
                                      v
                                Dashboard / BI Layer

Airflow nightly:
- gather labeled events
- retrain/export detector
- refresh daily summary table
```

## Repo Structure

```text
app/
  api/            # REST routes
  core/           # settings, logging
  db/             # session + base
  models/         # SQLAlchemy models
  schemas/        # Pydantic schemas
  services/       # detector, video, storage, violation logic
  utils/          # helpers
ml/               # retraining pipeline
dags/             # Airflow workflows
infra/            # nginx + deployment notes
tests/            # pytest suite
```

## Quick Start

### 1) Create environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2) Start locally without Docker
```bash
uvicorn app.main:app --reload
```

Open docs at `http://127.0.0.1:8000/docs`

### 3) Start with Docker Compose
```bash
docker compose up --build
```

## Demo Endpoints
- `GET /health`
- `POST /streams/register`
- `POST /streams/{camera_id}/analyze`
- `GET /violations`
- `GET /violations/{violation_id}`
- `GET /analytics/daily-summary`

## Example Request
```bash
curl -X POST http://127.0.0.1:8000/streams/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main & 5th",
    "location": "Arlington, TX",
    "source_url": "sample.mp4",
    "stop_line_y": 340,
    "red_light_roi": [20,20,60,120]
  }'
```

Then run one pass of analysis:
```bash
curl -X POST http://127.0.0.1:8000/streams/1/analyze
```

## YOLOv2 Weights Setup
Place these files in a `weights/` folder:
- `yolov2.cfg`
- `yolov2.weights`
- `coco.names` or custom classes file

Set in `.env`:
```env
YOLO_CONFIG_PATH=weights/yolov2.cfg
YOLO_WEIGHTS_PATH=weights/yolov2.weights
YOLO_CLASSES_PATH=weights/coco.names
DETECTION_MODE=yolo
```

For a no-weights local demo use:
```env
DETECTION_MODE=mock
```

## AWS EC2 Deployment
1. Launch Ubuntu EC2
2. Install Docker + Docker Compose plugin
3. Configure IAM role for S3 access or use access keys in secrets manager
4. Clone repo
5. Provide `.env`
6. Run:
```bash
docker compose -f docker-compose.yml up -d --build
```
7. Put Nginx in front using `infra/nginx.conf`

## Airflow
The DAG `dags/nightly_retrain_and_refresh.py` performs:
- fetch event metadata from PostgreSQL
- simulate labeling dataset export
- retrain a lightweight baseline model placeholder
- refresh the materialized daily summary

## Tests
```bash
pytest -q
```

## Resume-ready talking points
- Built a real-time smart traffic monitoring platform using YOLOv2-ready detection with evidence capture and violation analytics.
- Designed FastAPI microservices to stream RTSP/video feeds, score frames, and generate automated reports.
- Deployed Dockerized ML pipelines with PostgreSQL and S3-compatible evidence storage.
- Implemented Airflow DAGs for nightly retraining and summary refresh.

## Future Improvements
- Deep SORT-based multi-object tracking
- Real OCR for license plates
- Kafka event bus for horizontal scaling
- Prometheus + Grafana monitoring
- Human-in-the-loop review UI
