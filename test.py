import cv2
import easyocr
# import numpy as np

class WebcamEasyOCR:
    def __init__(self, languages=['en']):
        print("Initializing EasyOCR...")
        self.reader = easyocr.Reader(languages)
        self.cap = None
        print("EasyOCR initialized!")

    def start_camera(self, camera_index=0):
        """Start the webcam"""
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
        print("Camera started. Press 'q' to quit, 's' to capture and analyze")
    
    def process_frame(self, frame):
        """Process frame with EasyOCR"""
        try:
            # EasyOCR can work directly with the frame (numpy array)
            results = self.reader.readtext(frame)
            return results
        except Exception as e:
            print(f"Error processing frame: {e}")
            return []

    def draw_results(self, frame, results):
        """Draw bounding boxes and text on the frame"""
        for (bbox, text, confidence) in results:
            # Only show results with decent confidence
            if confidence > 0.3:
                # Get bounding box coordinates
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = (int(top_left[0]), int(top_left[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                
                # Draw rectangle around text
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                
                # Put text above the rectangle
                cv2.putText(frame, f"{text} ({confidence:.2f})", 
                           (top_left[0], top_left[1] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        return frame
    
    def run(self):
        """Main loop for webcam OCR"""
        self.start_camera()
        
        # Process every nth frame to improve performance
        frame_count = 0
        process_every = 3  # Process every 10th frame
        last_results = []
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Process OCR every few frames to improve performance
                if frame_count % process_every == 0:
                    last_results = self.process_frame(frame)
                    
                    # Print detected text to console
                    if last_results:
                        print("\n--- Detected Text ---")
                        for (bbox, text, confidence) in last_results:
                            if confidence > 0.3:
                                print(f"Text: '{text}' (Confidence: {confidence:.2f})")
                        print("-" * 20)
                
                # Draw results on current frame
                frame_with_results = self.draw_results(frame.copy(), last_results)
                
                # Display the frame
                cv2.imshow('EasyOCR Webcam', frame_with_results)
                
                frame_count += 1
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Force process current frame when 's' is pressed
                    print("Processing current frame...")
                    results = self.process_frame(frame)
                    if results:
                        print("\n=== SNAPSHOT RESULTS ===")
                        for (bbox, text, confidence) in results:
                            print(f"Text: '{text}' (Confidence: {confidence:.2f})")
                        print("=" * 25)
                    else:
                        print("No text detected in current frame")
                        
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Application closed")

def main():
    # You can add more languages like ['en', 'ch_sim', 'ja'] for Chinese and Japanese
    ocr_app = WebcamEasyOCR(languages=['en', 'id'])
    ocr_app.run()

if __name__ == "__main__":
    main()