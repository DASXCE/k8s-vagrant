### Prepare
```sh
sudo yum update -y
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

sudo yum install wget -y
#
```

### Install Docker

```sh
sudo yum install -y yum-utils

 sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

sudo yum install docker-ce docker-ce-cli containerd.io -y

sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl stop docker

cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF
sudo systemctl start docker
sudo docker info
#
```

### Kubeadm, kubelet, kubectl
```sh
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

# Set SELinux in permissive mode (effectively disabling it)
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

sudo systemctl enable --now kubelet
#
```

### Bootrstrap the Controll plane
```sh
# You can download images only
#kubeadm config images pull

cat <<EOF | sudo tee kubeadm-config.yaml
apiVersion: kubeadm.k8s.io/v1beta2
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: "10.10.10.10"
  bindPort: 6443
---
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
kubernetesVersion: 1.22.4               #<-- Use the word stable for newest version
controlPlaneEndpoint: "rxtvap1010:6443"  #<-- Use the node alias not the IP
networking:
  podSubnet: 192.168.0.0/16 # Calico default CALICO_IPV4POOL_CIDR
EOF

kubeadm init --config=kubeadm-config.yaml --upload-certs | tee kubeadm-init.out
#
```

### Setup KUBECONFIG
```sh
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
echo "source <(kubectl completion bash)" >> $HOME/.bashrc

kubectl get pods -n kube-system
#
```


### CNI - Calico
```sh
wget https://docs.projectcalico.org/manifests/calico.yaml

kubectl apply -f calico.yaml
#
```

### Join worker node
```sh
# On the master
sudo kubeadm token create

openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | \
openssl rsa -pubin -outform der 2>/dev/null | \
openssl dgst -sha256 -hex | sed 's/ˆ.* //' | 

# On the worker
sudo kubeadm join rxtvap1010:6443 --token TOKEN --discovery-token-ca-cert-hash sha256:HASH
#
```
