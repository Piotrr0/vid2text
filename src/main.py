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
    height = int(gray_frame.shape[0])
    width = int(gray_frame.shape[1] )
    ascii_art = ""

    for y in range(height):
        for x in range(width):
            gray_value = gray_frame[y, x]
            index = int((gray_value / 255) * (len(mapping) - 1))
            ascii_art += mapping[index]
        ascii_art += "\n" 

    return ascii_art

def resize_frame(frame, resize_factor):
    height = frame.shape[0]
    width = frame.shape[1]

    resize_height = int(height / resize_factor)
    resize_width = int(width / resize_factor)
    return cv2.resize(frame, (resize_height, resize_width))


def main():
    vid_path = "../video/example.mp4"
    mapping = [' ', '.', ':', '*', '%', '&', '#', '@']
    cap = cv2.VideoCapture(vid_path)
        
    frame_resize_factor = 5
    
    frame_width = 800
    frame_height = 800
    frame_rate = 30
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
    
        resized_frame = resize_frame(frame, frame_resize_factor)
        gray_frame = to_gray(resized_frame)
        ascii_art = map_to_ascii(gray_frame, mapping)

        ascii_frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        for i, line in enumerate(ascii_art.split("\n")):
            y = 15 + i * 15
            cv2.putText(ascii_frame, line, (int(frame_width/2), y), font, 0.4, (255, 255, 255), 1)

        out.write(ascii_frame)
        cv2.imshow('frame', ascii_frame)
        if cv2.waitKey(10) == ord('q'):
            break

        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()