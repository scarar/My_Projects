import torch
print(torch.cuda.is_available())  # True if GPU is detected
print(torch.cuda.get_device_name(0))  # Prints your GPU name
