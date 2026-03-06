#!/bin/bash
# Scripts for generating and serving Allure Report

RESULTS_DIR="./reports/allure-results"
REPORT_DIR="./reports/allure-report"

# 1. Clean previous results/report
echo "Cleaning old reports..."
# rm -rf $REPORT_DIR

# 2. Check if allure command is installed
if ! command -v allure &> /dev/null
then
    echo "Error: 'allure' command not found. Please install it (e.g., brew install allure)."
    exit 1
fi

# 3. Generate HTML report
echo "Generating static HTML report from $RESULTS_DIR..."
allure generate $RESULTS_DIR -o $REPORT_DIR --clean

# 4. Success message
echo "Report successfully generated to $REPORT_DIR"
echo "To view it, run: allure open $REPORT_DIR"
