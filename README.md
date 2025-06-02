# Face Attendance System

## Description

This project is a Face Attendance System that uses face recognition and anti-spoofing technology to securely log user attendance. It leverages computer vision and deep learning to detect real faces, prevent spoofing attacks, and manage user logins/logouts with a simple graphical interface. The system is built in Python and uses a pre-trained anti-spoofing model.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/face-attendance-system.git
cd face-attendance-system
```

### 2. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:

- opencv-python
- pillow
- numpy
- face-recognition
- torch
- torchvision

> **Note:** You may need to install additional dependencies for the anti-spoofing model in `Silent_Face_Anti_Spoofing/requirements.txt` if you plan to retrain or test the model separately.

## Usage

1. **Database directory:**  
   The `db/` directory is used to store images of registered users. This directory will be created automatically by the application if it does not already exist. Each image should be named after the user (e.g., `alice.jpg`). The system will use these images for face recognition.

2. **Run the application:**  
   ```bash
   python main.py
   ```
   This will launch a GUI window with options to log in, log out, or register a new user.

3. **Register a new user:**  
   Use the "register new user" button in the GUI to capture a new user's face and add them to the database.

4. **Login/Logout:**  
   Use the "login" and "logout" buttons to record attendance. The system will check for real faces using the anti-spoofing model before recognizing the user.

5. **Attendance Log:**  
   All login and logout events are recorded in `log.txt` with timestamps.

## Dependencies

- opencv-python
- pillow
- numpy
- face-recognition
- torch
- torchvision

For anti-spoofing model (in `Silent_Face_Anti_Spoofing/`):
- See `Silent_Face_Anti_Spoofing/requirements.txt` for additional requirements.

## Anti-Spoofing Model

The anti-spoofing model is included as a submodule in `Silent_Face_Anti_Spoofing/`.  
For more details, see the [Silent_Face_Anti_Spoofing README](Silent_Face_Anti_Spoofing/README.md).

## Contributing

Feel free to fork this repository and submit pull requests. When contributing, please ensure that your code adheres to the existing style and includes appropriate documentation.

---
