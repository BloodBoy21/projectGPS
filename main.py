from machine import UART, Pin
import utime
import ure
# Configure the UART interface
uart = machine.UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(4), rx=Pin(5))
utime.sleep_ms(1000) # wait for the GPS to boot up

buffer = b''

def getLanAndLon(gpgll) -> tuple:
    '''
    Extract latitude and longitude values from a GPGGL string and return them as a tuple
    '''
    gpgll = "$GPGLL,1759.79177,N,09433.46408,W,214557.00,A,A*7D"

    match = ure.search('\$GPGLL,(\d+\.\d+),([NS]),(\d+\.\d+),([EW])', gpgll)
    if match:
        # Extract latitude and longitude values and their directional indicators
        lat_deg = int(match.group(1)[:2])
        lat_min = float(match.group(1)[2:])
        lat_dir = match.group(2)
        lon_deg = int(match.group(3)[:3])
        lon_min = float(match.group(3)[3:])
        lon_dir = match.group(4)
        
        # Calculate decimal degrees values from extracted values
        lat = lat_deg + lat_min/60.0
        if lat_dir == "S":
            lat = -lat
        lon = lon_deg + lon_min/60.0
        if lon_dir == "W":
            lon = -lon
        print(f"lat: {lat}, lon: {lon}")
        return [lat, lon]
    return [None, None]


def findGPGLL(line) -> bytes or None:
    '''
    Find the GPGLL string in the line buffer and return it
    '''
    codes = line.split(b'\r\n')
    for code in codes:
        if b'$GPGLL' in code:
            print("*"*20)
            print(f"gpgll: {code}")
            print("*"*20)
            data = code.split(b'$')
            return [gppgl for gppgl in data if gppgl.startswith(b'GPGLL')][0]
    return None

def readData(line) -> tuple:
    '''
    Read the data from the line buffer and return the latitude and longitude values
    '''
    gppgl = findGPGLL(line)
    if gppgl is not None:
        data = gppgl.decode('utf-8')
        return getLanAndLon(data)
    return [None, None]

while True:
    if uart.any():
      buffer += uart.readline()
      if buffer is not None:
        [lat,lon] = readData(buffer)
        if lat and lon:
            buffer = b''
    if len(buffer) > 100:
        buffer = b''
    utime.sleep_ms(100)