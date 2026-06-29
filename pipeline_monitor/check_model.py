from ultralytics import YOLO

# Load your model
model = YOLO("my_trained_model.pt")

print("="*40)
print("MODEL INTERROGATION RESULTS")
print("="*40)
print(f"Class Names Dictionary: {model.names}")
print("-"*40)

# Try to detect a blank black image just to see if it triggers properly
import numpy as np
dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
results = model(dummy_image, verbose=False)
print(f"Model loaded successfully and is ready to infer.")