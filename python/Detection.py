import cv2
import asyncio
import websockets
import ast
import base64
import DetectNetConnector as decNet
import json
import time
import jetson.inference
import jetson.utils


#initializing network
connector = decNet.DetectNetConnector()
net = jetson.inference.detectNet("ssd-mobilenet-v2")



async def process(websocket,path):

	while not websocket.closed:

		async for message in websocket:
			# splitting mime-type from base64
			_, img_encoded = message.split(',')

			img_decoded = base64.b64decode(img_encoded)
			file_name = 'myImage.jpg'


			with open (file_name , 'wb') as f:
				f.write(img_decoded)

			# loading image to CPU
			image = jetson.utils.loadImage('myImage.jpg')
			
			# running inference
			detections = connector.RunInference(image,net)

			# converting CUDA image to Numpy
			frame_2=jetson.utils.cudaToNumpy(image)

			# openCV uses BGR format
			converted_picture = cv2.cvtColor(frame_2, cv2.COLOR_RGB2BGR)

			# encoding Numpy image into base64
			retval, buffer = cv2.imencode('.jpg', converted_picture)
			jpg_as_text = base64.b64encode(buffer)
			
			# sending detections list and image back to client
			response = {"detections":detections, "image":str(jpg_as_text.decode('utf-8'))}
			response = json.dumps(response)
			

			await websocket.send(response) 


async def main ():
	async with websockets.serve(process, "0.0.0.0", 4040):
		await asyncio.Future()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

