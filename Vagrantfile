Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/srv/tictic", :owner=> 'vagrant', :group=>'www-data', :mount_options => ['dmode=775', 'fmode=775']
  config.vm.network "private_network", ip: "192.168.33.103"
  # config.vm.provision "ansible" do |ansible|
  #   ansible.verbose = "v"
  #   ansible.playbook = "playbook.yml"
  # end
end
