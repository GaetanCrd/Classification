# Overnight Batch Prediction Generation

This script generates ML predictions for all tasks in your Label Studio project overnight.

## Setup

1. **Get your API token** from Label Studio:

   - Go to: http://localhost:8080/user/account
   - Copy your "Access Token"

2. **Make sure both services are running**:

   ```bash
   # Label Studio (Terminal 1)
   ./start_label_studio.sh

   # ML Backend (Terminal 2)
   cd custom_ml_backend
   ../.venv/bin/python _wsgi.py
   ```

## Quick Start (Interactive)

Run the script and it will prompt you for your API token:

```bash
python3 generate_predictions_batch.py
```

The script will:

- Show you a summary of tasks to process
- Estimate how long it will take (~30 seconds per image)
- Ask for confirmation before starting
- Save progress to `prediction_progress.json` so you can resume if interrupted

## Run Overnight (Unattended)

For a truly hands-off overnight run:

```bash
# Set your API token (get it from http://localhost:8080/user/account)
export LABEL_STUDIO_TOKEN='your-api-token-here'

# Run in background with nohup
nohup ./run_predictions_overnight.sh > predictions.log 2>&1 &

# Check progress
tail -f predictions.log
```

## Monitoring Progress

While running, you can check:

```bash
# View live progress
tail -f predictions.log

# Check progress file
cat prediction_progress.json
```

## Resume After Interruption

If the script is interrupted (computer sleep, network issue, etc.), just run it again:

```bash
python3 generate_predictions_batch.py
```

It will automatically resume from where it left off using `prediction_progress.json`.

## Expected Time

With 102 tasks at ~30 seconds each on CPU:

- **Estimated: 51 minutes (0.85 hours)**
- Could be faster if SAM finds few objects
- Could be slower if images are large or have many feathers

## What the Script Does

For each task:

1. Fetches task data from Label Studio
2. Sends it to the ML backend (SAM + metadata)
3. Receives predictions (bounding boxes + attributes)
4. Creates a prediction in Label Studio
5. Saves progress

## Troubleshooting

**"ML Backend is not responding"**

- Make sure the ML backend is running: `curl http://localhost:9090/health`
- Restart it: `cd custom_ml_backend && ../.venv/bin/python _wsgi.py &`

**"Failed to fetch tasks: 401"**

- Your API token is incorrect or expired
- Get a new one from http://localhost:8080/user/account

**"Timeout" errors**

- Some images might take longer than 5 minutes
- The script will mark them as failed and continue
- You can manually trigger predictions for failed tasks in Label Studio

**Script is too slow**

- SAM runs on CPU, which is slow
- Consider lowering detection thresholds to make it faster (fewer masks to process)
- Or let it run overnight as intended 😴

## After Completion

Once done:

1. Go to Label Studio: http://localhost:8080
2. You'll see predictions (bounding boxes) on all tasks
3. Review and correct them as needed
4. The attributes (colors, size, motif) are pre-filled from your metadata

Enjoy your semi-automated labeling! 🎉
