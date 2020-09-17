import time
from enviroplus import gas 
from ltr559 import LTR559
from  bme280  import  BME280
from enviroplus.noise import Noise
from subprocess import PIPE, Popen


def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

noise = Noise()

def get_noise():
    amps = noise.get_amplitudes_at_frequency_ranges([
        (100, 200),
        (500, 600),
        (1000, 1200)
    ])
    amps = [n * 32 for n in amps]

factor = 2.25

cpu_temps = [get_cpu_temperature()] * 5

def get_temperature():
    cpu_temp=get_cpu_temperature()
    cpu_temps = cpu_temps[1:] + [cpu_temp]
    avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
    raw_temp = bme280.get_temperature()
    temperature = raw_temp - ((avg_cpu_temp - raw_temp) / factor)

try:
    while True:

        readings=gas.read_all()
        oxidised=readings.oxidising
        reduced=gas.read_reducing()
        nh3=readings.nh3
        
        pressure=bme280.get_pressure()
        humidity=bme280.get_humidity()
        light=ltr559.get_lux()
        
        get_temperature()

        get_noise()

        variables=[temperature, pressure, light, humidity, oxidised, reduced, nh3 ]
        val_str=",".join(valriables)

        print(val_str,"\n")
        print(" The noise levels are:" ,amps, "\n")

except KeyboardInterrupt:
    sys.exit(0)