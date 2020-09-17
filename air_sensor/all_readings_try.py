import time
from enviroplus import gas 
from ltr559 import LTR559
from bme280 import BME280
from enviroplus.noise import Noise
from subprocess import PIPE, Popen


def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

noise = Noise()
bme280=BME280()
ltr559=LTR559()

def get_noise():
    amps = noise.get_amplitudes_at_frequency_ranges([
        (100, 200),
        (500, 600),
        (1000, 1200)
    ])
    amps = [n * 32 for n in amps]
    return amps

factor = 2.25


def get_temperature():
    cpu_temp=get_cpu_temperature()
    cpu_temps = [get_cpu_temperature()]*5 
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    temperature = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
    return temperature

try:
    while True:

        readings=gas.read_all()
        oxidised=readings.oxidising
	print("oxidised=", oxidised )
        reduced=gas.read_reducing()
	print("reduced=", reduced)
        nh3=readings.nh3
	print("nh3=",nh3)
        
        pressure=bme280.get_pressure()
	print("pressure=", pressure)
        humidity=bme280.get_humidity()
	print("humidity=",humidity)
        light=ltr559.get_lux()
	print("light=",light)
        
        temperature= get_temperature()
	print("temperature=",temperature)

        noise_lvl=get_noise()
	print("The noise levels are:", noise_lvl)
	
	time.sleep(5)

except KeyboardInterrupt:
    pass
