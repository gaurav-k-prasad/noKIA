import visionrpi
import time


for i in range(5):
    print(visionrpi.get_data())
    time.sleep(2)
