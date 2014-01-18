'''
Created on 27 nov. 2013

@author: Dennis
'''

ONE_SIXTH = 1.0 / 6.0

# Commented the entire function, since it should be manually inlined
'''
def rgb_to_luminance(r, g, b):
    """
    Computes only the luminance from RGB.
    
    Faster than colorsys.rgb_to_hls since it skips computations for Hue and Saturation.
    Useful for cases where only the luminance is required.
    """
    
    maxc = max(r, g, b)
    minc = min(r, g, b)

    return (minc+maxc)/2.0


    ROEL! Do you see all of this commented code down here? You were wasting processing time on all
    that crap even though you only used the luminance! Do I get a cookie now? :D
    
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = (maxc-minc) / (maxc+minc)
    else:
        s = (maxc-minc) / (2.0-maxc-minc)
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, l, s
'''

def rgb_to_hue(r, g, b):
    """
    Computes only hue from RGB.
    
    Faster than colorsys.rgb_to_hsv since it skips computations for Saturation and Value.
    Also slightly optimized computation of hue itself
    
    Useful for cases where only the Hue is required.
    """
    maxc = max(r, g, b)
    minc = min(r, g, b)

    if minc == maxc:
        return 0.0
    
    # previous implementation computed gc, bc and rc ahead of time.
    # since only 2 of the 3 values are used depending on conditions in
    # the if/elif/else, I moved the 2 used values into the if-blocks
    
    ONE_OVER_MAX_MINUS_MIN = 1.0 / (maxc - minc)
    
    if r == maxc:
        gc = (maxc-g) * ONE_OVER_MAX_MINUS_MIN
        bc = (maxc-b) * ONE_OVER_MAX_MINUS_MIN
        
        h = bc-gc
    elif g == maxc:
        rc = (maxc-r) * ONE_OVER_MAX_MINUS_MIN
        bc = (maxc-b) * ONE_OVER_MAX_MINUS_MIN
        
        h = 2.0+rc-bc
    else:
        rc = (maxc-r) * ONE_OVER_MAX_MINUS_MIN
        gc = (maxc-g) * ONE_OVER_MAX_MINUS_MIN
        
        h = 4.0+gc-rc
        
    return (h * ONE_SIXTH) % 1.0        # mult by 1/6 instead of dividing by 6