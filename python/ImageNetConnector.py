import jetson.inference
import jetson.utils

class ImageNetConnector:

    def __init__(self):
        print("init")

    def RunInference(self,img,net):
        """
            Run ImageNet Inference

            :param img: image to be classified
	    :param net: network for classification

            :return class_desc: object detected
            :return confidence: classification confidence
	    :return class_idx: class id 
        """

        # classify the image
        class_idx, confidence = net.Classify(img)

        # find the object description
        class_desc = net.GetClassDesc(class_idx)

        return class_desc, confidence, class_idx
