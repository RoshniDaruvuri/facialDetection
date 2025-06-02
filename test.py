import os
import cv2
import numpy as np
import warnings
import time
import sys

# Add the Silent-Face-Anti-Spoofing directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Silent_Face_Anti_Spoofing.src.anti_spoof_predict import AntiSpoofPredict
from Silent_Face_Anti_Spoofing.src.generate_patches import CropImage
from Silent_Face_Anti_Spoofing.src.utility import parse_model_name

warnings.filterwarnings('ignore')

def check_image(image):
    height, width, channel = image.shape
    if width/height != 3/4:
        print("Image is not appropriate!!!\nHeight/Width should be 4/3.")
        return False
    else:
        return True

def test(image, model_dir, device_id):
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()
    
    # Ensure image is in correct format
    if len(image.shape) != 3 or image.shape[2] != 3:
        print("Invalid image format")
        return 0
    
    # Resize image to have 3:4 width to height ratio
    image = cv2.resize(image, (int(image.shape[0] * 3 / 4), image.shape[0]))
    result = check_image(image)
    if result is False:
        return 0
        
    # Get face bbox
    image_bbox = model_test.get_bbox(image)
    if image_bbox is None:
        print("No face detected")
        return 0
        
    prediction = np.zeros((1, 3))
    test_speed = 0
    
    # Check if model directory exists and contains models
    if not os.path.exists(model_dir):
        print(f"Model directory not found: {model_dir}")
        return 0
        
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.pth')]
    if not model_files:
        print("No model files found in directory")
        return 0
    
    # sum the prediction from single model's result
    for model_name in model_files:
        try:
            h_input, w_input, model_type, scale = parse_model_name(model_name)
            param = {
                "org_img": image,
                "bbox": image_bbox,
                "scale": scale,
                "out_w": w_input,
                "out_h": h_input,
                "crop": True,
            }
            if scale is None:
                param["crop"] = False
            img = image_cropper.crop(**param)
            start = time.time()
            prediction += model_test.predict(img, os.path.join(model_dir, model_name))
            test_speed += time.time()-start
        except Exception as e:
            print(f"Error processing model {model_name}: {str(e)}")
            continue

    # If no successful predictions were made
    if np.sum(prediction) == 0:
        print("No successful predictions")
        return 0

    # draw result of prediction
    label = np.argmax(prediction)
    value = prediction[0][label]/2
    
    if label == 1:
        print("Real face detected with confidence: {:.2f}".format(value))
    else:
        print("Fake face detected with confidence: {:.2f}".format(value))
    
    return label 