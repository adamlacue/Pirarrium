import cv2
import datetime
import time

# Open the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)

# Set duration to 5 seconds
duration_seconds=5

# Get current date for the output filename
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
output_filename = f"C:\\Users\\adaml\\Desktop\\SpringTerm\\Capstone\\piCode\\dailyCapture_{current_date}.avi" # Replace with your desired destination

# Set the video codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))

# Record video for the specified duration
start_time = time.time()
while time.time() - start_time < duration_seconds:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    cv2.imshow('Recording', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
