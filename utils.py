def is_within_tolerance(actual_angle: float, target_angle: float, tolerance: float = 0.05) -> bool:
    '''
    Checks if the given `actual_angle` and `target_angle` are within the range
    of `tolerance`
    '''
    diff = abs((target_angle - actual_angle + 180) % 360 - 180)
    return diff <= tolerance

def get_direction(actual_angle: float, target_angle: float) -> bool:
    '''
    Returns the direction to move based on `actual_angle` and `target_angle`.
    
    `True` means reverse (anti-clockwise), and `False` means `clockwise`
    '''
    diff = (target_angle - actual_angle + 360) % 360
    return not diff <= 180
