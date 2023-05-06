from flask import Flask, request, send_file
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import zipfile
from io import BytesIO
import base64


app = Flask(__name__)

from sqlalchemy import create_engine, URL

url_object = URL.create(
    "mysql+pymysql",
    username="user",
    password="password",
    host="localhost",
    database="db_name",
)

engine = create_engine(url_object)

Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define a class that maps to the USERDATA table in the database
class Userdata(Base):
    __tablename__ = 'table_name'

    DEVICEID = Column(Integer, primary_key=True)
    geoid = Column(String(255))

def get_images_from_directory(folder_path):
    # Create a ZIP archive in memory containing all images in the folder
    zip_data = BytesIO()
    with zipfile.ZipFile(zip_data, 'w') as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    zf.write(file_path, file)

    # Prepare ZIP archive for sending
    zip_data.seek(0)
    zip_b64 = base64.b64encode(zip_data.getvalue()).decode('utf-8')
    return zip_b64


@app.route('/images/<int:id>')
def get_images(id):
    print(f"Received request for ID {id}")
    
    geoid = request.args.get('geoid')
    print(geoid)
    if geoid != '-1':
        folder_path = f'C:\\path\\to\\images\\dir\\{geoid}'
        print(f"Retrieving images from {folder_path}")
        images_zip = get_images_from_directory(folder_path)
        return {'geoid': geoid, 'images_zip': images_zip}

    # Query database for entry with specified ID
    session = Session()
    result = session.query(Userdata.geoid).filter_by(DEVICEID=id).first()
    if result is None:
        return 'ID not found', 404

    # Extract GEOID value and construct image folder path
    geoid = result[0]
    folder_path = f'C:\\path\\to\\images\\dir\\{geoid}'
    print(f"Retrieving images from {folder_path}")
    
    images_zip = get_images_from_directory(folder_path)
    return {'geoid': geoid, 'images_zip': images_zip}
    


if __name__ == '__main__':
    app.run(host='0.0.0.0')
