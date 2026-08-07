# InsightFlow AI V1 – Product Requirements Document (PRD)

# 1. Project Overview

## Product Name

**InsightFlow AI**

## Version

V1.0

## Goal

Build a backend service that continuously monitors tabular datasets (CSV/XLSX), compares the latest dataset with the previous snapshot, detects meaningful changes, and generates alerts when predefined thresholds are exceeded.

V1 is **not** an AI application. It is a data monitoring engine. AI explanations, forecasting, and anomaly detection are future modules.

---

# 2. Scope

## In Scope

- Upload CSV/XLSX datasets
- Store dataset snapshots
- Compare latest snapshot with previous snapshot
- Detect structural and statistical changes
- Configurable alert thresholds
- Generate monitoring reports
- Send notifications
- REST API
- Background monitoring scheduler

## Out of Scope (V2+)

- LLM explanations
- Forecasting
- Root cause analysis
- Multi-agent orchestration
- Dashboard analytics
- Authentication
- Multi-user support
- Multiple notification providers

---

# 3. Functional Requirements

## Dataset Upload

Users should be able to upload:

- CSV
- XLSX

System should

- Validate file
- Read into Pandas DataFrame
- Store original file
- Generate snapshot
- Save metadata

---

## Snapshot Management

Every upload creates a new immutable snapshot.

Each snapshot contains

- Dataset version
- Timestamp
- Metadata
- File path
- Row count
- Column count
- Dataset hash

Snapshots are never modified.

---

## Monitoring Engine

Every monitoring cycle:

1. Load newest snapshot
2. Load previous snapshot
3. Compare datasets
4. Generate report
5. Evaluate thresholds
6. Trigger notifications if required

---

## Comparison Engine

Compare

### Dataset Level

- Row count
- Column count
- Dataset hash

### Schema Level

- Added columns
- Removed columns
- Datatype changes

### Data Quality

- Missing values
- Duplicate rows
- Null percentage

### Numeric Statistics

For every numeric column

- Mean
- Median
- Standard deviation
- Min
- Max

### Categorical Statistics

- Unique count
- Top category
- Category distribution

---

## Alert Engine

Generate alerts when thresholds exceed configured limits.

Example thresholds

- Missing values >10%
- Mean shift >15%
- Duplicate increase >5%
- Row count change >20%
- Schema change detected

---

## Notification

Initially support

- Console
- Email (SMTP)

Notification contains

- Dataset
- Time
- Summary
- Metrics exceeded

---

## Reports

Each monitoring run generates one report.

Reports remain available for history.

---

# 4. Non-Functional Requirements

- FastAPI backend
- Modular architecture
- Service-based design
- Async APIs where appropriate
- Easy to extend
- Unit-test friendly
- Configuration via environment variables
- Background scheduler independent of API layer

---

# 5. High-Level Architecture

```
Upload Dataset
      │
      ▼
Snapshot Service
      │
      ▼
Store Snapshot
      │
Scheduler
      │
      ▼
Monitoring Service
      │
      ▼
Comparison Service
      │
      ▼
Threshold Service
      │
      ▼
Notification Service
```

---

# 6. Backend Folder Structure

```
backend/

app/

├── api/
│   ├── dataset_router.py
│   ├── monitoring_router.py
│   ├── report_router.py
│   ├── snapshot_router.py
│   └── notification_router.py
│
├── services/
│   ├── dataset_service.py
│   ├── snapshot_service.py
│   ├── comparison_service.py
│   ├── monitoring_service.py
│   ├── threshold_service.py
│   ├── notification_service.py
│   └── report_service.py
│
├── repositories/
│   ├── dataset_repository.py
│   ├── snapshot_repository.py
│   └── report_repository.py
│
├── schemas/
│
├── models/
│
├── workers/
│   └── scheduler.py
│
├── utils/
│
├── core/
│
└── main.py

uploads/

snapshots/

reports/
```

---

# 7. API Routes

## Dataset Routes

### POST /datasets/upload

Upload a dataset.

Response

- dataset_id
- snapshot_id
- filename
- rows
- columns

---

### GET /datasets

List uploaded datasets.

---

### GET /datasets/{dataset_id}

Return dataset metadata.

---

## Snapshot Routes

### GET /snapshots

List snapshots.

---

### GET /snapshots/{snapshot_id}

Snapshot metadata.

---

### GET /datasets/{dataset_id}/snapshots

List snapshots for one dataset.

---

## Monitoring Routes

### POST /monitor/run

Run monitoring immediately.

---

### GET /monitor/status

Latest monitoring status.

---

### GET /monitor/history

Monitoring execution history.

---

## Report Routes

### GET /reports

List reports.

---

### GET /reports/latest

Latest monitoring report.

---

### GET /reports/{report_id}

Detailed report.

---

## Notification Routes

### GET /notifications

Notification history.

---

### POST /notifications/test

Send test notification.

---

# 8. Database Models

## Dataset

```
Dataset

id
name
filename
created_at
latest_snapshot_id
status
```

---

## Snapshot

```
Snapshot

id
dataset_id
version
file_path
dataset_hash
rows
columns
created_at
```

---

## Monitoring Report

```
MonitoringReport

id
dataset_id
snapshot_id
previous_snapshot_id
created_at
alert_generated
summary
```

---

## Alert

```
Alert

id
report_id
severity
metric
threshold
actual_value
message
created_at
```

---

# 9. Pydantic Schemas

## DatasetResponse

```
id
name
filename
rows
columns
created_at
```

---

## SnapshotResponse

```
id
dataset_id
version
rows
columns
hash
created_at
```

---

## ColumnComparison

```
column_name

dtype_old

dtype_new

missing_old

missing_new

mean_old

mean_new

std_old

std_new

status
```

---

## MonitoringReportResponse

```
report_id

dataset_id

snapshot_old

snapshot_new

rows_added

rows_removed

columns_added

columns_removed

schema_changes

duplicate_change

missing_changes

numeric_changes

alerts
```

---

## AlertResponse

```
alert_id

severity

metric

threshold

actual_value

message
```

---

# 10. Service Responsibilities

## Dataset Service

- Validate uploads
- Read DataFrame
- Create dataset
- Trigger snapshot creation

---

## Snapshot Service

- Save snapshots
- Load snapshots
- Version management
- Calculate dataset hash

---

## Comparison Service

Responsible only for comparing two DataFrames.

Returns a structured comparison object.

No alerts.

No notifications.

---

## Threshold Service

Evaluate comparison output.

Determine whether an alert should be generated.

No data processing.

---

## Monitoring Service

Coordinates the workflow.

```
Load snapshots

↓

Compare

↓

Evaluate thresholds

↓

Generate report

↓

Notify
```

---

## Notification Service

Responsible only for delivering notifications.

No comparison logic.

---

## Report Service

Stores reports.

Retrieves report history.

---

# 11. Background Scheduler

Runs every hour.

Workflow

```
Load latest dataset

↓

Find previous snapshot

↓

Run comparison

↓

Generate report

↓

Check thresholds

↓

Notify
```

Scheduler never performs business logic directly.

It only calls MonitoringService.

---

# 12. V1 Success Criteria

The system is considered complete when it can:

- Accept CSV/XLSX uploads
- Store immutable dataset snapshots
- Compare the latest snapshot with the previous snapshot
- Detect schema and statistical changes
- Generate structured monitoring reports
- Trigger alerts when thresholds are exceeded
- Execute automatically on a schedule
- Expose all functionality through REST APIs
