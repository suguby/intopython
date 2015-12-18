sudo apt-get install nginx
wget https://raw.githubusercontent.com/nginx/nginx/master/conf/uwsgi_params

sudo ln -s /home/user/PycharmProjects/intopython/nginx.conf /etc/nginx/sites-enabled/intopython.conf

ll /etc/nginx/sites-enabled/
sudo service nginx restart


sudo apt-get install python3-pip
pip3
sudo pip3 install uwsgi
uwsgi --ini uwsgi.ini
touch extra/uwsgi.reload

sudo nano /etc/hosts
sudo service nginx restart
ping mysite.ru



sudo apt-get install apache2, libapache2-mod-wsgi-py3
sudo ln -s /home/user/PycharmProjects/intopython/apache.conf /etc/apache2/sites-available/mysite.conf
sudo a2ensite mysite
sudo service apache2 reload


