import numpy as np 
import matplotlib.pyplot as plt
from comtradeConfig import ComtradeConfig

## class to hold comtrade common functions

class Utilities:
    
    @staticmethod
    def generate_data_cfg():
            from datetime import datetime, timedelta
            date_and_time = datetime.now()
            date_and_time_string_start = date_and_time.strftime("%d/%m/%Y, %H:%M:%S.%f")
            date_and_time_end = date_and_time + timedelta(seconds=(1/ComtradeConfig.sampling_rate())*ComtradeConfig.sample_end(ComtradeConfig.sampling_rate(), ComtradeConfig.seconds()))
            date_and_time_string_end = date_and_time_end.strftime("%d/%m/%Y, %H:%M:%S.%f")
            
            voltage_peak = ComtradeConfig.voltage_peak()
            current_peak = ComtradeConfig.current_peak()


    def write_cfg_to_file(self,filename = "six_analog_signals_zero_digital" ):
        comtrade_cfg_data = self.generate_data_cfg()
        f_cfg = open(filename + ".cfg","w")
        for cfg_line in comtrade_cfg_data:
            f_cfg.write(cfg_line + "\n")

        f_cfg.close()

    ## function to compute and append data to dat file
    def write_dat_to_file(filename = "six_analog_signals_zero_digital"):
        f_dat = open(filename+".dat","w")
        
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

    def make_plot(xdata,ydata, xlabel, ylabel,legend):
        import mathplotlib.pypl
        plt.rcParams["figure.figsize"] = (15,8)
        plt.figure()
        plt.grid()
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        for y in ydata:
            plt.plot(xdata,y)
        plt.legend(legend)



    ## A method to compute the park voltage given voltage alpha and voltage beta
    #  This has been declared as a static method because it only requires it's input arguments to perfrom its function successfully
    #
    @staticmethod 
    def compute_v_park(v_alpha,v_beta):
        count = np.arange(0,len(v_alpha),1)
        park_series = []
        for i in count:
            park_series.append(np.sqrt((pow(v_alpha[i],2) + pow(v_beta[i],2)))/np.sqrt(3))

        return park_series 


    ## A function to read the instantaneous and rms triggered comtrade file
    #  This has been declared as a static method because it only requires it's input arguments to perfrom its function successfully
    @staticmethod
    def summarize_comtrade_files(filelocation_RMS,filelocation_inst):

        from comtrade import Comtrade
        import matplotlib.pyplot as plt

        comtradeObj = Comtrade()

        comtradeObj.load(filelocation_RMS + ".CFG", filelocation_RMS + ".DAT")

        import pandas as pd

        data_1 = {
            "timestamp": comtradeObj.time,
            "voltage_values_rms": comtradeObj.analog[1]
        }

        comtradeObj.load(filelocation_inst + ".CFG", filelocation_inst + ".DAT")

        data_2 = {
            "timestamp" : comtradeObj.time,
            "voltage_values_instantaneous": comtradeObj.analog[1]
        }
        return pd.DataFrame(data_1), pd.DataFrame(data_2)

    @staticmethod
    def synchronize_rms_and_inst(rms,inst):
        ## this function returns a list containing rms and inst dataframes synchronized
    
        trigger_rms = rms[rms.timestamp >=10]
        trigger_inst = inst[inst.timestamp >= 1]

        ## subtract the pretrigger value from time stamp
        trigger_rms.timestamp = trigger_rms.timestamp - 10
        trigger_inst.timestamp = trigger_inst.timestamp - 1
        
        return trigger_rms,trigger_inst

    @staticmethod
    def make_plot(xdata,ydata, xlabel, ylabel,legend):
        import matplotlib.pyplot as plt

        plt.rcParams["figure.figsize"] = (15,8)
        plt.figure()
        plt.grid()

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        for y in ydata:
            plt.plot(xdata,y)
        plt.legend(legend)


    @staticmethod
    def modulating_index_voltage(mod_index_voltage = 0.2):
        return mod_index_voltage

    @staticmethod
    def modulating_index_current(mod_index_current = 0):
        return mod_index_current

    @staticmethod
    def modulating_frequency(mod_frequency = 4):
        return mod_frequency

    @staticmethod
    def phase_of_modulating_frequency(phase_of_modu_freq = 0):
        return phase_of_modu_freq

    @staticmethod
    def phase_of_voltage_modulant(phase_of_voltage_mod = 0):
        return phase_of_voltage_mod

    @staticmethod
    def phase_of_current_modulant(phase_of_current_mod = 180):
        return phase_of_current_mod

    @staticmethod
    def oneTwentyDegrees(degree = 120):
        return degree

    