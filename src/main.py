import cv2
import numpy as np

def to_gray(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    gray_frame = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            blue = frame[y, x, 0]
            green = frame[y, x, 1]
            red = frame[y, x, 2]
            
            gray_value = int(0.2989 * red + 0.5870 * green + 0.1140 * blue)
            gray_frame[y, x] = gray_value

    return gray_frame

def map_to_ascii(gray_frame, mapping):
    height = gray_frame.shape[0]
    width = gray_frame.shape[1]
    ascii_art = ""

    for y in range(height):
        for x in range(width):
            gray_value = gray_frame[y, x]
            index = int((gray_value / 255) * (len(mapping) - 1))
            ascii_art += mapping[index]
        ascii_art += "\n" 

    return ascii_art


def main():
    vid_path = "../video/example.mp4"
    mapping = ['@', '#', '&', '%', '*', ':', '.', ' '] 
    cap = cv2.VideoCapture(vid_path)
        
    scale_percent = 50
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        resized_frame = cv2.resize(frame, (width, height))
        print(resized_frame.shape)
        
        gray_frame = to_gray(resized_frame)
        ascii_art = map_to_ascii(gray_frame, mapping)
        print(ascii_art)
        
    cap.release()

if __name__ == "__main__":
    main()