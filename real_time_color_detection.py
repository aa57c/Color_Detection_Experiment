
import cv2
import pandas as pd
import time

# Load the color data
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        data = abs(R - int(csv.loc[i, 'R'])) + abs(G - int(csv.loc[i, 'G'])) + abs(B - int(csv.loc[i, 'B']))
        if data <= minimum:
            minimum = data
            cname = csv.loc[i, 'color_name']
    return cname

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


clicked = False
r = g = b = xpos = ypos = 0

# Start the webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', draw_function)

display_duration = 3  # Display duration in seconds
display_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if clicked:
        current_time = time.time()
        if current_time - display_time < display_duration:
            cv2.rectangle(frame, (20, 20), (750, 60), (b, g, r), -1)
            text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
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
