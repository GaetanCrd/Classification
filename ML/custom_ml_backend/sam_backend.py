"""
Custom SAM ML Backend entry point
This file must be named exactly 'model.py' and define a class inheriting from LabelStudioMLBase
"""

from .model import SAMWithMetadata

# Export the model class so label-studio-ml can find it
NewModel = SAMWithMetadata
