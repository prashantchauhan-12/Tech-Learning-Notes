# Observability Zero to Hero: Detailed Revision Notes (Day 1 to Day 7)

> Based on the video series by Abhishek Veeramalla, with extra explanation, cleaned-up commands and current-version caveats added.
> All practicals run on Kubernetes (EKS in the videos; Minikube/Kind also work).
> Commands marked **(repo)** follow the `observability-zero-to-hero` GitHub repo (day-wise folders). Always check the repo README for the latest flags and values files.

---

## Table of Contents

1. [Course Roadmap](#0-course-roadmap)
2. [Day 1: Observability Fundamentals](#day-1-observability-fundamentals)
3. [Day 2: Metrics, Monitoring, Prometheus and Grafana Setup](#day-2-metrics-monitoring-prometheus-and-grafana-setup)
4. [Day 3: Prometheus in Practice and PromQL](#day-3-prometheus-in-practice-promql-and-grafana-dashboards)
5. [Day 4: Custom Metrics, ServiceMonitor, Alertmanager](#day-4-instrumentation-of-custom-metrics-and-alertmanager)
6. [Day 5: Logging with the EFK Stack](#day-5-logging-with-the-efk-stack)
7. [Day 6: Distributed Tracing with Jaeger and OpenTelemetry](#day-6-distributed-tracing-with-jaeger)
8. [Day 7: End-to-End Project, OpenTelemetry Demo App](#day-7-end-to-end-project-opentelemetry-demo-application)
9. [Master Architecture Cheat Sheet](#master-architecture-cheat-sheet)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Interview Questions and Answers](#interview-questions-and-model-answers)
12. [Cleanup Commands](#cleanup-commands)
13. [Important Notes on Versions and Deprecations](#important-notes-on-versions-and-deprecations-read-this)

---

## 0. Course Roadmap

| Day | Topic | Tools |
|---|---|---|
| 1 | Fundamentals: what/why of observability, 3 pillars, monitoring vs observability | Theory |
| 2 | Metrics and monitoring, Prometheus architecture, install on EKS | Prometheus, Grafana, Alertmanager |
| 3 | Prometheus in practice, PromQL, Grafana dashboards | node-exporter, kube-state-metrics |
| 4 | Instrumentation of custom metrics, ServiceMonitor, alerting by email | `prom-client`, Alertmanager |
| 5 | Logging | EFK (Elasticsearch, Fluent Bit, Kibana) |
| 6 | Distributed tracing | Jaeger, OpenTelemetry |
| 7 | Full project with the OpenTelemetry demo app | OTel Demo, Jaeger, Grafana |

The series also plans to cover **eBPF** (how it changes observability) as a closing topic.
**Prerequisite:** basic Kubernetes knowledge.

---

# Day 1: Observability Fundamentals

## 1.1 What is observability?

**Textbook definition:** if you have observability, you can understand the **internal state of a system** from the data it emits.

"System" = **application + infrastructure + networking** (for example an app on a Kubernetes cluster on AWS inside a VPC).

### The three questions: What / Why / How

| Question | Example | Answered by |
|---|---|---|
| **WHAT** is the state of the system? | Disk utilization of a node over 24 h; CPU/memory; out of 100 API calls, how many succeeded or failed | **Metrics** |
| **WHY** is the system in that state? | Why did 5 of 1000 HTTP requests fail? Why is there a memory leak? | **Logs** |
| **HOW** do I fix it? | Which hop failed (LB, frontend, backend, DB)? Which part of the code uses the memory? | **Traces** |

## 1.2 Three Pillars of Observability

```
            OBSERVABILITY
   ┌────────────┬────────────┬────────────┐
   │  METRICS   │    LOGS    │   TRACES   │
   │   WHAT     │    WHY     │    HOW     │
   └────────────┴────────────┴────────────┘
```

**Worked example, a failing HTTP request:**

1. **Metrics** show that 10 requests failed in the last 30 min and 100 in 24 h. This is historical data, and it gives you a timestamp (for example 10:00).
2. **Logs** for 10:00 show who sent the request, which module it hit and the exact error.
3. **Traces** show the full path: `client → load balancer → frontend → backend → database`, with the time at each hop. Was it 5 ms as expected? Did it reach the right backend? Where did it fail?

## 1.3 Metrics, Logs, Traces in detail

- **Metrics**: historical (time-stamped) data of events, for example CPU, memory, disk, HTTP request counts. Without history you cannot explain why the app was down at 10 am ten days ago.
- **Logs**: messages written by developers (info, debug, warn, error, trace levels). Good logging means you understand the app better.
- **Traces**: end-to-end journey of one request across services, giving extensive data to debug, troubleshoot and fix.

## 1.4 Monitoring vs Observability

| | Monitoring | Observability |
|---|---|---|
| Pillars covered | **Only metrics** (plus alerts and dashboards) | Metrics + Logs + Traces |
| Scope | Subset | Superset |
| Components | Metrics + **Alerts** + **Dashboards** | Everything above |
| Tools | Prometheus + Alertmanager + Grafana | + EFK + Jaeger |

> **Monitoring is a subset of observability.** Interview answer: "Monitoring = metrics + alerting + dashboards. Observability = metrics + logs + traces, giving complete feedback about the internal state."

## 1.5 Why do companies need observability? (SLA / SLO story)

Scenario: a startup has a **Resume Builder** app on Kubernetes (EKS, VPC). A customer asks why they should pick it over competitors. The company signs an **SLA (Service Level Agreement)** containing **SLOs (Service Level Objectives)**, which are the promises:

- Availability of **99.9%** (only 0.1% downtime per year).
- Out of 10,000 requests, at least **9,995 respond within 30 ms with HTTP 200**.

This leaves an **error budget** of 5 requests. If 1, 2 or 3 requests fail you are still inside the budget, but at 5 you breach the SLO. You need a **continuous feedback system** to react at request 1-3, not at request 6. That feedback system is **observability**.

- Companies with strong **SRE** principles must implement observability first.
- It is also needed for Instagram, Facebook and banking apps. For example, a banking request taking 5 s → 10 s → 20 s must alert developers early.

## 1.6 Whose responsibility is observability?

**Collective effort** between developers and DevOps/SRE.

| Developers | DevOps / SRE |
|---|---|
| **Instrument** metrics, logs, traces in code | **Deploy/configure** Prometheus, Grafana, EFK/ELK, Jaeger |
| Write info/debug/error logs | Set up K8s, exporters, Helm charts, dashboards, alerts |
| Use OpenTelemetry or `prom-client` | Give end users (management, QA, devs) URLs to dashboards |

If either half is missing, observability does not work.

---

# Day 2: Metrics, Monitoring, Prometheus and Grafana Setup

## 2.1 What are metrics? (Hospital analogy)

A patient is admitted and a nurse records heartbeat and blood pressure every 15 min (10:00 → 76, 10:15 → 81 …). This periodic data is used by the doctor to judge health.

- **Metrics = historical/periodic data of events used to understand the health of a system.**
- Problem: raw metrics (notepad or Excel) are hard to read, and you can miss spikes.

## 2.2 Monitoring = Metrics + Dashboards + Alerts

A monitoring system:
1. **Scrapes (pulls)** metrics (or receives pushed metrics),
2. **Visualizes** them as graphs and dashboards (like stock price charts over 10 days, 1 month, 1 year),
3. **Fires alerts** (for example heartbeat > 90 → WhatsApp to the nurse; > 110 → message to the doctor).

> **Scraping = pulling** metrics from a target. Remember this word.

## 2.3 Metrics in the IT world

| Layer | Example metrics |
|---|---|
| Infrastructure (AWS VMs = K8s nodes) | CPU, memory, disk |
| Kubernetes | Pod status, crash-loop restarts, deployment status, HPA replica counts |
| Application | Total HTTP requests, signups in last 30 days, latency, user activity |

How many metrics to collect depends on the company: 10, 50 or hundreds.

## 2.4 What is Prometheus?

- Most popular **open-source monitoring platform** in the Kubernetes world.
- **CNCF project**, reportedly the 2nd CNCF graduated project after Kubernetes.
- Competitors: Nagios, InfluxDB, Graphite, plus commercial tools. Many vendors build on Prometheus rather than writing their own.

### Prometheus architecture

```
   Exporters (node-exporter, kube-state-metrics, DB exporters, /metrics of apps)
         ▲  (pull / scrape)                     ▲ push (short-lived jobs)
         │                                      │
  ┌──────┴──────────────────────────────────────┴───────┐
  │                PROMETHEUS SERVER                    │
  │  Retrieval ──► Time Series DB (TSDB) ◄── HTTP Server│◄── PromQL / UI / Grafana
  │       ▲                                             │
  │  Service Discovery (which targets?)                 │
  └──────────────────────┬──────────────────────────────┘
                         ▼
                  Alertmanager ──► Slack / Email / PagerDuty
```

| Component | Role |
|---|---|
| **Retrieval** | Pulls (scrapes) metrics from targets |
| **TSDB (time-series DB)** | Stores metrics as `(timestamp, key=value)` |
| **HTTP server** | Accepts **PromQL** queries (UI, Grafana) |
| **Alertmanager** | Routes and fires alerts (Slack, email) |
| **Pushgateway** | For short-lived jobs that push metrics (ignore as a beginner) |
| **Service Discovery** | Tells Prometheus which targets/apps to scrape |

> Time-series DB: unlike a normal DB (`name=value`), every value is stored with its **timestamp**.

### Grafana

- Visualization and dashboard platform (not a monitoring tool).
- Advantages over the Prometheus UI: **better visualization**, **multi-data-source** (Prometheus, InfluxDB, Nagios, Graphite …) and **authentication/authorization** (SSO, roles for managers/devs/QA).
- Prometheus + Grafana = standard monitoring stack.

## 2.5 Practical: Install Prometheus + Grafana + Alertmanager on EKS

### Step 0: Create an EKS cluster (skip if you already have one)

```bash
# Create cluster (no node group)  (repo: day-2 README)
eksctl create cluster --name observability --region us-east-1 --without-nodegroup

# Associate OIDC provider (links K8s service accounts with IAM roles)
eksctl utils associate-iam-oidc-provider \
  --cluster observability --region us-east-1 --approve

# Create node group
eksctl create nodegroup --cluster observability --region us-east-1 \
  --name observability-ng --node-type t3.medium \
  --nodes 2 --nodes-min 2 --nodes-max 3
```

> **Why OIDC?** It lets a Kubernetes service account assume an IAM role (used later for EBS CSI with Elasticsearch). Not required for Day 2 itself.
> **Delete the cluster when done**, since EKS costs money.

### Step 1: Helm repos and namespace

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring
```

### Step 2: Custom values file (enable Alertmanager)

`custom_kube_prometheus_stack.yml` (repo) enables Alertmanager:

```yaml
alertmanager:
  enabled: true
```

### Step 3: Install kube-prometheus-stack

```bash
git clone https://github.com/iam-veeramalla/observability-zero-to-hero.git
cd observability-zero-to-hero/day-2

helm install stable prometheus-community/kube-prometheus-stack \
  -n monitoring -f custom_kube_prometheus_stack.yml
```

This installs **Prometheus, Grafana, Alertmanager, node-exporter (DaemonSet), kube-state-metrics, Prometheus Operator**.

```bash
kubectl get pods -n monitoring
kubectl get svc  -n monitoring
```

### Step 4: Access the UIs via port-forward

(Port-forward works on any cluster. In production use an **Ingress/ALB**.)

```bash
# Prometheus (9090)
kubectl port-forward svc/prometheus-operated -n monitoring 9090:9090

# Grafana (service port 80 → local 3000)
kubectl port-forward svc/stable-grafana -n monitoring 3000:80

# Alertmanager (9093)
kubectl port-forward svc/alertmanager-operated -n monitoring 9093:9093
```

> Service names depend on your Helm release name. Use `kubectl get svc -n monitoring`. On an EC2 instance add `--address 0.0.0.0` and browse to `<public-ip>:<port>`.

**Grafana login:** username `admin`, password `prom-operator` (default for this chart; check the repo docs or the `*-grafana` secret).

```bash
kubectl get secret -n monitoring stable-grafana -o jsonpath='{.data.admin-password}' | base64 -d
```

### Step 5: Prometheus as Grafana data source

Grafana → **Connections → Add new connection → Prometheus** → provide Prometheus URL, for example `http://prometheus-operated.monitoring.svc:9090`. With kube-prometheus-stack this data source is **auto-provisioned**.

## 2.6 Where does Prometheus get its metrics? (3 sources)

| # | Source | What it provides | How |
|---|---|---|---|
| 1 | **node-exporter** | Node/VM CPU, memory, disk, network (reads `/proc`, system files) | DaemonSet, one pod per node |
| 2 | **kube-state-metrics (KSM)** | K8s object state: pods, deployments, configmaps, secrets, restarts | Talks to the **API server**, single replica |
| 3 | **App `/metrics` endpoint** | Custom app metrics (HTTP requests, logins …) | Developers implement it, found via **ServiceMonitor** |

Other exporters: MySQL exporter, DB exporters and more.

**Why DaemonSet vs single pod?**
- node-exporter must read each node individually → **DaemonSet** (one per node).
- kube-state-metrics only calls the API server, which can be reached from any node → **1 replica**.

---

# Day 3: Prometheus in Practice, PromQL and Grafana Dashboards

## 3.1 Seeing exporters' raw data

```bash
kubectl get svc -n monitoring     # note ClusterIP of node-exporter (9100) and kube-state-metrics (8080)
```

The services are **ClusterIP**, so they are only reachable from inside the cluster. SSH/SSM into a node (on Minikube: `minikube ssh`):

```bash
curl <node-exporter-cluster-ip>:9100/metrics
curl <kube-state-metrics-cluster-ip>:8080/metrics | grep restart
curl <kube-state-metrics-cluster-ip>:8080/metrics | grep container
```

The output format is Prometheus text format: `metric_name{label="value"} number`.

Example: `kube_pod_container_status_restarts_total{namespace="...",pod="..."} 3`

## 3.2 Flow when you create a pod

```
kubectl run → API server → (scheduler/kubelet) → pod created
                     ▲
        kube-state-metrics watches the API server
                     │ exposes  /metrics
        Prometheus scrapes KSM → stores in TSDB
                     │
        User runs PromQL / Grafana shows graph
```

## 3.3 Demo: make a pod that keeps crashing

```bash
kubectl run busybox-crash --image=busybox --restart=Always -- /bin/sh -c "exit 1"
kubectl get pods -w         # CrashLoopBackOff, restarts increasing
```

Prometheus UI queries:

```promql
# all containers, all namespaces
kube_pod_container_status_restarts_total

# only default namespace
kube_pod_container_status_restarts_total{namespace="default"}

# a specific pod
kube_pod_container_status_restarts_total{namespace="default", pod="busybox-crash"}
```

Switch to the **Graph** tab and set the range to 1m/5m/30m/1h. Explore with **autocomplete** (type `kube_` …).

**CrashLoopBackOff timing:** the restart delay grows (10s, 20s, 40s … up to 5 min), so the graph shows restarts spreading further apart.

## 3.4 More PromQL

```promql
# ConfigMaps created, in kube-system
kube_configmap_created{namespace="kube-system"}

# Init container restarts
kube_pod_init_container_status_restarts_total

# Rate of restarts over 5 min (useful for alerting)
rate(kube_pod_container_status_restarts_total[5m])

# Aggregations
sum(kube_pod_container_status_restarts_total)
sum by (namespace) (kube_pod_container_status_restarts_total)
avg by (namespace) (container_memory_usage_bytes)     # average memory per namespace
```

**Aggregation operators:** `sum`, `avg`, `min`, `max`, `count` (most used: **sum and avg**), with `by (label)` or `without (label)`.

> You do not need to know every metric. Learn the common ones: pod restarts, configmaps/secrets count, CPU/memory/disk, HTTP requests, user signups.

## 3.5 Why Grafana if Prometheus has a UI?

| Prometheus UI | Grafana |
|---|---|
| Basic graphs | Rich dashboards |
| Only Prometheus | Many data sources (InfluxDB, Nagios, Graphite …) |
| No authn/authz | SSO / roles (view / edit / admin) |
| Monitoring tool | Visualization platform |

### Grafana practical

1. Dashboards ship by default (Kubernetes / Compute Resources / Namespace (Pods) and so on).
   If a panel shows no data, pick the **Prometheus** data source in the dropdown.
2. **Create own dashboard:** *New → Dashboard → Add visualization → select Prometheus* → paste query
   `kube_pod_container_status_restarts_total{namespace="default"}` → Run query → set time range → **Save**.
3. **Add more data sources:** Connections → Data sources → Add data source (InfluxDB, etc.).
4. **Administration**: users, teams, SSO, permissions.

## 3.6 Metric types (preview for Day 4)

`Counter`, `Gauge`, `Histogram`, `Summary` (see Day 4).

---

# Day 4: Instrumentation of Custom Metrics and Alertmanager

## 4.1 What is instrumentation?

Writing metrics/logs/traces **into the application code** so the observability stack has data to consume. Exporters cannot provide app-specific data such as logins in the last 30 days or request duration of a specific service.

> Without instrumentation, the best observability stack is useless.

## 4.2 Metric types

| Type | Behaviour | Examples |
|---|---|---|
| **Counter** | Only goes **up** (resets at restart) | `http_requests_total`, accounts created, errors total |
| **Gauge** | Goes **up and down** | CPU %, memory, queue length, number of ConfigMaps, temperature |
| **Histogram** | Observations counted in **buckets** (plus sum and count) | Request duration (`le=0.5, 1, 5, 10` s), response size |
| **Summary** | Like histogram, with quantiles calculated client-side | Request latency quantiles |

**Rule of thumb:**
- Always increasing? → **Counter**
- Can go up and down? → **Gauge**
- Need "how many were below X"/percentiles/latency? → **Histogram** (Summary is similar)

Analogy: metric types are like data types (string/list/dict), each for a different kind of data.

### Histogram bucket idea

Request took 4 ms? It is counted in the ≤5 ms bucket and every bucket above it (buckets are cumulative, the `le` label means "less than or equal").

PromQL for p95 latency:
```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

## 4.3 Node.js example with `prom-client`

```javascript
const client = require('prom-client');
const express = require('express');
const app = express();

// collect default Node.js process metrics (cpu, memory, event loop…)
client.collectDefaultMetrics();

// Counter: only increases
const httpRequestsTotal = new client.Counter({
  name: 'http_request_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'statusCode'],
});

// Histogram: request duration in buckets
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'statusCode'],
  buckets: [0.5, 1, 5, 10],
});

app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    const labels = { method: req.method, route: req.path, statusCode: res.statusCode };
    httpRequestsTotal.inc(labels);
    end(labels);
  });
  next();
});

// /metrics endpoint that Prometheus scrapes
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

app.listen(3000);
```

The demo app has **service-a** and **service-b** (Node.js) exposing `/healthy`, `/serverError`, `/notFound`, `/logs`, `/crash`, `/example`, `/call-to-service-b`, `/metrics`.

## 4.4 Deploy the demo app (repo: day-4)

```bash
cd day-4
kubectl create namespace dev
kubectl apply -k kubernetes-manifest/          # uses kustomize
kubectl get pods -n dev
kubectl get svc  -n dev                        # service-a is a LoadBalancer, wait for ELB DNS
```

Open `http://<ELB-DNS>/` (health check), `/logs`, `/metrics`.

## 4.5 Service Discovery with ServiceMonitor

After deploying, `http_request_total` is **not** visible in Prometheus. Reason: Prometheus does not know it should scrape `service-a`. With 10,000 services you don't want it scraping everything, so you explicitly tell it which ones, using a **ServiceMonitor** (custom resource from the Prometheus Operator):

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: service-a-monitor
  namespace: dev
  labels:
    release: stable            # must match your Helm release label so the Operator selects it
spec:
  selector:
    matchLabels:
      app: service-a           # label on the Service
  namespaceSelector:
    matchNames:
      - dev
  endpoints:
    - port: service-a-port     # NAME of the service port
      path: /metrics
      interval: 15s
```

```bash
kubectl apply -f service-monitor.yaml
```

Wait 1 to 2 minutes, then in Prometheus UI run `http_request_total` and change the range to 1m.

> **Full flow to remember (interview):**
> 1. **Instrument** the app (`/metrics`)
> 2. **Set up** Prometheus (monitoring stack)
> 3. **Service discovery** via ServiceMonitor

Check targets: Prometheus UI → **Status → Targets**.

## 4.6 Alertmanager: fire email alerts

Files in repo `day-4/alerts-alertmanager-servicemonitor-manifests/`:
`alerts.yaml` (rules), `alertmanager-config.yaml`, `email-secret.yaml`, `service-monitor.yaml`, `kustomization.yaml`.

### Step 1: Create a Gmail App Password
Google Account → Security → enable **2-Step Verification** → search **App passwords** → create one named `alertmanager` → copy the 16-char password.
(Use a dummy email account for demos.)

### Step 2: Base64-encode it and put it in the Secret
```bash
echo -n 'YOUR_APP_PASSWORD' | base64
```
```yaml
# email-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: alertmanager-email-pass
  namespace: monitoring
type: Opaque
data:
  password: <base64-string>
```
> Use `echo -n` (no newline), or authentication fails.

### Step 3: Alert rules (`PrometheusRule`)
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: custom-alert-rules
  namespace: monitoring
  labels:
    release: stable
spec:
  groups:
    - name: custom.rules
      rules:
        - alert: HighCPUUsage
          expr: 100 * (1 - avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m]))) > 80
          for: 2m
          labels:
            severity: warning
          annotations:
            summary: "High CPU on {{ $labels.instance }}"
        - alert: PodRestart
          expr: increase(kube_pod_container_status_restarts_total{namespace="dev"}[5m]) > 0
          for: 0m
          labels:
            severity: critical
          annotations:
            summary: "Pod {{ $labels.pod }} restarted"
```

### Step 4: Alertmanager receiver config (`AlertmanagerConfig`)
```yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: email-config
  namespace: monitoring
  labels:
    release: stable
spec:
  route:
    receiver: send-mail
    groupBy: ['alertname']
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 1h
  receivers:
    - name: send-mail
      emailConfigs:
        - to: you@example.com
          from: you@example.com
          smarthost: smtp.gmail.com:587
          authUsername: you@example.com
          authIdentity: you@example.com
          authPassword:
            name: alertmanager-email-pass
            key: password
          sendResolved: true
```

### Step 5: Apply and test
```bash
kubectl apply -k .
# Crash the demo app on purpose:
curl http://<ELB-DNS>/crash
kubectl get pods -n dev         # restarts increase
```
An email (visible on phone) arrives from Alertmanager about the pod restart.

Check in UIs: Prometheus → **Alerts** (Inactive/Pending/Firing); Alertmanager `:9093` shows active alerts.

**Alert lifecycle:** `Inactive → Pending (for: duration) → Firing → sent to Alertmanager → grouped/routed → receiver`.

---

# Day 5: Logging with the EFK Stack

## 5.1 Why logs?

Logs are messages written by developers so that users and operators can understand what the app is doing and debug it. The simple example is a shell script that adds two numbers: with log messages ("Starting addition…", "Addition complete, result = …") any user can follow what happened. In a 10,000-line app, logs tell you **where and why** it failed.

## 5.2 Why a centralized logging system?

With 100+ microservices across namespaces you cannot `kubectl logs` each one. Central logging aggregates logs in one place where you can search, for example "DB connection timeout", and see which services are affected. It is also critical for security events such as a Log4j vulnerability.

## 5.3 EFK vs ELK

| | EFK | ELK |
|---|---|---|
| **E** | Elasticsearch (store and search) | same |
| **F / L** | **Fluent Bit** (lightweight log **forwarder**) | **Logstash** (heavier log **aggregator**: advanced filtering, labeling, transformation) |
| **K** | Kibana (UI) | same |

Fluent Bit advantages: lightweight, few issues, **vendor neutral** (can forward to Splunk/others later). Use Logstash only when you need advanced processing.

## 5.4 Architecture (mirrors the Prometheus architecture)

```
Pods on every node ──► Fluent Bit (DaemonSet) ──push──► Elasticsearch (StatefulSet + EBS PVC) ◄── Kibana (UI, KQL)
   /var/log/containers/*.log          INPUT→FILTER→OUTPUT              gp2 volumes / snapshots
```

| Metrics world | Logs world |
|---|---|
| node-exporter (DaemonSet), **pull** | Fluent Bit (DaemonSet), **push** |
| Prometheus TSDB | Elasticsearch |
| Grafana / PromQL | Kibana / KQL |

## 5.5 Why IAM role for service account + EBS CSI driver?

Elasticsearch runs inside EKS but stores data on **EBS volumes** (an AWS service outside the cluster). For a pod to create/use EBS:
- Map the K8s **service account** to an **IAM role** (IRSA via the OIDC provider).
- Install the **EBS CSI driver** (creates EBS volumes automatically for PVCs using the `gp2` storage class).

## 5.6 Practical steps (repo: day-5)

```bash
# 1. IAM service account for the EBS CSI driver
eksctl create iamserviceaccount \
  --name ebs-csi-controller-sa \
  --namespace kube-system \
  --cluster observability \
  --role-name AmazonEKS_EBS_CSI_DriverRole \
  --role-only \
  --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --approve

# 2. Get the role ARN
ARN=$(aws iam get-role --role-name AmazonEKS_EBS_CSI_DriverRole --query 'Role.Arn' --output text)

# 3. Install the EBS CSI add-on
eksctl create addon --cluster observability --name aws-ebs-csi-driver \
  --version latest --service-account-role-arn $ARN --force

# 4. Namespace
kubectl create namespace logging
```

### Elasticsearch
```bash
helm repo add elastic https://helm.elastic.co
helm repo update

# elasticsearch values: use gp2 for volumeClaimTemplate (repo has this file)
helm install elasticsearch elastic/elasticsearch -f elasticsearch-values.yaml -n logging
```
`elasticsearch-values.yaml` (repo) sets, in essence:
```yaml
replicas: 2
volumeClaimTemplate:
  accessModes: ["ReadWriteOnce"]
  storageClassName: gp2
  resources:
    requests:
      storage: 5Gi
```

**Get credentials** (username is `elastic`):
```bash
kubectl get secrets -n logging elasticsearch-master-credentials \
  -o jsonpath='{.data.username}' | base64 -d; echo
kubectl get secrets -n logging elasticsearch-master-credentials \
  -o jsonpath='{.data.password}' | base64 -d; echo
```
Keep the password handy: Fluent Bit, Kibana and Jaeger all need it.

### Kibana
```bash
helm install kibana elastic/kibana -n logging --set service.type=LoadBalancer
kubectl get svc -n logging        # get the ELB DNS
# open: http://<ELB-DNS>:5601   (user: elastic, password from above)
```

### Fluent Bit
```bash
helm repo add fluent https://fluent.github.io/helm-charts
helm repo update
```
Edit `fluent-bit.yaml` (repo): in **both OUTPUT sections** set `HTTP_User elastic` and `HTTP_Passwd <password>`, then:
```bash
helm install fluent-bit fluent/fluent-bit -f fluent-bit.yaml -n logging
kubectl get pods -n logging      # one fluent-bit pod per node (DaemonSet)
```
If Helm complains about YAML near a line number (for example line 449), it is an **indentation problem**. Fix and re-run (`helm upgrade`).

### Fluent Bit configuration: 4 sections

| Section | Purpose | In the demo |
|---|---|---|
| **SERVICE** | Global settings (flush, log level, HTTP server) | defaults |
| **INPUT** | Where logs come from | `tail` on `/var/log/containers/*.log` |
| **FILTER** | Modify / drop / enrich records | Kubernetes filter and a **Lua script** that ignores the `logging` namespace (you can also ignore `kube-system`) |
| **OUTPUT** | Where to send | `es`: Host `elasticsearch-master`, Port `9200`, user/password, **TLS On** (required on EKS with the secured ES chart) |

### Test with an app
```bash
kubectl create namespace dev
kubectl apply -k day-4/kubernetes-manifest/ -n dev
kubectl logs -n logging <fluent-bit-pod>     # see "inotify_fs_add ... service-a" lines
```
Ignore the warning "failed to flush chunk" at the beginning (transient retry).

### Kibana: see logs
1. **Discover → Create data view** → name `log management` → index pattern matching the Fluent Bit index (for example `kubernetes_cluster-*` or `logstash-*`, depends on the config) → timestamp field `@timestamp` → **Save**.
2. Filter with **KQL**, for example:
```
kubernetes.namespace_name : "dev"
kubernetes.container_name : "service-a" and log : *error*
```

---

# Day 6: Distributed Tracing with Jaeger

## 6.1 Tracing: the travel itinerary analogy

Hyderabad → Hyderabad airport (45 min) → Dubai (3.5 h) → Boston airport (12 h) → cab to friend's house (**2.5 h instead of 30 min**). The itinerary with timestamps showed which **hop** caused the delay. That is tracing.

In microservices: `user → login → service-a → service-b → payment`. Expected 1 s but took 4 s. Tracing shows the time spent at every hop so you can find the slow one (for example B → payment took 60 µs instead of 30 µs).

### Vocabulary
- **Trace** = entire journey of one request.
- **Span** = one unit of work/hop in a trace (a service call, a function, a DB query), with start time and duration.
- **Context propagation** = passing trace ID across services (HTTP headers, gRPC metadata).

## 6.2 Two halves of implementing tracing

| Developers | DevOps/SRE |
|---|---|
| **Instrument** code (OpenTelemetry SDK; can go down to function level) | **Deploy** the tracing backend (Jaeger, Datadog, Dynatrace …) |

Auto-instrumentation and eBPF can give minimal traces without code changes, but deep traces require instrumentation.

## 6.3 Jaeger architecture

```
App (instrumented with OTel) ─► Agent ─► Collector ─► Storage (Elasticsearch / Cassandra) ◄─ Query ◄─ Jaeger UI
```

| Component | Role |
|---|---|
| **Agent** | Receives traces from the application |
| **Collector** | Receives and processes traces from the agent and writes them to storage |
| **Storage** | Elasticsearch (preferred) / Cassandra. Not bundled, you configure it |
| **Query + UI** | Search and view traces |

> **Modern note:** newer Jaeger versions (v1.5x+ / v2) deprecate the separate agent. Applications send OTLP straight to the collector. The concept is the same.

## 6.4 Practical (repo: day-6)

### Step 1: Elasticsearch (same as Day 5, steps 1-4 and Elasticsearch install)
If Day 5's Elasticsearch is still running you can reuse it. Otherwise repeat the IAM service account, EBS CSI driver, `logging` namespace and Elasticsearch Helm install.

### Step 2: Get credentials and CA certificate
```bash
# username "elastic"
kubectl get secrets -n logging elasticsearch-master-credentials -o jsonpath='{.data.username}' | base64 -d; echo
kubectl get secrets -n logging elasticsearch-master-credentials -o jsonpath='{.data.password}' | base64 -d; echo

# CA cert for secure (TLS) communication
kubectl get secret elasticsearch-master-certs -n logging \
  -o jsonpath='{.data.ca\.crt}' | base64 -d > ca-cert.pem
```

### Step 3: Tracing namespace, ConfigMap and Secret
```bash
kubectl create namespace tracing
kubectl create configmap jaeger-tls  --from-file=ca-cert.pem -n tracing
kubectl create secret generic es-tls-secret --from-file=ca-cert.pem -n tracing
```
(The CA cert is not very sensitive, so a ConfigMap is fine, and the repo mounts both.)

### Step 4: Update `jaeger-values.yaml`
Sections: **collector**, **query (UI)**, **storage**. You only change the **storage** section:
```yaml
storage:
  type: elasticsearch
  elasticsearch:
    host: elasticsearch-master.logging.svc.cluster.local
    port: 9200
    scheme: https
    user: elastic
    password: <PASTE-PASSWORD>
```
Service name and port stay the same, so only the **password** must be changed. Update it **before** installing.

### Step 5: Install Jaeger
```bash
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update
helm install jaeger jaegertracing/jaeger -n tracing -f jaeger-values.yaml

# Wrong password? fix the file and:
helm upgrade jaeger jaegertracing/jaeger -n tracing -f jaeger-values.yaml

kubectl get pods -n tracing     # agent, collector, query should be Running
```

### Step 6: Access the UI
```bash
kubectl port-forward svc/jaeger-query -n tracing 8080:80
# On EC2 use:   --address 0.0.0.0    and browse http://<public-ip>:8080
```
(Or change the service to LoadBalancer / use Ingress.)

### Troubleshooting seen in the video
`jaeger-query` in **CrashLoopBackOff** with **liveness/readiness probe failed** → caused by stale ConfigMap/Secret from an old Elasticsearch (wrong CA cert). Fix: delete the ConfigMap and Secret, regenerate `ca-cert.pem`, recreate both, restart pods.
```bash
kubectl describe pod <jaeger-query-pod> -n tracing
kubectl delete configmap jaeger-tls -n tracing
kubectl delete secret es-tls-secret -n tracing
# recreate as in Step 2 and Step 3
```

### Step 7: Deploy the instrumented demo app
Service A and B have `tracing.js` (OpenTelemetry):
```bash
kubectl create namespace dev
kubectl apply -k day-4/kubernetes-manifest/      # service-a + service-b
kubectl get svc -n dev                           # LoadBalancer DNS (wait 2-3 min)
```
Traffic generates traces: hit `/healthy` and `/call-to-service-b`.
Jaeger shows service names only after traffic arrives.

- `/healthy` trace: **6 spans**: middleware → Express init → logger → anonymous → handler.
- `/call-to-service-b`: **12 spans** across service-a → service-b.
- Click a span to see duration (µs), tags and process info.
- Jaeger UI extras: **System Architecture (dependency graph)** and **Monitor** tab (P99 latency; requires Prometheus).

## 6.5 OpenTelemetry instrumentation (Node.js, sketch of `tracing.js`)

```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');

const sdk = new NodeSDK({
  resource: new Resource({ 'service.name': 'service-a' }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://jaeger-collector.tracing.svc:4318/v1/traces',   // adjust to your collector
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
```
Load it **before** your app code (`node -r ./tracing.js index.js`).

---

# Day 7: End-to-End Project, OpenTelemetry Demo Application

## 7.1 About the project

The **OpenTelemetry Astronomy Shop demo**, maintained by observability vendors (Datadog, Dynatrace, Microsoft, Alibaba, Grafana Labs …). It is an e-commerce microservice app with many services in **different languages**:

| Service | Language |
|---|---|
| Cart | .NET |
| Checkout, Product catalog | Go |
| Recommendation | Python |
| Payment, Frontend, Ad etc. | Node.js / Java / others |
| Email | Ruby |
| Currency, Shipping | C++, Rust |
| Load generator | Python (Locust) |

It is ideal as a **resume/learning project**: pick a language you know, open the service's source, and see how **OTel traces and metrics** are instrumented. Go services import `otel`, `trace` and `metric` packages.

## 7.2 Why OpenTelemetry? (vendor neutrality)

Problem: if code uses the Prometheus client/Datadog SDK directly, switching tools means changing **every microservice**.

**OpenTelemetry (CNCF)** = vendor-neutral **APIs + SDKs** (+ Collector). Developers instrument once. Changing the backend (Prometheus → Datadog, Jaeger → Dynatrace) becomes just a **config change in the exporter**.

```
Microservice + OTel API/SDK
        │ emits metrics, logs, traces
        ▼
OTel Collector:  RECEIVER ─► PROCESSOR ─► EXPORTER  (configured in exporter config file)
                                              │
            ┌─────────────────────────────────┼───────────────┐
            ▼                                 ▼               ▼
        Jaeger (traces)                 Prometheus (metrics)   Logs backend
            │                                 │
       Elasticsearch DB                   TSDB → Grafana
```

## 7.3 Deploy (Helm)

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm install my-otel-demo open-telemetry/opentelemetry-demo

kubectl get pods            # ~20 pods
kubectl get svc
```

### Expose via port-forward
```bash
kubectl port-forward svc/my-otel-demo-frontendproxy 8080:8080
```
(On a cloud VM: add `--address 0.0.0.0` and use the VM public IP.)

| URL | What |
|---|---|
| `http://localhost:8080/` | Web store: add items to cart, change currency |
| `http://localhost:8080/jaeger/ui` | **Jaeger** UI (17 services) |
| `http://localhost:8080/grafana` | **Grafana** (auth disabled, preloaded dashboards) |
| `http://localhost:8080/loadgen/` | Load generator (Locust) |

Even without you clicking, the load generator creates traffic. Do your own actions to trace your own requests.

## 7.4 Explore traces in Jaeger

- Select the service `cart` → **Find Traces** → see front-end-proxy → front end → cart → `GetCart` spans with duration, container ID, cloud region, K8s node etc.
- `checkout`: ~47 spans, because checkout needs items in the cart first (cart → checkout → payment/shipping/email via gRPC).
- Errors show up on the failing span.

## 7.5 Explore metrics in Grafana

- Use the predefined **Demo Dashboard** (latency, error rate), or **New → Dashboard → Add visualization (Prometheus)**.
- Sample PromQL:
```promql
http_server_duration_seconds_bucket          # per service latency buckets
app_recommendations_counter_total            # recommendation service counter
```
- If you query `pod`/node CPU/memory metrics, you get **nothing**. This Prometheus doesn't include **node-exporter** or **kube-state-metrics**. Install the full **kube-prometheus-stack** (Day 2) to get these.

## 7.6 How to use the project for learning and the resume
1. Read the architecture diagram.
2. Choose a service in your language and read its instrumentation.
3. Deploy with Helm, explore Jaeger and Grafana.
4. Add kube-prometheus-stack, try EFK for logs and build your own dashboards/alerts.
5. Talk about: instrumentation (devs) vs implementation (DevOps), OTel collector pipeline, SLO-based alerts.

---

# Master Architecture Cheat Sheet

| Pillar | Answers | Collector on nodes | Storage | UI / Query | Mode |
|---|---|---|---|---|---|
| **Metrics** | What | node-exporter, kube-state-metrics, app `/metrics` | Prometheus TSDB | Grafana, PromQL | **Pull** (scrape) |
| **Logs** | Why | Fluent Bit (DaemonSet) | Elasticsearch (+EBS) | Kibana, KQL | **Push** (forward) |
| **Traces** | How | Jaeger agent / OTel collector | Elasticsearch / Cassandra | Jaeger UI | **Push** (OTLP) |

Namespaces used: `monitoring`, `logging`, `tracing`, `dev` (apps). Separate namespaces give easier RBAC and troubleshooting.

Default ports:

| Component | Port |
|---|---|
| Prometheus | 9090 |
| Alertmanager | 9093 |
| Grafana | 3000 (container) / 80 (svc) |
| node-exporter | 9100 |
| kube-state-metrics | 8080 |
| Elasticsearch | 9200 |
| Kibana | 5601 |
| Jaeger query UI | 16686 (svc often 80) |
| OTLP gRPC / HTTP | 4317 / 4318 |

---

# Troubleshooting Guide

| Symptom | Likely cause | Fix |
|---|---|---|
| Custom metric not in Prometheus | No ServiceMonitor, wrong labels or port name | Create ServiceMonitor, check `release` label, **Status → Targets** |
| Grafana dashboard empty | Wrong data source selected | Choose **Prometheus** in dropdown |
| Port-forward not reachable on a VM | Binds to 127.0.0.1 | Add `--address 0.0.0.0`, open the security group |
| Alert email not sent | Bad app password or base64 has trailing newline | Use `echo -n`, enable 2FA, check Alertmanager logs |
| Fluent Bit Helm error at line N | YAML indentation | Fix indentation, `helm upgrade` |
| Fluent Bit "failed to flush chunk" | Transient retry while ES is starting | Ignore unless it persists, then verify ES host/password/TLS |
| Nothing in Kibana | No data view, or wrong password in **both** OUTPUT blocks | Create data view, fix password |
| PVC Pending (Elasticsearch) | EBS CSI driver or IAM role missing | Install driver with correct role ARN |
| `jaeger-query` CrashLoopBackOff | Wrong ES password or stale CA cert ConfigMap/Secret | Recreate cert objects, `helm upgrade` |
| Jaeger shows no services | No traffic or app not instrumented | Hit the app endpoints, check OTel exporter URL |
| No node/pod metrics in OTel demo | node-exporter and KSM not installed | Install kube-prometheus-stack |

Debug basics:
```bash
kubectl get pods -n <ns>
kubectl describe pod <pod> -n <ns>
kubectl logs <pod> -n <ns> [-c container] [--previous]
kubectl get events -n <ns> --sort-by=.lastTimestamp
```

---

# Interview Questions and Model Answers

**1. What is observability?**
The ability to understand the internal state of a system (app, infrastructure, network) from its outputs: metrics, logs and traces. It tells you what is happening, why, and how to fix it.

**2. Monitoring vs observability?**
Monitoring covers one pillar (metrics) plus alerts and dashboards. Observability covers all three pillars and is the superset.

**3. Explain the three pillars with an example.**
Failed HTTP requests: metrics show the count and time, logs show the error reason at that timestamp, traces show which hop in the request path failed or was slow.

**4. Who implements observability?**
Both. Developers instrument telemetry; DevOps/SRE deploy and operate the stack and dashboards.

**5. What are SLI, SLO, SLA and error budget?**
SLI is the measured indicator (for example success rate). SLO is the target (99.9%). SLA is the contract with consequences. The error budget is the allowed failure (100% minus the SLO). Observability lets you track all of these.

**6. Explain Prometheus architecture.**
Retrieval scrapes exporters, apps and pushgateway, using service discovery. Data goes to the TSDB. The HTTP server answers PromQL. Alertmanager handles alerts. Grafana visualizes.

**7. Pull vs push?**
Prometheus pulls (scrapes); short-lived jobs use Pushgateway. Fluent Bit and OTel push.

**8. What do node-exporter and kube-state-metrics do? Why DaemonSet vs Deployment?**
node-exporter exposes node OS/hardware metrics, so it is a DaemonSet. KSM turns API-server object state into metrics, so one replica is enough.

**9. Counter vs gauge vs histogram?**
Counter only increases (requests). Gauge moves up and down (memory). Histogram buckets observations (latency) and allows percentiles via `histogram_quantile`.

**10. What is a ServiceMonitor?**
A Prometheus Operator CRD declaring which Services and endpoints to scrape, which avoids scraping everything in the cluster.

**11. Why Grafana when Prometheus has a UI?**
Richer dashboards, multiple data sources, authentication and authorization.

**12. EFK vs ELK?**
Fluent Bit is a lightweight forwarder and vendor-neutral. Logstash is a heavier aggregator with advanced transformations.

**13. How does Elasticsearch on EKS persist to EBS?**
EBS CSI driver creates the volumes for gp2 PVCs, and IRSA (service account ↔ IAM role through OIDC) gives permission.

**14. Trace vs span vs context propagation?**
A trace is the whole request journey, a span is one operation, and context propagation passes the trace ID between services.

**15. Why OpenTelemetry?**
It is vendor-neutral, so you instrument once and change the backend through exporter config instead of rewriting microservices.

**16. Describe the OTel collector pipeline.**
Receivers take data in, processors transform or batch it, exporters send it to backends (Jaeger, Prometheus, and others).

**17. An app shows high latency. How would you investigate?**
Metrics (P95/P99 dashboard, alert) → identify time window → logs for errors in that window → traces to find the slow span → fix with developers.

---

# Cleanup Commands

```bash
# Helm releases
helm uninstall stable -n monitoring
helm uninstall kibana fluent-bit elasticsearch -n logging
helm uninstall jaeger -n tracing
helm uninstall my-otel-demo

# Namespaces
kubectl delete ns monitoring logging tracing dev

# PVC/EBS volumes (check they're gone to avoid charges)
kubectl get pvc -A
aws ec2 describe-volumes --filters Name=status,Values=available

# Delete EKS cluster (important: avoids AWS costs)
eksctl delete cluster --name observability --region us-east-1
```

---

# Important Notes on Versions and Deprecations (read this)

The videos were recorded earlier, so check these when following along today:

1. **Bitnami charts/images:** if you use `bitnami/elasticsearch` or `bitnami/kibana`, note that since **28 Aug 2025** Bitnami stopped publishing new versioned images and charts to the public catalog. Old versions moved to `docker.io/bitnamilegacy` (no updates), and production-grade images became a paid offering. The repo's Day 5/6 flow uses the `elastic` Helm repo, so you are not directly affected, but avoid Bitnami charts in new setups without overriding image repositories.
2. **Elastic Helm charts** (`helm.elastic.co`) are **no longer actively maintained** (last chart line is 8.5.x). For anything beyond learning, use **Elastic Cloud on Kubernetes (ECK)** or OpenSearch.
3. **Jaeger:** v2 is built on the OpenTelemetry Collector and the standalone **agent is deprecated**. Application SDKs should send **OTLP** directly to the collector. Helm values keys differ between chart versions, so verify against the chart's `values.yaml`.
4. **kube-prometheus-stack** service names depend on your Helm release name (`stable-…`, `prometheus-…`). Always run `kubectl get svc -n monitoring`.
5. **Grafana default password** for this chart is `prom-operator` unless overridden.
6. **EKS versions, eksctl flags and IAM policy names** change. Cross-check with AWS docs.
7. The YAML blocks for ServiceMonitor, PrometheusRule, AlertmanagerConfig, Jaeger values and the Node.js snippets in these notes are **reconstructed reference versions** of what is shown in the videos. The exact files live in the day-wise folders of the repo, so prefer those when they differ.

### Useful references
- Prometheus docs: https://prometheus.io/docs/
- PromQL basics: https://prometheus.io/docs/prometheus/latest/querying/basics/
- kube-prometheus-stack chart: https://github.com/prometheus-community/helm-charts
- Fluent Bit docs: https://docs.fluentbit.io/
- Jaeger docs: https://www.jaegertracing.io/docs/
- OpenTelemetry docs: https://opentelemetry.io/docs/
- OTel Demo: https://opentelemetry.io/docs/demo/
- Course repo: `observability-zero-to-hero` (GitHub, link in the video description)

---

*End of notes. Suggested revision routine: read one day per sitting, re-run that day's commands on a fresh cluster, and answer the interview questions aloud.*
