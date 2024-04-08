import serial
import keyboard
import time

# Initialize serial port
ser = serial.Serial('COM1', 115200)  # Change 'COM1' to your serial port
ser.timeout = 1  # Set timeout to 1 second (adjust as needed)

# Define the string to trigger key press
trigger_string_1 = "clench"
trigger_string_2 = "swiperight"


while True:
    # Read serial data until newline character is encountered
    incoming_data = ser.readline().decode().strip()
    
    if incoming_data:
        print("Received:", incoming_data)
        
        # Check if the received data matches the trigger string
        if incoming_data == trigger_string_1:
            # Simulate key press (e.g., press 'a' key)
            keyboard.press('c')
            keyboard.release('c')
            print("Key 'a' pressed")
            time.sleep(0.7)
        if incoming_data == trigger_string_2:
            # Simulate key press (e.g., press 'a' key)
            keyboard.press('s')
            keyboard.release('s')
            print("Key 'a' pressed")
            time.sleep(0.7)
        else:
            keyboard.press('n')
            keyboard.release('n')



