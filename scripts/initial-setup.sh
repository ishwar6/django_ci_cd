sudo apt-get update -y

wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | 
  sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
/etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins

sudo systemctl daemon-reload
sudo systemctl start jenkins

sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl enable jenkins
sudo systemctl status jenkins

