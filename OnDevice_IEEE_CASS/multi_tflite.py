import numpy as np
import tflite_runtime.interpreter as tflite
import platform

class multi_tflite:
	def __init__(self,ellipse_model,point_model):
		self.interpreter1 = tflite.Interpreter(ellipse_model,
  experimental_delegates=[tflite.load_delegate('libedgetpu.so.1', {"device": "usb:0"})])
		self.interpreter2 = tflite.Interpreter(point_model,
  experimental_delegates=[tflite.load_delegate('libedgetpu.so.1', {"device": "usb:1"})])
		self.interpreter1.allocate_tensors()
		self.interpreter2.allocate_tensors()
		self.input1 = self.interpreter1.get_input_details()
		self.output1 = self.interpreter1.get_output_details()
		self.input2 = self.interpreter2.get_input_details()
		self.output2 = self.interpreter2.get_output_details()

	def predict_img(self,frame):
		frame = frame.astype('float32')/255.0
		frame = np.expand_dims(frame,axis=0)
		self.interpreter1.set_tensor(self.input1[0]['index'],frame)
		self.interpreter1.invoke()
		output_data = self.interpreter1.get_tensor(self.output1[0]['index'])
		output_data = np.squeeze(output_data)
		output_data = np.reshape(output_data,(224,224,1))*255.0
		output_data = output_data.astype('uint8')
		return output_data
	def predict_point(self,input_arr):
		input_arr = input_arr.reshape((1,1,10))
		input_arr = input_arr.astype('float32')
		self.interpreter2.set_tensor(self.input2[0]['index'],input_arr)
		self.interpreter2.invoke()
		output_arr = self.interpreter2.get_tensor(self.output2[0]['index'])
		return output_arr
