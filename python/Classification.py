import cv2
import asyncio
import websockets
import ast
import base64
import ImageNetConnector as imgNet
import json
import time
import jetson.inference
import jetson.utils


#initializing network
connector = imgNet.ImageNetConnector()
net = jetson.inference.imageNet("googlenet")



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
			class_desc, confidence, class_id = connector.RunInference(image,net)

			# sending class name, confidence, and classID back to client
			response = {"className":class_desc, "confidence":confidence, "classID": class_id}
			response = json.dumps(response)

			await websocket.send(response)


async def main ():
	async with websockets.serve(process, "0.0.0.0", 4040):
		await asyncio.Future()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

