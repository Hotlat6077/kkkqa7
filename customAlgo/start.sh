#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PID_FILE="service01.pid"
LOG_FILE="service01.out"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Already running, pid=$(cat "$PID_FILE")"
  exit 0
fi

nohup python3 service01.py > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "Started, pid=$(cat "$PID_FILE"), log=$LOG_FILE"
