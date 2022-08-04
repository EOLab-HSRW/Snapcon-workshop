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
#Assigning csi camera as input Source
camera = jetson.utils.videoSource("csi://0")  #"/dev/video0"


def reSizeImage():
	# Capture image from jetson camera (cuda Image)
	image =  camera.Capture()
            
        #Resizing the image for Snap (1270*720) --> (480*360)
	reSizedImage = jetson.utils.cudaAllocMapped(width = image.width * 0.375, height = image.height * 0.5, format = image.format)
	jetson.utils.cudaResize(image, reSizedImage)

	return reSizedImage

async def process(websocket,path):
	sendImage = False
	while not websocket.closed:
		sendFrame = False
		async for message in websocket:
			
			# deciding whether to send rendered image or not  
			if message == "sendImage":
				sendImage = True
				break
			if message == "notSendImage":
				sendImage = False					
				break
			# ask for image from jetson camera
			if message == "frame":
				sendFrame = True
				image = reSizeImage()
			else:
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
			if sendImage or sendFrame:
			
				response = {"detections":detections, "image":str(jpg_as_text.decode('utf-8'))}
			else:
				response = {"detections":detections}
			
			response = json.dumps(response)
			

			await websocket.send(response) 


async def main ():
	async with websockets.serve(process, "0.0.0.0", 4040, ping_interval = None):
		await asyncio.Future()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

