#!/bin/bash
# process_pipeline.sh - Main wrapper script to run the entire data pipeline
# This will be called by the Dash application or can be run manually via SSH

# Determine the base directory based on script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BASE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Configuration - using relative paths from the project structure
DATA_DIR="${BASE_DIR}/data"
RAW_DIR="${DATA_DIR}/raw"
ARCHIVE_DIR="${DATA_DIR}/archive"
PROCESSED_DIR="${DATA_DIR}/processed"
FINAL_DIR="${DATA_DIR}/final"
LOG_DIR="${DATA_DIR}/.logs"

# Ensure output directories exist
mkdir -p "$ARCHIVE_DIR" "$PROCESSED_DIR" "$FINAL_DIR" "$LOG_DIR"

# Log file for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_DIR}/pipeline_${TIMESTAMP}.log"

# Function to log messages to both console and log file
log_message() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" | tee -a "$LOG_FILE"
}

# Function to run a python script safely
run_python_script() {
    local script_name=$1
    local script_path="${SCRIPT_DIR}/${script_name}"
    
    log_message "Running: ${script_name}"
    
    if [ ! -f "$script_path" ]; then
        log_message "ERROR: Script not found: ${script_path}"
        return 1
    fi
    
    # Pass necessary directories as arguments to the Python script
    python "$script_path" \
        --raw "$RAW_DIR" \
        --processed "$PROCESSED_DIR" \
        --output "$DATA_DIR" \
        --log "$LOG_FILE" 2>&1
    
    local status=$?
    if [ $status -ne 0 ]; then
        log_message "ERROR: ${script_name} failed with status ${status}"
        return $status
    else
        log_message "${script_name} completed successfully"
        return 0
    fi
}

# Function to archive raw data files
archive_files() {
    log_message "Archiving raw data files"
    for file in "$RAW_DIR"/*; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            name="${filename%.*}"
            ext="${filename##*.}"
            archived_name="${name}_${TIMESTAMP}.${ext}"


            if mv "$file" "${ARCHIVE_DIR}/${archived_name}"; then

                log_message "Archived: ${filename} as ${archived_name}"
            else
                log_message "ERROR: Failed to archive ${filename}"
            fi
        fi
    done
}

# Start pipeline
log_message "=== Starting data pipeline ==="
log_message "Base directory: ${BASE_DIR}"
log_message "Raw data directory: ${RAW_DIR}"

# Debug: List contents of raw directory
log_message "Contents of raw directory:"
ls -la "$RAW_DIR" | tee -a "$LOG_FILE"

# Execute Python Script 1 - tidy assess and recc
if run_python_script "process_iac.py"; then
    log_message "Step 1 completed: Processed assess and recc data"
else
    log_message "ERROR: Failed at Step 1. Exiting pipeline."
    exit 1
fi

# Execute Python Script 2 - EC emission factors
if run_python_script "generate_ec_emission_factors.py"; then
    log_message "Step 2 completed: Generated EC emission factors"
else
    log_message "ERROR: Failed at Step 2. Exiting pipeline."
    exit 1
fi

# Execute Python Script 3 - PPI dataset
if run_python_script "process_ppi.py"; then
    log_message "Step 3 completed: Processed PPI dataset"
else
    log_message "ERROR: Failed at Step 3. Exiting pipeline."
    exit 1
fi

# Execute Python Script 4 - Integration
if run_python_script "integrate_data.py"; then
    log_message "Step 4 completed: Final data integration"
else
    log_message "ERROR: Failed at Step 4. Exiting pipeline."
    exit 1
fi

# Archive raw data files (copy instead of move to preserve originals)
archive_files

log_message "=== Pipeline completed successfully ==="
echo "All data processing steps completed successfully!"
exit 0