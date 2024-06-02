########################################################################################################################
# CALCULATE SMA # CALCULATE SMA # CALCULATE SMA # CALCULATE SMA # CALCULATE SMA # CALCULATE SMA # CALCULATE SMA # CALCUL
########################################################################################################################

# function: calculating Smooth Moving Average
def calculate_SMA(data):
    sma = sum(data) / len(data)
    return sma


########################################################################################################################
# CALCULATE VARIANCE # CALCULATE VARIANCE # CALCULATE VARIANCE # CALCULATE VARIANCE # CALCULATE VARIANCE # CALCULATE VAR
########################################################################################################################

# function: calculating Smooth Moving Average
def calculate_VAR(data):
    n = len(data)
    sma = calculate_SMA(data)
    variance = sum([(x - sma) ** 2 for x in data]) / (n - 1)
    return variance


########################################################################################################################
# CALCULATE SD # CALCULATE SD # CALCULATE SD # CALCULATE SD # CALCULATE SD # CALCULATE SD # CALCULATE SD # CALCULATE SD
########################################################################################################################

# function: calculating first Standard Deviation
def calculate_SD(data):
    sma = calculate_SMA(data)
    variance = calculate_VAR(data)
    sd = variance ** 0.5
    return sd


########################################################################################################################
# CALCULATE SDS # CALCULATE SDS # CALCULATE SDS # CALCULATE SDS # CALCULATE SDS # CALCULATE SDS # CALCULATE SDS # CALCUL
########################################################################################################################

# function: calculating Standard Deviation (positive and negative value)
def calculate_SDs(data, amount):
    sma = calculate_SMA(data)
    variance = calculate_VAR(data)
    sd = (variance ** 0.5) * amount
    sd_pos = sma + sd
    sd_neg = sma - sd
    return sd_pos, sd_neg


########################################################################################################################
# CALCULATE SDS FAST # CALCULATE SDS FAST # CALCULATE SDS FAST # CALCULATE SDS FAST # CALCULATE SDS FAST # CALCULATE SDS
########################################################################################################################

# function: calculating Standard Deviation (positive and negative value)
def calculate_SDs_fast(data, sma, n, amount):
    variance = sum([(x - sma) ** 2 for x in data]) / (n - 1)
    sd = (variance ** 0.5) * amount
    sd_pos = sma + sd
    sd_neg = sma - sd
    return sd_pos, sd_neg


########################################################################################################################
# GET AMOUNT SD # GET AMOUNT SD # GET AMOUNT SD # GET AMOUNT SD # GET AMOUNT SD # GET AMOUNT SD # GET AMOUNT SD # GET AM
########################################################################################################################

# function: getting the amount of response values
def get_amount_SD(sma, sd, value):
    diff = value - sma
    amount = diff / sd
    return amount


########################################################################################################################
# GET SD FROM SD # GET SD FROM SD # GET SD FROM SD # GET SD FROM SD # GET SD FROM SD # GET SD FROM SD # GET SD FROM SD #
########################################################################################################################

# function: getting Standard Deviation from another one
def get_SD_from_SD(sma, sd_before, amount_before, amount_after):
    sd = sd_before - sma
    sd_after = sma + sd * (amount_after / amount_before)
    return sd_after


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
