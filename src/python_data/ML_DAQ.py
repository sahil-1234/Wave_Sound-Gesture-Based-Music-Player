import serial
import numpy as np
import matplotlib.pyplot as plt
import time

# Settings
serial_port = 'COM10'
baud_rate = 115200
label_name = 'clench'
num_class_samples = 50
# Number of samples to collect for this label category
time_per_sample = 0.6    # Seconds
accel_sample_rate = 100  # Times per second (Hz) to read from acceleromater
num_accel_samples = int(time_per_sample * accel_sample_rate)

# Test Serial port (open, wait for Arduino to reset, read line, close)
ser = serial.Serial(serial_port, baud_rate, timeout=1)
time.sleep(2)
ser.write('r'.encode('ascii'))
line = ser.readline()
ser.close()
print(line)


# Open serial port and read lines
def capture_accel(ser, nsamples):
    samples = np.zeros((nsamples, 6))
    for i in range(nsamples):

        # Use timer to determine when to take measurement next
        start = time.time()

        # Transmit 'r' to have Arduino respond with X, Y, and Z acceleration
        ser.write('r'.encode('ascii'))
        line = ser.readline()
        parsed = line.decode().rstrip().split('\t')
        sample = np.array([float(axis) for axis in parsed])
        samples[i] = sample

        # Wait before reading again
        while (time.time() - start) < (1. / accel_sample_rate):
            pass

    return samples


# Capture sample set
accel_data = np.zeros((num_class_samples, num_accel_samples, 6))
ser = serial.Serial(serial_port, baud_rate, timeout=1)
print('Waiting for Arduino to reset...')
time.sleep(2)
i = 0
while i < num_class_samples:
    input('Press enter and draw shape with board')
    try:

        # Get sample from Arduino
        samples = capture_accel(ser, num_accel_samples)
        accel_data[i] = np.array(samples)
        print('Sample', i, 'captured with shape:', accel_data[i].shape)
        i += 1

    except:
        print('Error parsing samples. Try again.')
        pass
ser.close()

# Plot a few
for sample_idx in range(4):
    fig = plt.figure(figsize=(14,2))
    ax = fig.add_subplot(111)
    ax.plot(accel_data[sample_idx, :, 0], label='ax')
    ax.plot(accel_data[sample_idx, :, 1], label='ay')
    ax.plot(accel_data[sample_idx, :, 2], label='az')
    ax.plot(accel_data[sample_idx, :, 3], label='gx')
    ax.plot(accel_data[sample_idx, :, 4], label='gy')
    ax.plot(accel_data[sample_idx, :, 5], label='gz')
    plt.legend(loc='upper left')
plt.show()


# Save raw accelerometer data
np.save(label_name, accel_data)

# Test: load array
test_data = np.load(label_name + '.npy')
print(test_data)

# Save raw accelerometer data as CSV
csv_filename = label_name + '.csv'
np.savetxt(csv_filename, accel_data.reshape(-1, accel_data.shape[-1]), delimiter=',')