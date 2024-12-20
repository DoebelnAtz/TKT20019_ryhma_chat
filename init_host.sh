#!/bin/bash

#Email from command line argument
# Check if email argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Email address required as command line argument"
    echo "Usage: $0 [email@example.com] [password]" 
    exit 1
fi

EMAIL=$1
DB_PASSWORD=$2

export DB_USER="marvin"
export DB_NAME="deep_thought"


# Bash script to set up a Flask app with WebSocket support on a Debian server
# This script assumes that I've already cloned the TKT_Chat repository to ~/TKT_Chat and it is ran inside that directory
DIRECTORY="TKT_Chat"
DOMAIN="taival.app" # A domain I happen to have

# Exit immediately if a command exits with a non-zero status
set -e

echo "Updating and upgrading the system packages..."
sudo apt update
sudo apt upgrade -y

# Check if the PostgreSQL setup script is already run
if [ ! -f /etc/postgresql/$(ls /etc/postgresql)/main/postgresql.conf ]; then
    echo "Setting up PostgreSQL..."
    ./init_host_postgres.sh $DB_PASSWORD
else
    echo "PostgreSQL setup already completed."
fi

echo "Installing Python3, pip3, and virtualenv..."
sudo apt install -y python3 python3-pip python3-venv

cd ~/$DIRECTORY
# check if key is already set in key.txt
if [ ! -f key.txt ]; then
    secret_key=$(openssl rand -hex 32)
    echo $secret_key > key.txt
    echo "Secret key generated and saved to key.txt"
else
    echo "Secret key already set in key.txt"
fi
echo "Setting up a virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Flask and dependencies..."
pip install -r ~/$DIRECTORY/requirements.txt

echo "Deactivating the virtual environment..."
deactivate


echo "Installing Nginx..."
sudo apt install -y nginx

echo "Configuring Nginx to reverse proxy to the Flask app..."
NGINX_CONF="/etc/nginx/sites-available/$DIRECTORY"

sudo bash -c "cat > $NGINX_CONF" << EOL
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_read_timeout 86400;
    }

    location /static/ {
        alias /home/$USER/$DIRECTORY/app/static/;
    }
}
EOL

echo "Enabling the new Nginx configuration..."
sudo ln -sf /etc/nginx/sites-available/$DIRECTORY /etc/nginx/sites-enabled/

echo "Removing the default Nginx configuration..."
sudo rm -f /etc/nginx/sites-enabled/default

echo "Testing Nginx configuration..."
sudo nginx -t

echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "Installing certbot..."
sudo apt install -y certbot python3-certbot-nginx

echo "Enabling certbot to automatically renew SSL certificates..."
sudo systemctl enable --now certbot.timer


echo "Obtaining SSL certificate with Certbot..."
sudo certbot --nginx --non-interactive --agree-tos --redirect -d ${DOMAIN} --email ${EMAIL}


echo "Creating a systemd service file for the Flask app..."
SERVICE_FILE="/etc/systemd/system/$DIRECTORY.service"

# Note — gunicorn doesn't seem to look at .flaskenv file, so we need to set the environment variables here
sudo bash -c "cat > $SERVICE_FILE" << EOL
[Unit]
Description=Gunicorn instance to serve $DIRECTORY Flask app
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/home/$USER/$DIRECTORY
Environment="PATH=/home/$USER/$DIRECTORY/venv/bin"
Environment="FLASK_APP=app:create_app"
Environment="FLASK_ENV=production"
Environment="DB_PASSWORD=$DB_PASSWORD"
Environment="SECRET_KEY=$(cat key.txt)"
ExecStart=/home/$USER/$DIRECTORY/venv/bin/gunicorn --worker-class eventlet -w 1 -b localhost:5000 app:app --reload

[Install]
WantedBy=multi-user.target
EOL

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Starting and enabling the Flask app service..."
sudo systemctl start $DIRECTORY.service
sudo systemctl enable $DIRECTORY.service

echo "Checking the status of the service..."
sudo systemctl status $DIRECTORY.service --no-pager


echo "Installing Fail2ban..."
sudo apt install -y fail2ban

echo "Creating local jail configuration for Fail2ban..."
sudo bash -c "cat > /etc/fail2ban/jail.local" << EOL
[sshd]
enabled = true
port    = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s

[nginx-http-auth]
enabled = true

[nginx-botsearch]
enabled  = true

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
findtime = 60
bantime = 3600     # 1 hour
maxretry = 5       

[nginx-req-limit]
enabled = true
filter = nginx-req-limit
logpath = /var/log/nginx/error.log
findtime = 60
bantime = 7200     # 2 hours
maxretry = 3

[nginx-dos]
enabled  = true

[nginx-nohome]
enabled = true

[nginx-noproxy]
enabled = true

[nginx-badbots]
enabled  = true

[nginx-auth]
enabled = true

[nginx-botsearch]
enabled = true
EOL

echo "Restarting Fail2ban service..."
sudo systemctl restart fail2ban

echo "Setup complete. Your Flask app should now be running and accessible."
