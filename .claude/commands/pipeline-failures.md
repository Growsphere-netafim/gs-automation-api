# Pipeline Failures Analyzer

Analyze Azure DevOps pipeline failures for gs-automation-api.

## Usage

When the user runs `/pipeline-failures` with a build ID or URL, do the following:

1. Extract the build ID from the input (from URL `buildId=XXXXX` or directly as a number)
2. Check if `AZURE_DEVOPS_PAT` is set in the environment. If not, instruct the user to set it:
   ```
   export AZURE_DEVOPS_PAT=your_pat_here
   ```
   Then explain how to create a PAT: Azure DevOps → User Settings → Personal Access Tokens → New Token (Scopes: Build Read, Test Management Read)

3. Run the analysis script:
   ```bash
   source .venv/bin/activate 2>/dev/null || true
   python scripts/fetch_pipeline_failures.py --build-id <BUILD_ID>
   ```

4. Based on the output, provide a concise diagnosis:
   - If all failures share the same error → root cause is clear, suggest fix
   - If 401/403 errors → authentication issue
   - If 404 errors → missing test data / wrong IDs
   - If 500 errors → API/environment issue in QA1
   - If mixed errors → analyze top groups separately

## Project Context
- Org: netafimdf
- Project: NetbeatVx
- Pipeline: gs-automation-api nightly
- Azure DevOps URL pattern: https://netafimdf.visualstudio.com/NetbeatVx/_build/results?buildId=XXXXX
