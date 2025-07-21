Vagrant.configure("2") do |config|
  config.vm.define "jenkins" do |jenkins|
    config.vm.box = "bento/ubuntu-22.04"
    jenkins.vm.hostname = "jenkins"
    jenkins.vm.network "private_network", ip: "192.168.56.10"
    jenkins.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 2
    end
  end

  config.vm.define "ansible" do |ansible|
    config.vm.box = "bento/ubuntu-22.04"
    ansible.vm.hostname = "ansible"
    ansible.vm.network "private_network", ip: "192.168.56.20"
    ansible.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus = 1
    end
  end

  config.vm.define "app-server" do |app|
    config.vm.box = "bento/ubuntu-22.04"
    app.vm.hostname = "app-server"
    app.vm.network "private_network", ip: "192.168.56.30"
    app.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus = 1
    end
  end
end
