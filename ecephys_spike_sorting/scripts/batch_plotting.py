from ecephys_spike_sorting.common.visualization import plotKsTemplates
ks_directory = r'F:\CatGT\catgt_AA_201025_2_201123_mismatch_1_g0\AA_201025_2_201123_mismatch_1_g0_imec0\imec0_ks2'
raw_data_file = r'F:\CatGT\catgt_AA_201025_2_201123_mismatch_1_g0\AA_201025_2_201123_mismatch_1_g0_imec0\AA_201025_2_201123_mismatch_1_g0_tcat.imec0.ap.bin'
output_path = None

plotKsTemplates(ks_directory, raw_data_file, sample_rate = 30000, bit_volts = 0.195, time_range = [10, 11], exclude_noise=True, fig=None, output_path=output_path)



# import glob

# from ecephys_spike_sorting.common.visualization import plotContinuousFile

# mouse = '72112' #, '425589', '432104', '425597'] #,'434845','434494','434843']

# probes = ['probeA','probeB','probeC','probeD','probeE','probeF']

# for probe in probes:

#     output_path = r'/mnt/nvme0/continuous_file_qc/' + mouse + '_' + probe + '.png'
#     raw_data_file = glob.glob(r'/mnt/sd5.3/RE-SORT/*' + mouse + '*/*' + probe + '*/continuous/Neuropix-3a-100.0/continuous.dat')[0]

#     plotContinuousFile(raw_data_file, time_range = [5000, 5002], output_path=output_path)
