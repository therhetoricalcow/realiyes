import numpy as np
import time
import tflite_runtime.interpreter as tflite
import platform

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': 'edgetpu.dll'
}[platform.system()]

class tflite_model:
    def __init__(self,model_file):
        self.interpreter = tflite.Interpreter(model_path=model_file,experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        print(self.input_details[0]['index'])
    def predict(self,frame):
        start_time = time.time()
        self.interpreter.set_tensor(self.input_details[0]['index'],frame)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        output_data = np.squeeze(output_data)
        stop_time = time.time()
        print("Time Taken to Make Prediction: " + str(stop_time-start_time) + " seconds")
        return output_data
