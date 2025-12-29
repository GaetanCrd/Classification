#!/usr/bin/env python
"""
Start script for custom SAM ML backend
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from label_studio_ml.api import init_app

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Start SAM with Metadata ML Backend')
    parser.add_argument('--model-path', type=str, required=True,
                        help='Path to SAM model checkpoint')
    parser.add_argument('--port', type=int, default=9090,
                        help='Port to run server on')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host to bind to')
    
    args = parser.parse_args()
    
    # Set model path as environment variable
    os.environ['MODEL_PATH'] = args.model_path
    
    print(f"🚀 Starting SAM with Metadata backend on {args.host}:{args.port}")
    print(f"📦 Using model: {args.model_path}")
    
    app = init_app(__name__)
    app.run(host=args.host, port=args.port, debug=False)
