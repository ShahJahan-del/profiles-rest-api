# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Choix de la box Ubuntu
  config.vm.box = "bento/ubuntu-24.04"

  # --- AJOUT : Augmentation du timeout à 10 minutes (600 secondes) ---
  # Idéal pour éviter le "Timed out while waiting for the machine to boot" sur Windows/OneDrive
  config.vm.boot_timeout = 600

  # Redirection de port pour ton API Django
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Script de configuration initiale (Provisioning)
  config.vm.provision "shell", inline: <<-SHELL
    # Désactivation des mises à jour automatiques en arrière-plan pour éviter de bloquer apt-get
    systemctl disable apt-daily.service
    systemctl disable apt-daily.timer

    # Installation des prérequis pour Django et Python
    sudo apt-get update
    sudo apt-get install -y python3-venv zip

    # Ton script magique qui crée l'alias 'python' pour appeler 'python3' automatiquement !
    touch /home/vagrant/.bash_aliases
    if ! grep -q PYTHON_ALIAS_ADDED /home/vagrant/.bash_aliases; then
      echo "# PYTHON_ALIAS_ADDED" >> /home/vagrant/.bash_aliases
      echo "alias python='python3'" >> /home/vagrant/.bash_aliases
    fi
  SHELL
end
