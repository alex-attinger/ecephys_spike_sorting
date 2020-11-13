import os, io, json
import subprocess

from helpers import SpikeGLX_utils
from create_input_json import createInputJson

# run a set of SpikeGLX tcat.probeN.bin files that are stored in one folder.
# creates an output folder for each, generatees a channel map file from
# the SpikeGLX metadata, then runs any other listed modules.

# directory for json files -- these record the parameters used for processing
#json_directory = r'F:\CatGT\catgt_AA_200920_4_201005_dark_g0\AA_200920_4_201005_dark_g0_imec0'

# directory with the raw data files. The metadata should be present, also
#npx_directory = r'F:\CatGT\catgt_AA_200920_4_201005_dark_g0\AA_200920_4_201005_dark_g0_imec0'


# list of run names
import glob
import os
 
run_names = [												
						'AA_200920_4_201005_dark_g0_tcat.imec0.ap.bin',

]
run_names = glob.glob('F:\\CatGT\\cat*\\*\\*.ap.bin')

probe_type = 'NP1'



# List of modules to run per probe
# if not running kilosort_helper, KS2 output must be in directories
# named according to this script, i.e. run_name_gN_tcat.imecN_phy
modules = [
            #'depth_estimation',
			'kilosort_helper',
            'kilosort_postprocessing',
            #'noise_templates',
            #'psth_events',
            'mean_waveforms',
            'quality_metrics'

		  ]

for fi in run_names:
    
    [h,t] = os.path.split(fi)
    name=t
    json_directory = h
    npx_directory = h
    baseName = SpikeGLX_utils.ParseTcatName(name)
    prbStr = SpikeGLX_utils.GetProbeStr(name)   # returns empty string for 3A
    session_id = baseName

    # Create output directory
    kilosort_output_parent = os.path.join(npx_directory)
    
    if not os.path.exists(kilosort_output_parent):
        os.mkdir(kilosort_output_parent)
        
    # output subdirectory
    extra = '_9_2'
    outputName = 'imec' + prbStr + '_ks' + extra
    
    kilosort_output_dir = os.path.join(kilosort_output_parent, outputName)


    input_json = os.path.join(json_directory, session_id + extra +'-input.json')
    output_json = os.path.join(json_directory, session_id + extra+ '-output.json')
    
    # kilosort_postprocessing and noise_templates moduules alter the files
    # that are input to phy. If using these modules, keep a copy of the
    # original phy output
    if ('kilosort_postprocessing' in modules) or ('noise_templates' in modules):
        ks_make_copy = True
    else:
        ks_make_copy = False
    
    print( 'Creating json file for KS2 and postprocessing')
    info = createInputJson(input_json, npx_directory=npx_directory, 
	                                   continuous_file = os.path.join(npx_directory,name),
                                       spikeGLX_data = 'True',
									   kilosort_output_directory=kilosort_output_dir, 
                                       ks_make_copy = ks_make_copy,
                                       extracted_data_directory = npx_directory,
                                       noise_template_use_rf = True
                                       )
    kilosort2_params = info["kilosort_helper_params"]["kilosort2_params"]
    kilosort2_params["minfr_goodchannels"] = 0.01
    kilosort2_params["Th"]= '[9 2]'
    kilosort2_params["ThPre"] = 5


    info["kilosort_helper_params"]["kilosort2_params"]= kilosort2_params
    with io.open(input_json, 'w', encoding='utf-8') as f:
        f.write(json.dumps(info, ensure_ascii=False, sort_keys=True, indent=4))
    
    print(info["kilosort_helper_params"]["kilosort2_params"])
    for module in modules:
        command = "python -W ignore -m ecephys_spike_sorting.modules." + module + " --input_json " + input_json \
		          + " --output_json " + output_json
        subprocess.check_call(command.split(' '))
        
        
        
	


    
