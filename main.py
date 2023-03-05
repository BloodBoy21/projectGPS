import utime
import lib.wifi as server
import lib.gps as gps
import lib.readEnv as env
import time
import machine

ssid = env.get_env('ssid')
password= env.get_env('password')

if __name__ == '__main__':
    try:
      server.connect(ssid, password)
      server.login()
      while True:
          if gps.uart.any():
            gps.buffer += gps.uart.readline()
            if gps.buffer is not None:
              [lat,lng] = gps.readData(gps.buffer)
              if lat and lng:
                  data = {
                      'lat': lat,
                      'lng': lng
                  }
                  server.send_data(data)
                  buffer = b''
                  time.sleep(18)
          if len(gps.buffer) > 50:
              buffer = b''
          utime.sleep_ms(100)
    except Exception as e:
        print(e)
        # time.sleep(5)
        # machine.reset()