
# ImageSub.

ImageSub is web app project using  Recurrent Neural Network. This project based on NeuralTalk2 by [Andrej Karpathy] (https://github.com/karpathy). I modify the project in order to interact with the user via a web application. So Users can upload pictures or photographs that they want to identify its caption. 
If you prefer using Docker and Restful version, you can using neuraltalk2-web : https://github.com/jacopofar/neuraltalk2-web

This is an early code release that works great but is slightly hastily released and probably requires some code reading of inline comments (which I tried to be quite good with in general). I will be improving it over time but wanted to push the code out there because I promised it to too many people.


![teaser results](https://lh3.googleusercontent.com/-Znrp20opeTI/V5_5BIGEYbI/AAAAAAAABUE/q5ZBjnd4ZFksNG0gXnCd1ZtquctDfdlaACCo/s576/Screen%2BShot%2B2016-08-02%2Bat%2B8.33.25%2BAM.png)


### Requirements
See original instruction here : (https://github.com/karpathy/neuraltalk2/blob/master/README.md)
Now you need to clone or download this project into your machine and open open `vis/app.py`, and edit line :

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


**"I only have CPU"**. Okay, in that case download the [cpu model checkpoint](http://cs.stanford.edu/people/karpathy/neuraltalk2/checkpoint_v1_cpu.zip). Make sure you add `-gpuid -1` in `vis/app.py` to tell the script to run on CPU. 


### License

BSD License.
