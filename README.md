# resign.py + inject_framework.py 
Easily resign and inject a framework into a .ipa file in minutes!

# resign.py - Easily resign an .ipa file

`Code resigning` is the process where we re-sign an existing application with a new signing identity due to various reasons (the old signing identity expired, you want to tamper the existing app for educational purpose, etc...)

In iOS development, manually resigning an existing ipa is a complex and time consuming process. In order to simply this process, I've created `resign.py` to save our fellow developers some time. 

## Usage

Given an existing `Their_App.ipa` file and you want to resign this ipa file you will need to prepare your new signing identity (your certificate and the provisiong profile). 

Once you've have your code signing identity ready in your local machine, you can run resign.py from terminal (make sure your have Python installed on your machine): 

```bash
python3 resign.py \
--ipa <path to Their_App.ipa \
--profile <Path to your provision profile> \
--certificate <path to your certificate> \
--bundle <new bundle id>
```

Example:
```bash
python3 resign.py \
--ipa facebook.ipa \
--profile fb-profile.mobileprovision \
--certificate "iPhone Developer: Thanh Vu (FTFWZ27352)" \
--bundle com.demo.fb
```

# inject_framework.py - Easily injecting a framework into an .ipa file
You have a framework which you want to inject into an existing .ipa file? `inject_framework.py`'s here for the rescure. 
`inject_framework.py` is made ontop of `resign.py` and [optool](https://github.com/alexzielenski/optool)

Usages
```bash
python3 inject_framework.py \
--ipa your_ipa.ipa \
--profile <Your provision profile path> \
--certificate <your certificate name> \
--bundle <new bundle id> \
--framework <framework path>
```

Example
```bash
python3 inject_framework.py \
--ipa facebook.ipa \
--profile fb-profile.mobileprovision \
--certificate "iPhone Developer: Thanh Vu (FTFWZ27352)" \
--bundle com.demo.fb \
--framework SomethingSecret.framework
```


