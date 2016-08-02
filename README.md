
# ImageSub.

ImageSub is web app project using  Recurrent Neural Network. This project based on NeuralTalk V2 by [Andrej Karpathy] (https://github.com/karpathy). I modify the project in order to interact with the user via a web application. So Users can upload pictures or photographs that they want to identify its caption. 

This is an early code release that works great but is slightly hastily released and probably requires some code reading of inline comments (which I tried to be quite good with in general). I will be improving it over time but wanted to push the code out there because I promised it to too many people.


![teaser results](https://lh3.googleusercontent.com/-Znrp20opeTI/V5_5BIGEYbI/AAAAAAAABUE/q5ZBjnd4ZFksNG0gXnCd1ZtquctDfdlaACCo/s576/Screen%2BShot%2B2016-08-02%2Bat%2B8.33.25%2BAM.png)


### Requirements
See original readme : (https://github.com/karpathy/neuraltalk2/blob/master/README.md)


#### For evaluation only

This code is written in Lua and requires [Torch](http://torch.ch/). If you're on Ubuntu, installing Torch in your home directory may look something like: 

```bash
$ curl -s https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash
$ git clone https://github.com/torch/distro.git ~/torch --recursive
$ cd ~/torch; 
$ ./install.sh      # and enter "yes" at the end to modify your bashrc
$ source ~/.bashrc
```

See the Torch installation documentation for more details. After Torch is installed we need to get a few more packages using [LuaRocks](https://luarocks.org/) (which already came with the Torch install). In particular:

```bash
$ luarocks install nn
$ luarocks install nngraph 
$ luarocks install image 
```

We're also going to need the [cjson](http://www.kyne.com.au/~mark/software/lua-cjson-manual.html) library so that we can load/save json files. Follow their [download link](http://www.kyne.com.au/~mark/software/lua-cjson.php) and then look under their section 2.4 for easy luarocks install.

If you'd like to run on an NVIDIA GPU using CUDA (which you really, really want to if you're training a model, since we're using a VGGNet), you'll of course need a GPU, and you will have to install the [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit). Then get the `cutorch` and `cunn` packages:

```bash
$ luarocks install cutorch
$ luarocks install cunn
```

If you'd like to use the cudnn backend (the pretrained checkpoint does), you also have to install [cudnn](https://github.com/soumith/cudnn.torch). First follow the link to [NVIDIA website](https://developer.nvidia.com/cuDNN), register with them and download the cudnn library. Then make sure you adjust your `LD_LIBRARY_PATH` to point to the `lib64` folder that contains the library (e.g. `libcudnn.so.7.0.64`). Then git clone the `cudnn.torch` repo, `cd` inside and do `luarocks make cudnn-scm-1.rockspec` to build the Torch bindings.

#### For training

If you'd like to train your models you will need [loadcaffe](https://github.com/szagoruyko/loadcaffe), since we are using the VGGNet. First, make sure you follow their instructions to install `protobuf` and everything else (e.g. `sudo apt-get install libprotobuf-dev protobuf-compiler`), and then install via luarocks:

```bash
luarocks install loadcaffe
```

Finally, you will also need to install [torch-hdf5](https://github.com/deepmind/torch-hdf5), and [h5py](http://www.h5py.org/), since we will be using hdf5 files to store the preprocessed data.

Phew! Quite a few dependencies, sorry no easy way around it :\

### I just want to caption images

In this case you want to run the evaluation script on a pretrained model checkpoint. 
I trained a decent one on the [MS COCO dataset](http://mscoco.org/) that you can run on your images.
The pretrained checkpoint can be downloaded here: [pretrained checkpoint link](http://cs.stanford.edu/people/karpathy/neuraltalk2/checkpoint_v1.zip) (600MB). It's large because it contains the weights of a finetuned VGGNet. Now open `vis/app.py`, and edit line :

```bash
subprocess.call('th eval.lua -model ../Public/model_id1-501-1448236541_cpu.t7 -image_folder '+folder_path+' -num_images 1 -result_folder vis/'+dir, shell=True, cwd="../") 
```

`-model` is where your model located.
Run python server

```bash
$ cd vis
$ python app.py
```

Now visit `localhost:8000` in your browser.


**"I only have CPU"**. Okay, in that case download the [cpu model checkpoint](http://cs.stanford.edu/people/karpathy/neuraltalk2/checkpoint_v1_cpu.zip). Make sure you run the eval script with `-gpuid -1` to tell the script to run on CPU. On my machine it takes a bit less than 1 second per image to caption in CPU mode.

### I'd like to train my own network on MS COCO

Great, first we need to some preprocessing. Head over to the `coco/` folder and run the IPython notebook to download the dataset and do some very simple preprocessing. The notebook will combine the train/val data together and create a very simple and small json file that contains a large list of image paths, and raw captions for each image, of the form:

```
[{ "file_path": "path/img.jpg", "captions": ["a caption", "a second caption of i"tgit ...] }, ...]
```

Once we have this, we're ready to invoke the `prepro.py` script, which will read all of this in and create a dataset (an hdf5 file and a json file) ready for consumption in the Lua code. For example, for MS COCO we can run the prepro file as follows:

```bash
$ python prepro.py --input_json coco/coco_raw.json --num_val 5000 --num_test 5000 --images_root coco/images --word_count_threshold 5 --output_json coco/cocotalk.json --output_h5 coco/cocotalk.h5
```

This is telling the script to read in all the data (the images and the captions), allocate 5000 images for val/test splits respectively, and map all words that occur <= 5 times to a special `UNK` token. The resulting `json` and `h5` files are about 30GB and contain everything we want to know about the dataset.

**Warning**: the prepro script will fail with the default MSCOCO data because one of their images is corrupted. See [this issue](https://github.com/karpathy/neuraltalk2/issues/4) for the fix, it involves manually replacing one image in the dataset.

The last thing we need is the [VGG-16 Caffe checkpoint](http://www.robots.ox.ac.uk/~vgg/research/very_deep/), (under Models section, "16-layer model" bullet point). Put the two files (the prototxt configuration file and the proto binary of weights) somewhere (e.g. a `model` directory), and we're ready to train!

```bash
$ th train.lua -input_h5 coco/cocotalk.h5 -input_json coco/cocotalk.json
```

The train script will take over, and start dumping checkpoints into the folder specified by `checkpoint_path` (default = current folder). You also have to point the train script to the VGGNet protos (see the options inside `train.lua`).

If you'd like to evaluate BLEU/METEOR/CIDEr scores during training in addition to validation cross entropy loss, use `-language_eval 1` option, but don't forget to download the [coco-caption code](https://github.com/tylin/coco-caption) into `coco-caption` directory.

**A few notes on training.** To give you an idea, with the default settings one epoch of MS COCO images is about 7500 iterations. 1 epoch of training (with no finetuning - notice this is the default) takes about 1 hour and results in validation loss ~2.7 and CIDEr score of ~0.4. By iteration 70,000 CIDEr climbs up to about 0.6 (validation loss at about 2.5) and then will top out at a bit below 0.7 CIDEr. After that additional improvements are only possible by turning on CNN finetuning. I like to do the training in stages, where I first train with no finetuning, and then restart the train script with `-finetune_cnn_after 0` to start finetuning right away, and using `-start_from` flag to continue from the previous model checkpoint. You'll see your score rise up to about 0.9 CIDEr over ~2 days or so (on MS COCO).

### I'd like to train on my own data

No problem, create a json file in the exact same form as before, describing your JPG files:

```
[{ "file_path": "path/img.jpg", "captions": ["a caption", "a similar caption" ...] }, ...]
```

and invoke the `prepro.py` script to preprocess all the images and data into and hdf5 file and json file. Then invoke `train.lua` (see detailed options inside code).

### I'd like to distribute my GPU trained checkpoints for CPU

Use the script `convert_checkpoint_gpu_to_cpu.lua` to convert your GPU checkpoints to be usable on CPU. See inline documentation for why this separate script is needed. For example:

```bash
th convert_checkpoint_gpu_to_cpu.lua gpu_checkpoint.t7
```

write the file `gpu_checkpoint.t7_cpu.t7`, which you can now run with `-gpuid -1` in the eval script.

### License

BSD License.

### Acknowledgements

Parts of this code were written in collaboration with my labmate [Justin Johnson](http://cs.stanford.edu/people/jcjohns/). 

I'm very grateful for [NVIDIA](https://developer.nvidia.com/deep-learning)'s support in providing GPUs that made this work possible.

I'm also very grateful to the maintainers of Torch for maintaining a wonderful deep learning library.
