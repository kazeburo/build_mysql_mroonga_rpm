# -*- mode: ruby -*-
# vi: set ft=ruby :

# This vagrantfile required destroy provisioner
# vagrant plugin install vagrant-destroy-provisioner


VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vbguest.auto_update = false
  config.vm.box = "CentOS-6.4-x86_64-v20131103"
  config.vm.box_url = "http://developer.nrel.gov/downloads/vagrant-boxes/CentOS-6.4-x86_64-v20131103.box"
  config.vm.provision "shell", path: "provision.sh"
  config.vm.provision "destroy"
end

