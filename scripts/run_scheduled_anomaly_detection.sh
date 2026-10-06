#!/usr/bin/env bash
# ==============================================================================
# Scheduled Anomaly Surveillance & Automated Alert Dispatch Runner (Task 10.4)
# Downtown San Diego Homeless Population Analysis
# Suitable for automated execution via Cron or Apache Airflow BashOperator
# ==============================================================================

set -euo pipefail

# Determine repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

# Activate virtual environment
if [[ -f "${REPO_ROOT}/.venv/bin/activate" ]]; then
    source "${REPO_ROOT}/.venv/bin/activate"
fi

TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
LOG_DIR="${REPO_ROOT}/data/logs"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/anomaly_surveillance_${TIMESTAMP}.log"

echo "======================================================================" | tee -a "${LOG_FILE}"
echo "Starting Scheduled Anomaly Surveillance: ${TIMESTAMP}" | tee -a "${LOG_FILE}"
echo "Repository Root: ${REPO_ROOT}" | tee -a "${LOG_FILE}"
echo "Log Destination: ${LOG_FILE}" | tee -a "${LOG_FILE}"
echo "======================================================================" | tee -a "${LOG_FILE}"

# Execute headless surveillance and alert dispatch
python anomaly_detection.py --schedule --send 2>&1 | tee -a "${LOG_FILE}"

EXIT_CODE=$?

if [[ ${EXIT_CODE} -eq 0 ]]; then
    echo "======================================================================" | tee -a "${LOG_FILE}"
    echo "✓ Surveillance execution completed successfully at $(date +"%Y-%m-%d %H:%M:%S")" | tee -a "${LOG_FILE}"
    echo "======================================================================" | tee -a "${LOG_FILE}"
    exit 0
else
    echo "======================================================================" | tee -a "${LOG_FILE}"
    echo "❌ Surveillance run failed with exit code ${EXIT_CODE}" | tee -a "${LOG_FILE}"
    echo "======================================================================" | tee -a "${LOG_FILE}"
    exit ${EXIT_CODE}
fi
