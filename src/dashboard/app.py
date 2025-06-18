import sys
import os
from datetime import datetime, timedelta
import boto3
import pandas as pd
import requests
import streamlit as st
import subprocess

# === Path Config ===
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from sqlalchemy import func, cast, Date
from src.backend.database.configure import SessionLocal
from src.backend.models.user import User
from src.backend.models.exercise import Exercise
from src.backend.models.workout import Workout
from src.backend.models.logged_exercise import LoggedExercise
from src.backend.models.logged_exercise_set import LoggedExerciseSet


# === Page Config ===
st.set_page_config(page_title="Triance Developer Dashboard", layout="wide")
st.title("Triance Internal Developer Metrics Dashboard")

# === Section 1: EC2 Instance System Metrics ===
st.header("1. EC2 Instance System Metrics")

with st.expander("🔧 Uptime, Disk & Memory Info"):
    ec2_metrics = subprocess.getoutput("u" \
    "ptime && df -h | grep /dev/root && free -h")
    st.code(ec2_metrics, language="bash")

st.divider()

# === Section 2: RDS Instance Metrics ===
st.header("2. RDS Instance Metrics")

REGION = "us-east-2"
DB_INSTANCE_ID = "triance"
cloudwatch = boto3.client("cloudwatch", region_name=REGION)


def fetch_rds_metric(metric_name, stat="Average"):
    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName=metric_name,
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': DB_INSTANCE_ID}],
        StartTime=datetime.utcnow() - timedelta(minutes=30),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=[stat]
    )
    datapoints = metrics.get("Datapoints", [])
    if datapoints:
        return round(datapoints[-1][stat], 2)
    return "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("RDS CPU Utilization", f"{fetch_rds_metric('CPUUtilization')}%")
col2.metric("RDS Free Storage (MB)", fetch_rds_metric('FreeStorageSpace', stat='Minimum') // 1024**2)
col3.metric("RDS Connections", fetch_rds_metric('DatabaseConnections'))

st.divider()

# === Section 3: GitHub Repository Activity ===
st.header("3. GitHub Repository Activity")

GITHUB_REPO = "karavi1/Triance"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if GITHUB_TOKEN:
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    commits = requests.get(
        f"https://api.github.com/repos/{GITHUB_REPO}/commits",
        headers=headers
    ).json()

    actions = requests.get(
        f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs",
        headers=headers
    ).json()

    st.subheader("Latest Commit")
    if isinstance(commits, list) and commits:
        latest = commits[0]
        st.write(f"**{latest['commit']['message']}** by `{latest['commit']['author']['name']}`")
        st.write(f"Committed at: {latest['commit']['author']['date']}")

    st.subheader("Recent GitHub Actions")
    if "workflow_runs" in actions:
        for run in actions["workflow_runs"][:5]:
            st.write(f"- **{run['name']}** | Status: `{run['conclusion']}` | Trigger: {run['event']} | Time: {run['created_at']}")
else:
    st.warning("Set GITHUB_TOKEN to access GitHub data.")

st.divider()

# === Section 4: App Health Checks ===
st.header("5. Uptime Checks")

BACKEND_URL = "https://triance.app/api/custom-docs"
try:
    res = requests.get(BACKEND_URL, timeout=5)
    if res.status_code == 200:
        st.success("Backend is reachable ✅")
    else:
        st.warning(f"Backend responded with status code {res.status_code}")
except Exception as e:
    st.error(f"Backend not reachable: {e}")

st.divider()

# === Section 5: User Activity Logs ===
st.header("6. User Event Logs (TODO)")
st.info("Coming soon: Event logs based on user API activity")
st.info("Need to implement some OLAP data warehousing/metrics")