# reddit-deleter-2025
A simple script to delete your reddit post history. Working in 2025. It will edit your comments first to whatever you want to replace them with (not sure if this matters)

Note that if you have a lot of posts to delete, reddit may rate limit you. If this happens, wait until later and then try again. Or change your IP address.

To use, install python and run the following commands:

### Linux

```bash
git clone https://github.com/mythemeria/reddit-deleter.git
cd reddit-deleter
python -m venv venv
source ./venv/bin/activate
pip install selenium
python delete.py
```

If someone who uses windows can provide instructions for running this on windows, that would be appreciated.
