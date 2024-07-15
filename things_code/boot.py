import network
import esp
import gc

esp.osdebug(None)
gc.collect()

ssid = 'IZZI-6D04'
password = 'F0AF85386D04'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

print('Network Connection Successful')
print(station.ifconfig())
