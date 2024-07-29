import cv2
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import time
import logging

# Configure logging
logging.basicConfig(filename='k_nearest_real_time_color_detection.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the color data
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv('colors.csv', names=index, header=None)

# Prepare the data for training
X = csv[['R', 'G', 'B']]
y = csv['color_name']

# Initialize and train the k-NN model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

def get_color_name_knn(R, G, B):
    color_df = pd.DataFrame([[R, G, B]], columns=['R', 'G', 'B'])
    color = knn.predict(color_df)[0]
    return color

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked, display_time
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        display_time = time.time()
        color_name = get_color_name_knn(r, g, b)
        logging.info(f'{color_name} R={r} G={g} B={b}')

clicked = False
r = g = b = xpos = ypos = 0
display_duration = 3  # Display duration in seconds
display_time = 0

# Start the webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', draw_function)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Check if the banner should still be displayed
    if clicked:
        current_time = time.time()
        if current_time - display_time < display_duration:
            cv2.rectangle(frame, (20, 20), (750, 60), (b, g, r), -1)
            text = get_color_name_knn(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
            cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            if r + g + b >= 600:
                cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        else:
            clicked = False
    
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(20) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
