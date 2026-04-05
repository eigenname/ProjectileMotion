import numpy as np

def get_rounding_from_speed(value): # Determine the number of decimal places based on initial speed arg
    if value == 0:
        return 0
    return max(0, -np.floor(np.log10(abs(value))))

