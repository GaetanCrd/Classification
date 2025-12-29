"""
WSGI entry point for Label Studio ML Backend
"""
import os
import sys

# Add current directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from label_studio_ml.api import init_app
from model import SAMWithMetadata

# Initialize the ML backend app with the model class
# Pass model_dir so the backend can store job artifacts
app = init_app(
    model_class=SAMWithMetadata,
    model_dir=os.path.join(backend_dir, 'model_storage')
)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090, debug=False)
