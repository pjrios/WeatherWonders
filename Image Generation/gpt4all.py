from diffusers import StableDiffusionPipeline
from pygpt4all import GPT4All_J
from datetime import timezone
from datetime import timezone
from datetime import time
import geopandas as gpd
import mysql.connector
import requests
import datetime
import pickle
import torch
import os

#-----------------------------------------------------------------------
# areas geojson. we use to create a dictionary
geojsonfile = "division.geojson"
save_dir    = "C:\\path\\to\\save\\dir"
# filename to save the dictionary
filename = 'geoid_dict.pkl'

# Check if the dictionary file exists
if os.path.exists(filename):
    # Load the dictionary from the file
    with open(filename, 'rb') as f:
        geoid_dict = pickle.load(f)
else:
    gdf = gpd.read_file(geojsonfile)

    # Create a dictionary for each GEOID in the form of GEOID, (latitude, longitude)
    geoid_dict = {}
    for index, row in gdf.iterrows():
      geoid = row['GEOID'].strip('0')
      latitude = row['geometry'].centroid.y
      longitude = row['geometry'].centroid.x
      geoid_dict[geoid] = (latitude, longitude)

    # Print out the dictionary
    #print(geoid_dict)
    # Save the dictionary to the file
    with open(filename, 'wb') as f:
        pickle.dump(geoid_dict, f)
        
# Connect to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Mjy2892z@@",
  database="STOPICS"
)

# Create a cursor object to interact with the database
mycursor = mydb.cursor()

# Execute a query to select all the non-repeated GEOIDs from the user data table
mycursor.execute("SELECT DISTINCT GEOID FROM USERDATA")

# Fetch all the results and print them out
results = mycursor.fetchall()

locations = []
#print(results)

for row in results:
  locations.append(row[0])
#print(locations)
# Close the database connection
mydb.close()



# Make API call
api_key = 'your-api-key'
for location in locations:
    latitude =  geoid_dict[str(location)][0] #36.082157
    longitude = geoid_dict[str(location)][1] #-94.171852
    print(latitude,longitude)

    location = "Fayetteville"
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&exclude=minutely,hourly,daily,alerts&appid={api_key}'
    response = requests.get(url)
    #------------------------------------------------

    # Get the current time 
    current_time = datetime.datetime.now().time()

    # Parse JSON response
    data = response.json()
    
    weather = data["weather"][0]["main"]
    # Determine time of day
    if current_time < time(12):
        time_of_day = "morning"
    elif time(12) <= current_time < time(18):
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"

    prompt = f"Imagine a large format, fine art painting that is both a beautiful landscape and a masterpiece, inspired by the current weather, which is {weather}, in the {time_of_day}. Write a two sentence description of a day given the previews information. only return the paragraph"
    #print(prompt)

    text = ""

    #load model
    model = GPT4All_J("C:\\path\\to\\GPT4All\\model\\ggml-gpt4all-j-v1.3-groovy.bin")

    #generate 
    for token in model.generate(prompt):
        text = text + token

    #print(text)
    
    diff_model = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(diff_model, torch_dtype=torch.float16)  
    pipe = pipe.to("cuda")#change to cpu if you dont have a gpu

    image = pipe(prompt, height=720, width= 960).images[0]  # image here is in [PIL format](https://pillow.readthedocs.io/en/stable/)

    # Now to display an image you can either save it such as:
    image.save(f"{save_dir}\\{location}\\weather.png")
    #image
