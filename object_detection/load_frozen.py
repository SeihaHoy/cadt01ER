import tensorflow as tf

class MyDectector:
    def __init__(self):
        print("[INFO] loading model...")
        PATH_TO_CKPT = r"models/frozen_inference_graph.pb"
        # download model from: https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API#run-network-in-opencv

        # Load the Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.compat.v1.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.compat.v1.import_graph_def(od_graph_def, name='')
            self.sess = tf.compat.v1.Session(graph=detection_graph)

        # Input tensor is the image
        self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        # Number of objects detected
        self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        # code source of tensorflow model loading: https://www.geeksforgeeks.org/ml-training-image-classifier-using-tensorflow-object-detection-api/

