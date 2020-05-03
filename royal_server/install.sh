# Install python
python3.6 -m venv pokerenv
source pokerenv/bin/activate
pip install -r requirements.txt


# Update nginx config
# ## Manually replace the proxy_pass
#    line with the poker_dir if necessary
# proxy_pass http://unix:/home/${username}/repos/poker/royal_server/poker.sock;
sudo nginx -t && sudo systemctl restart nginx

# update the systemd service file
sudo systemctl stop poker
sed -i 's/${username}/yourusername/g' files/poker.service
sudo cp files/poker.service /etc/systemd/system/poker.service

sudo systemctl daemon-reload
sudo systemctl start poker

