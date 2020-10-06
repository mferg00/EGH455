import time
from enviroplus import gas 
from ltr559 import LTR559
from bme280 import BME280
from enviroplus.noise import Noise
from subprocess import PIPE, Popen
import numpy as np
import mysql.connector
from mysql.connector import Error

insert_query = """INSERT INTO UAVSensors  (Time, Pressure, Humidity, Light, Temperature, Noise_1, Noise_2, Noise_3, Ox_Threshold, Red_Threshold, Nh3_Threshold, Ox, Red, Nh3) 
								VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s) """


connection = mysql.connector.connect(host='172.20.10.2',
													database='sensors',
													user='mysql',
													password='mysql')


def get_cpu_temperature():
	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
	output, _error = process.communicate()
	return float(output[output.index('=') + 1:output.rindex("'")])

noise = Noise()
bme280=BME280()
ltr559=LTR559()

def get_noise():
	amps = noise.get_amplitudes_at_frequency_ranges([
		(20, 3350),
		(3350, 6680),
		(6680,10010),
#	(10010, 13340),
#        (13340,16670),
#        (16670,20000)
	])
	amps = [n * 32 for n in amps]
	amps=np.log10(amps)
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

def get_gases():
	readings=gas.read_all()
	oxidised=round(readings.oxidising, 2)
	reduced=round(gas.read_reducing(),2)
	nh3=round(readings.nh3,2)
	gases=[oxidised,reduced,nh3]
	return gases

start_time = time.time()

gases_threshold=get_gases()

print("The sensors are calibrating, please wait two minutes.")

file1=open("all_readings.txt","w")
file1.seek(0)
file1.truncate()


try:
	while True:

		elapsed_time = time.time() - start_time
		
		if elapsed_time<20:
			gases_threshold=get_gases()
			pressure_calibration=bme280.get_pressure()
			humidity_calibration=bme280.get_humidity()
			light_calibration=ltr559.get_lux()
			temperature_calibration= get_temperature()
			noise_lvl_calibration=get_noise()
		

		elif elapsed_time>20:

			run_time=elapsed_time -20
			
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

			gases=get_gases()

			try:
				if connection.is_connected():
					cursor = connection.cursor()
					noise_1, noise_2, noise_3 = noise_lvl
					ox_thresh, red_thresh, nh3_thresh = gases_threshold
					ox, red, nh3 = gases
					sensor_data = [float(run_time),float(pressure),float(humidity),float(light),float(temperature),float(noise_1),float(noise_2),float(noise_3),float(ox_thresh),float(red_thresh), float(nh3_thresh),float(ox), float(red), float(nh3)]
					print("Sensor data")
					print(sensor_data)
					recordTuple = tuple(sensor_data)
					cursor.execute(insert_query, recordTuple)
					connection.commit()
			except Error as e:
				print("Error while connecting to MySQL", e)

			if gases[0]>gases_threshold[0]:
				print("OX current value: ",gases[0]," OX threshold: ",gases_threshold[0], " OX concentration is increasing")
			elif gases[0]<gases_threshold[0]:
				print("OX current value: ",gases[0]," OX threshold: ",gases_threshold[0], " OX concentration is reducing")
			else:
				print("OX current value: ",gases[0]," OX threshold: ",gases_threshold[0], " OX concentration is the same as threshold")

			if gases[1]>gases_threshold[1]:
				print("RED current value: ",gases[1]," RED threshold: ",gases_threshold[1], " RED concentration is reducing")
			elif gases[1]<gases_threshold[1]:
				print("RED current value: ",gases[1]," RED threshold: ",gases_threshold[1], " RED concentration is increasing")
			else:
				print("RED current value: ",gases[1]," RED threshold: ",gases_threshold[1], " RED concentration is the same as threshold")

			if gases[2]>gases_threshold[2]:
				print("NH3 current value: ",gases[2]," NH3 threshold: ",gases_threshold[2], " NH3 concentration is reducing")
			elif gases[2]<gases_threshold[2]:
				print("NH3 current value: ",gases[2]," NH3 threshold: ",gases_threshold[2], " NH3 concentration is increasing")
			else:
				print("NH3 current value: ",gases[2]," NH3 threshold: ",gases_threshold[2], " NH3 concentration is the same")

			time.sleep(5)
			
except KeyboardInterrupt:
	file1.close()
	pass
