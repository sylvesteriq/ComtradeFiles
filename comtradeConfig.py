
## define class Configuration to hold all comtrade specification

class ComtradeConfig:
    ## set the year default is 2001
    def year(year = 2022):
        return year

    ## function to set the frequency (default is 50Hz) floating point values are allowed
    def frequency (frequency = 50):
        return frequency
    
    ## set the length of the data stream which will determine samp
    def seconds (seconds = 300):
        return seconds
    

    ## sampling rate is set to xKhz
    def sampling_rate (sampling_rate = 2000):    
        return sampling_rate
    
    def sample_end(sampling_rate,seconds):
        ## number of samples for n seconds at x sampling rate
        return sampling_rate * seconds
    
    def voltage_peak(peak = 50):
        return peak
    
    def current_peak(peak = 1):
        return peak
    

    ## set the maximum data value to 1000 which should be within the range of 0 to 32767 (Note that 0 to -32767 and 0 to +32767 are the limits for the data repesented in the data file)
    maximum_data_value_voltage = 1000
    channel_multiplier_voltage = voltage_peak()/maximum_data_value_voltage

    ## compute the current multiplier
    maximum_data_value_current = 100
    channel_multiplier_current = current_peak()/maximum_data_value_current

    ## A method to return the first modulating frequency
    @staticmethod
    def modulating_frequency(mod_freq = 4):
        return mod_freq

    @staticmethod
    def phase_of_modulating_frequency(phase_of_mod_frequency = 0):
        return phase_of_mod_frequency


    @staticmethod
    def phase_of_voltage_modulant(phase_of_mod_voltage = 0):
        return phase_of_mod_voltage

    @staticmethod
    def phase_of_current_modulant(phase_of_mod_current = 180):
        return phase_of_mod_current

    @staticmethod
    def oneTwentyDegrees(oneTwentyDegrees = 120):
        return oneTwentyDegrees

    ## Defining Modulation index for voltage
    @staticmethod
    def modulating_index_voltage(mod_index_voltage = 0.2):
        return mod_index_voltage

    @staticmethod
    def modulating_index_current(mod_index_current = 0):
        return mod_index_current

    @staticmethod
    def method_to_test_within_class_call():
        Utilities.modulating_index
