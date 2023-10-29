# ipa-resigner
Resign ipa tool

# Resign ipa
```bash
python3 resign.py \
--ipa your_ipa.ipa \
--profile <Your provision profile path> \
--certificate <your certificate name> \
--bundle <new bundle id>
```

Example
```bash
python3 resign.py \
--ipa facebook.ipa \
--profile fb-profile.mobileprovision \
--certificate "iPhone Developer: Thanh Vu (FTFWZ27352)" \
--bundle com.demo.fb
```

# Inject a framework
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
