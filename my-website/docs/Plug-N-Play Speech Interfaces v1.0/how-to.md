---
tags:
  - Foundation-AI
---

# How-To Guides

### Installation
To successfully install the environment needed to run this code, run the following commands:
```
sudo apt-get install libasound-dev
wget https://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz
tar -xvzf pa_stable_v190700_20210406.tgz
cd portaudio
./configure
make
sudo make install
sudo ldconfig
```
This will install portaudio. You need port audio in order to successfully install PyAudio. You can then proceed with installing python requirements. Start by install PyTorch first. Note: You must use 2.0.0.
```
conda create --name speechgui --file requirements_versionless.txt
conda activate speechgui
pip install torch==2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
Once PyTorch is installed you can let pip handle the rest. You can use conda if you want, but do not install PyAudio with Conda. There is a known issue with the default package build that conda selects for 0.2.14. Use the default package from pip to avoid this.
```
pip install -r requirements.txt
```
We have added functionality to make hosting models remotely possible. Please follow the [install instructions](https://github.com/pytorch/serve) for Torch Serve in order to use the move-models branch. This is an ongoing work in progress. And HTTPS request functionality is only partially established. 

Your environment should now be set up. 

### Running the Program
Start the server by running:
```
python manage.py runserver
```
You should then receive a message that says something along the lines of:
```
Starting development server at http://127.0.0.1:8000/
```
Open the provided web address in your browser. You can then select a wake word and choose whether you want to enter test mode or ICICLE mode. Note that when your portaudio processes start loading you will probably get a number of warning messages saying that certain devices do not exist. This is normal and to be expected--- it is caused by the default configuration file automatically assuming certain devices exist. Just ignore these messages.
