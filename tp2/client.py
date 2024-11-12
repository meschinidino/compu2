# client.py
import requests

# Send the image to the async server for processing
response = requests.post('http://127.0.0.1:8080/process', files={'image': open('/home/dino/PycharmProjects/compu2/tp2/fallout.jpeg', 'rb')})
task_id = response.json()['task_id']

# Check the status of the task
status_response = requests.get(f'http://127.0.0.1:8080/status/{task_id}')
while status_response.json()['status'] == 'processing':
    status_response = requests.get(f'http://127.0.0.1:8080/status/{task_id}')

# Save the processed image to a file
if status_response.status_code == 200:
    with open('output_image.jpg', 'wb') as f:
        f.write(status_response.content)
    print("Processed image saved as output_image.jpg")
else:
    print("Failed to retrieve the processed image")