# -*- coding: utf-8 -*-
import sys, os, glob
import matplotlib.pyplot as plt
import numpy
import pandas
sys.path.append(r'C:\TestGit\scripts-test\Data_Processing\python-comtrade')
sys.path.append(r'C:\TestGit\Data_Processing\python-comtrade')
from comtrade import Comtrade
import datetime

rec = Comtrade()

#? User inputs
# Set time type: 1=seconds, 0=datetime format
time_type = 1
# Set output file name identifier (if desired)
out_id = ""

#? Code
# Define input comtrade folder
comtrade_folder = os.getcwd()
# Find all applicable comtrade files
comtrade_files = [f for f in glob.glob(r'{}\**\*.cfg'.format(comtrade_folder), recursive=True) if any(val in f for val in ['RMS','Monitor','Inst'])]
# Process comtrade files
for comtrade_file in comtrade_files:
	comtrade_base = os.path.splitext(comtrade_file)[0]
	csv_file = comtrade_base + out_id + '.csv'
	# Load comtrade data into memory
	rec.load('{}.cfg'.format(comtrade_base), '{}.dat'.format(comtrade_base))
	# The following code corrects for an issue with the monitor file not being read correctly. It also assume a sample rate of 1Hz.
	if "monitor" in str(comtrade_base).lower():
		time_data = [i * (len(rec.time) / rec.time[-1]) for i in rec.time]
	else:
		time_data = rec.time
	# Save data as datetime or seconds format based on user option
	if time_type == 0:
		time = []
		# Add time from comtrade to start time for each entry and save
		for timestep in time_data:
			t = rec.start_timestamp + datetime.timedelta(seconds=timestep)
			t = t.strftime('%d/%m/%Y %H:%M:%S.%f')
			time.append(t)
	else:
		time = time_data
	# Get comtrade data as df. Analog data from comtrade module had to be transposed (columns swapped with rows).	
	df_data = pandas.DataFrame(numpy.transpose(rec.analog), index=time, columns=rec.analog_channel_ids)
	# Save dataframe as csv
	df_data.to_csv(csv_file)