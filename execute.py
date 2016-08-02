import subprocess

subprocess.call('th eval.lua -model ../Public/model_id1-501-1448236541_cpu.t7 -image_folder ../Downloads/ -num_images 1 -gpuid -1', shell=True)


