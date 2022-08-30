## Revision 3
## This is a script to generate a comtrade file in ascii format with voltage and current modulations

## Goals 
## 1- All configs should be in a variable with key value pairs
## 2- Create modular functions which perform specific functions

import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.fft import fft, fftfreq

## define class Configuration to hold all comtrade specification

class ComtradeConfig:
    ## set the year default is 2001
    def year(year = 2001):
        year = int(year)
        if (year != 2001 and year != 1999 and year != 1991):
            raise Exception("Comtrade rev_year is not valid")
        return year

    ## function to set the frequency (default is 50Hz) floating point values are allowed
    def frequency (frequency = 50):
        try: 
            frequency = float(frequency)
        except:
            print("frequency should be a number in hertz")
        return frequency
    
    ## set the length of the data stream which will determine samp
    def seconds (seconds = 300):
        try: 
            seconds = float(seconds)
        except:
            print("seconds should be a number in hertz")
        return seconds
    

    ## sampling rate is set to xKhz
    def sampling_rate (sampling_rate = 2000):
        if(isinstance(sampling_rate,int) == False):
           raise Exception("sampling rate must be an integer")
        if (sampling_rate > 8000 or sampling_rate < 1000):
            raise Exception("sampling rate needs to be between 1000Hz and 8000Hz")
            
        return sampling_rate
    
    def sample_end(sampling_rate,seconds):
        ## number of samples for n seconds at x sampling rate
        
        return sampling_rate * seconds
    
    def voltage_peak(peak = 100):
        
        if(peak > 120 or peak < 0):
            raise Exception("voltage must be between range of 0 and 120v")
            
        return peak
    
    def current_peak(peak = 1):
        
        if(peak > 1.2 or peak < 0):
            raise Exception("cuurent must be between range of 0 and 1.2A")
            
        return peak
    
    ## set the maximum data value to 1000 which should be within the range of 0 to 32767 (Note that 0 to -32767 and 0 to +32767 are the limits for the data repesented in the data file)
    maximum_data_value_voltage = 1000
    channel_multiplier_voltage = voltage_peak()/maximum_data_value_voltage

    ## compute the current multiplier
    maximum_data_value_current = 100
    channel_multiplier_current = current_peak()/maximum_data_value_current
    
    
def generate_data_cfg():
    from datetime import datetime, timedelta
    date_and_time = datetime.now()
    date_and_time_string_start = date_and_time.strftime("%d/%m/%Y, %H:%M:%S.%f")
    date_and_time_end = date_and_time + timedelta(seconds=(1/ComtradeConfig.sampling_rate())*ComtradeConfig.sample_end(ComtradeConfig.sampling_rate(), ComtradeConfig.seconds()))
    date_and_time_string_end = date_and_time_end.strftime("%d/%m/%Y, %H:%M:%S.%f")
    
    voltage_peak = ComtradeConfig.voltage_peak()
    current_peak = ComtradeConfig.current_peak()
    


    ## construct the data for config file
    comtrade_cfg_data = []

    comtrade_cfg_data.append(",," + str(ComtradeConfig.year()))
    comtrade_cfg_data.append("6,6A,0D")
    comtrade_cfg_data.append("1,v1,a,,V," + str(ComtradeConfig.channel_multiplier_voltage) + ",0,0,-32767,32767,1,1,s")
    comtrade_cfg_data.append("2,v2,b,,V," + str(ComtradeConfig.channel_multiplier_voltage) + ",0,0,-32767,32767,1,1,s")
    comtrade_cfg_data.append("3,v3,c,,V," + str(ComtradeConfig.channel_multiplier_voltage) + ",0,0,-32767,32767,1,1,s")
    comtrade_cfg_data.append("4,iq,a,,A," + str(ComtradeConfig.channel_multiplier_current) + ",0,0,-32767,32767,1,1,s")
    comtrade_cfg_data.append("5,iq,b,,A," + str(ComtradeConfig.channel_multiplier_current) + ",0,0,-32767,32767,1,1,s")
    comtrade_cfg_data.append("6,iq,c,,A," + str(ComtradeConfig.channel_multiplier_current) + ",0,0,-32767,32767,1,1,s")
    comtrade_cfg_data.append(str(ComtradeConfig.frequency))
    comtrade_cfg_data.append("1")
    comtrade_cfg_data.append(str(ComtradeConfig.sampling_rate()) + "," + str(ComtradeConfig.sample_end(ComtradeConfig.sampling_rate(), ComtradeConfig.seconds())))
    comtrade_cfg_data.append(date_and_time_string_start)
    comtrade_cfg_data.append(date_and_time_string_end)
    comtrade_cfg_data.append("ASCII")
    comtrade_cfg_data.append("1")
    
    return comtrade_cfg_data

def write_cfg_to_file():
    comtrade_cfg_data = generate_data_cfg()
    f_cfg = open("six_analog_signals_zero_digital.cfg","w")
    for cfg_line in comtrade_cfg_data:
        f_cfg.write(cfg_line + "\n")

    f_cfg.close()


## define the signal peaks
    

write_cfg_to_file()

def generate_signal(t,peak,base_frequency,phase_base, modulating_index,modulating_frequency, modulant_phase):
    signal = []
    for t_inst in t:
        signal.append(peak*math.cos( 2*math.pi*base_frequency*t_inst + (phase_base*(math.pi/180)) ) * ( 1+modulating_index_voltage*math.cos(2*math.pi*modulating_frequency*t_inst + (modulant_phase*(math.pi/180)) )))
    
    return signal

## generate data for dat file

fs = ComtradeConfig.sampling_rate()
T = 1/fs

t = np.arange(0,ComtradeConfig.seconds(),T)

modulating_index = 0
modulating_frequency = 12


##generate_signal(t,ComtradeConfig.voltage_peak(100.5),ComtradeConfig.frequency(),0,modulating_index,modulating_frequency,)

## variables to hold 3 voltages
samples_va = []
samples_vb = []
samples_vc = []

## variables to hold 3 currents
samples_ia = []
samples_ib = []
samples_ic = []

voltage_peak = ComtradeConfig.voltage_peak()
current_peak = ComtradeConfig.current_peak()
base_frequency = ComtradeConfig.frequency()

## define the phases of va, vb and vc
phase_of_base_va = 0
phase_of_base_vb = phase_of_base_va - 120
phase_of_base_vc = phase_of_base_va + 120

## phase difference between v(i) and i(i) where i represents the a,b or c
lag = -30  


## define the phases of ia,ib and ic
phase_of_base_ia = phase_of_base_va + lag
phase_of_base_ib = phase_of_base_vb + lag
phase_of_base_ic = phase_of_base_vc + lag

## define variables to hold voltage and current alpha and beta components
samples_v_alpha = []
samples_v_beta  = []
samples_v_gamma = []

samples_i_alpha = []
samples_i_beta  = []
samples_i_gamma = []

##  define variables to hold P_park and Q_park
samples_P_park = []
samples_Q_park = []

## Defining Modulation index 
modulating_index_voltage = 0
modulating_index_current = 0

## modulating Frequency
modulating_frequency = 40
phase_of_modulating_frequency = 0


phase_of_voltage_modulant = 0
phase_of_current_modulant = 180

three_phase_frequency_shift = 120


for t_inst in t:
    # Generate values for all voltages
    va_inst = voltage_peak*math.cos( 2*math.pi*base_frequency*t_inst + (phase_of_base_va*(math.pi/180)) ) * ( 1+modulating_index_voltage*math.cos(2*math.pi*modulating_frequency*t_inst + (phase_of_voltage_modulant*(math.pi/180)) ))
    vb_inst = voltage_peak*math.cos( 2*math.pi*base_frequency*t_inst + (phase_of_base_vb*(math.pi/180)) ) * ( 1+modulating_index_voltage*math.cos(2*math.pi*modulating_frequency*t_inst + (phase_of_voltage_modulant*(math.pi/180)) ))
    vc_inst = voltage_peak*math.cos( 2*math.pi*base_frequency*t_inst + (phase_of_base_vc*(math.pi/180)) ) * ( 1+modulating_index_voltage*math.cos(2*math.pi*modulating_frequency*t_inst + (phase_of_voltage_modulant*(math.pi/180)) ))
    
    samples_va.append(va_inst)
    samples_vb.append(vb_inst)
    samples_vc.append(vc_inst)
    
    v_alpha = (np.sqrt(2/3)) * ( (1 * va_inst) + ((-1/2) * vb_inst) + ((-1/2) * vc_inst) )
    v_beta  = (np.sqrt(2/3)) * ( (0 * va_inst) + (((np.sqrt(3))/2) * vb_inst) + ((-(np.sqrt(3))/2) * vc_inst) )
    v_gamma = (np.sqrt(2/3)) * ( ((1/(np.sqrt(2))) * va_inst) + ((1/(np.sqrt(2))) * vb_inst + ((1/(np.sqrt(2))) * vc_inst)) )
    
    samples_v_alpha.append(v_alpha)
    samples_v_beta.append(v_beta)
    samples_v_gamma.append(v_gamma)
    
    # Generate values for all currents
    ia_inst = current_peak*math.cos(2*math.pi*base_frequency*t_inst + (phase_of_base_ia*(math.pi/180))) * (1+modulating_index_current*math.cos(2*math.pi*modulating_frequency*t_inst + (phase_of_current_modulant*(math.pi/180)) ))
    ib_inst = current_peak*math.cos(2*math.pi*base_frequency*t_inst + (phase_of_base_ib*(math.pi/180))) * (1+modulating_index_current*math.cos(2*math.pi*modulating_frequency*t_inst + (phase_of_current_modulant*(math.pi/180)) ))
    ic_inst = current_peak*math.cos(2*math.pi*base_frequency*t_inst + (phase_of_base_ic*(math.pi/180))) * (1+modulating_index_current*math.cos(2*math.pi*modulating_frequency*t_inst + (phase_of_current_modulant*(math.pi/180)) ))
    
    
    samples_ia.append(ia_inst)
    samples_ib.append(ib_inst)
    samples_ic.append(ic_inst)

    i_alpha = (np.sqrt(2/3)) * ( (1 * ia_inst) + ((-1/2) * ib_inst) + ((-1/2) * ic_inst) )
    i_beta  = (np.sqrt(2/3)) * ( (0 * ia_inst) + (((np.sqrt(3))/2) * ib_inst) + ((-(np.sqrt(3))/2) * ic_inst) )
    i_gamma = (np.sqrt(2/3)) * ( ((1/(np.sqrt(2))) * ia_inst) + ((1/(np.sqrt(2))) * ib_inst + ((1/(np.sqrt(2))) * ic_inst)) )

    samples_i_alpha.append(i_alpha)
    samples_i_beta.append(i_beta)
    samples_i_gamma.append(i_gamma)
    
    ## compute and append the p_park and q_park values
    
    p_park_inst = (v_alpha * i_alpha) + (v_beta* i_beta)
    q_park_inst = (v_beta * i_alpha) - (v_alpha * i_beta)
    
    samples_P_park.append(p_park_inst)
    samples_Q_park.append(q_park_inst)

    
## function to compute and append data to dat file
def write_dat_to_file():
    f_dat = open("six_analog_signals_zero_digital.dat","w")
    
    index = np.arange(0,int(ComtradeConfig.seconds()*fs),1)
    mega = 1000000
    for i in index:
        ## note that rounding of samples_va which is a voltage value to int is an approximation at the thousandths place for a 100 volt sensed signal
        
        f_dat.write(str(i+1) + 
                    "," + str(round(t[i]*mega)) + 
                    "," + str(round(samples_va[i]/float(ComtradeConfig.channel_multiplier_voltage))) + 
                    "," + str(round(samples_vb[i]/float(ComtradeConfig.channel_multiplier_voltage))) + 
                    "," + str(round(samples_vc[i]/float(ComtradeConfig.channel_multiplier_voltage))) + 
                    "," + str(round(samples_ia[i]/float(ComtradeConfig.channel_multiplier_current))) +
                    "," + str(round(samples_ib[i]/float(ComtradeConfig.channel_multiplier_current))) + 
                    "," + str(round(samples_ic[i]/float(ComtradeConfig.channel_multiplier_current))) + "\n")
        
    f_dat.close()
    
write_dat_to_file()

def make_plot(xdata,ydata, xlabel, ylabel,legend):
    plt.rcParams["figure.figsize"] = (15,8)
    plt.figure()
    plt.grid()
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    for y in ydata:
        plt.plot(xdata,y)
    plt.legend(legend)

make_plot(t[1:600],[samples_va[1:600],samples_vb[1:600],samples_vc[1:600]],"seconds","voltage",["phase A","phase B","phase C"])
make_plot(t[1:600],[samples_ia[1:600],samples_ib[1:600],samples_ic[1:600]],"seconds","current",["phase A","phase B","phase C"])
make_plot(t[1:600],[samples_v_alpha[1:600],samples_v_beta[1:600],samples_v_gamma[1:600]],"seconds","voltage",["V Alpha","V Beta","V Gamma"])
make_plot(t[1:600],[samples_i_alpha[1:600],samples_i_beta[1:600],samples_i_gamma[1:600]],"seconds","voltage",["i Alpha","i Beta","i Gamma"])
make_plot(t[1:600],[samples_P_park[1:600],samples_Q_park[1:600]],"seconds","power",["P Park","Q Park"])