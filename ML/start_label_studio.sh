#!/bin/bash
# Start Label Studio with local file serving enabled

export LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/Users/pierrebastiani/Classification

cd /Users/pierrebastiani/Classification
.venv/bin/label-studio start
