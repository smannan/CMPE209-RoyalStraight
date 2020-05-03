sudo systemctl stop poker
source pokerenv/bin/activate
pip install -r requirements.txt
python pokersqrl.py
deactivate
sudo systemctl start poker