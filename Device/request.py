import requests
import zipfile
import os
from io  import BytesIO
import configparser
import base64
import subprocess
import psutil
import time

config_file = 'device.conf'
save_path   = '/home/pjrios/display/images'
os.makedirs(save_path, exist_ok=True)

# We read device.conf 
config      = configparser.ConfigParser()
config.read(config_file)
freq = config.getfloat('main','freq')*60*60
device_id = config.getint('main','device_id')
geo_id = config.getint('main','geoid')
url       = f"https://2e2e-208-116-169-88.ngrok-free.app/images/{device_id}?geoid={geo_id}"

done = 0
while(done!=2):
	response = requests.get(url)
	#print(response.status_code)
	
	if response.status_code == 200: 
		json_data = response.json()
		geoid = json_data['geoid']
		zip_b64 = json_data['images_zip']
		
		#print(freq)
		
		zip_data = BytesIO(base64.b64decode(zip_b64))
		
		with zipfile.ZipFile(zip_data,'r') as zf:
			zf.extractall(save_path)
			#print("Saved!!")
				
		num_images = len(os.listdir(save_path))
		
		config.set('main','geoid', str(geoid))
		config.set('main','status','ready')
		with open(config_file,'w') as conf:
			config.write(conf)
		intervals = freq//num_images
		#print(num_images)
		subprocess.run(['pkill','-9','fbi'],check=False)
		fbi_cmd = f"sudo fbi -a -t {int(intervals)} -T 1 -noverbose {os.path.join(save_path,'*')}"
		#print(fbi_cmd)
		subprocess.run(fbi_cmd,shell=True)
		done = 2
	else:
		done += 1
		running = False
		for process in psutil.process_iter():
			if process.name() =="fbi":
				running= True
				break
		if not running:
			fbi_cmd = f"sudo fbi -a -t {freq} -T 1 -noverbose {os.path.join(save_path,'/home/pjrios/display/starting image/welcome.jpg')}"
			print("start fbi")
		subprocess.run(fbi_cmd,shell=True)
		print("done: ",done)
		print('Request failed')
		time.sleep(10)
