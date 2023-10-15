import pickle as pkl
import joblib as jl
model = jl.load("./model_weights_jlib_2.pkl")

# 10 flattened samples for one data point
# sample_data = [[-9.38,  4.39,  0.12, -9.34,  4.39,  0.2 , -9.45,  4.35,  0.12,
#         -9.38,  4.47,  0.16, -9.38,  4.43,  0.2 , -9.38,  4.39,  0.2 ,
#         -9.34,  4.43,  0.2 , -9.34,  4.43,  0.16, -9.34,  4.39,  0.24,
#         -9.41,  4.39,  0.12]]

# preds = model.predict(sample_data)
# print(preds)
def detect_chewing(acceleration_data):
    answer = model.predict(acceleration_data)
    return answer[0]