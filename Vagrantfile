Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.provision "shell", inline: <<-SHELL
    # add the repositroy for python3.6
    add-apt-repository ppa:deadsnakes/ppa -y
    apt-get update

    # install system requirements
    apt-get install nginx python3.6 python3.6-venv -y
    apt-get upgrade -y

    # install python requirements
    python3.6 -m venv venv
    chown -R ubuntu venv  # make sure we own the venv directory
    source venv/bin/activate
    pip install -r /vagrant/requirements.txt

    # create our local database, this will change to postgresql later
    mkdir /database
    chown ubuntu /database
    python /vagrant/manage.py migrate

    # Activate the python virtual environment on ssh login
    echo "source venv/bin/activate" >> /home/ubuntu/.bashrc
    # also change directory to our project root
    echo "cd /vagrant" >> /home/ubuntu/.bashrc
  SHELL
end
