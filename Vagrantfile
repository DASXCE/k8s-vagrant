Vagrant.configure("2") do |config|

  # centos/7 box + yum updates + install docker + install BlueCoat cert
  # commented out. Docker version is higher than in the CKAD labs.
  #config.vm.box = "centos7-docker-bluecoat"
  #config.vm.box = "centos/8"
  config.vm.box = "centos-8-bluecoat"
  # When enabled it is very slow!
  config.vm.box_check_update = false
  # centos7 is 40GB, it does not matter as it is shared...
  # config.disksize.size = "10GB"

  # default hardware
  config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2

        # This does not work. Still getting nameserver 10.0.2.3
        #v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        #v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  # PROXY CONFIG
  # Not needed anymore. cntlm proxy deprecated in favor of BlueCoat
  if Vagrant.has_plugin?("vagrant-proxyconf") && ENV['use_proxy']
    config.proxy.http     = "http://10.10.10.1:3128/"
    config.proxy.https    = "http://10.10.10.1:3128/"
    config.proxy.no_proxy = "localhost,127.0.0.1,.example.com, 10.*, 192.168.*, *.1dc.com, *.gzs.de"
  end

  # Add Salt master to /etc/hosts
  # ~~Disabled - using dnsmasq instead~~
  # Update: still needed because Vagrant fucks up /etc/resolv.conf
  # With this salt can work and then the fd_resolver state must be reapplied

  # New: vagrant plugin install vagrant-dns
  #config.dns.tld = "lab"
  # vagrant plugin install vagrant-hosts
  config.vm.provision :hosts do |provisioner|
    provisioner.sync_hosts = true
  end
  #config.vm.provision "shell", inline: "sudo echo '10.10.10.10 salt k8scp' | sudo tee -a /etc/hosts"

  # this is executed only once at 'provision' time.
  # swap has to be disabled permanently by removing the fstab entry.
  config.vm.provision "shell", inline: "swapoff -a"
  config.vm.provision "shell", inline: "sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab"

  # Default ssh login / commented as it was not working
  #config.ssh.username = 'root'
  #config.ssh.password = 'vagrant'
  #config.ssh.insert_key = 'true' # sa ovim je greska root@127.0.0.1: Permission denied (publickey).

  ## K8S CLUSTER
  # master
  config.vm.define "master" do |subconfig|
    subconfig.vm.network "forwarded_port", guest: 443, host: 4443
    # Kube API server port
    subconfig.vm.network "forwarded_port", guest: 6443, host: 6643
    subconfig.vm.network "private_network", ip: "10.10.10.10"
    subconfig.vm.hostname = "rxtvap1010"
    #subconfig.dns.patterns = "rxtvap1010.k8s.lab", "k8scp", "salt"
    #subconfig.vm.provision :hosts do |provisioner|
    #  provisioner.add_host '10.10.10.10', ['rxtvap1010.k8s.lab', 'rxtvap1010']
    #end

    subconfig.vm.synced_folder "/Users/f5boc77/git/Salt/", "/srv/salt/"
    subconfig.vm.synced_folder "/Users/f5boc77/git/Salt_Assets/", "/srv/assets/"
  end

  # worker1
  config.vm.define "worker1" do |subconfig|
    subconfig.vm.network "private_network", ip: "10.10.10.11"
    subconfig.vm.hostname = "rxtvap1011"
    #subconfig.dns.patterns = "rxtvap1011.k8s.lab"
    #subconfig.vm.provision.add_host '10.10.10.11', ['rxtvap1011.k8s.lab', 'rxtvap1011']
  end

  # worker2
  config.vm.define "worker2" do |subconfig|
    subconfig.vm.network "private_network", ip: "10.10.10.12"
    subconfig.vm.hostname = "rxtvap1012"
    #subconfig.dns.patterns = "rxtvap1012.k8s.lab"
    #subconfig.vm.provision.add_host '10.10.10.12', ['rxtvap1012.k8s.lab', 'rxtvap1012']
  end

  ## ETCD CLUSTER
  # etcd1
  config.vm.define "etcd1" do |subconfig|
    subconfig.vm.network "private_network", ip: "10.10.10.21"
    subconfig.vm.hostname = "rxtvap1021"
    #subconfig.dns.patterns = "rxtvap1021.k8s.lab"
  end

  # etcd2
  config.vm.define "etcd2" do |subconfig|
    subconfig.vm.network "private_network", ip: "10.10.10.22"
    subconfig.vm.hostname = "rxtvap1022"
    #subconfig.dns.patterns = "rxtvap1022.k8s.lab"
  end

  # etcd3
  config.vm.define "etcd3" do |subconfig|
    subconfig.vm.network "private_network", ip: "10.10.10.23"
    subconfig.vm.hostname = "rxtvap1023"
    #subconfig.dns.patterns = "rxtvap1023.k8s.lab"
  end
end
