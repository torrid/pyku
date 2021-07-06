This source installs and configures a (local) kubernetes cluster from scratch,
and deploys a Python/Flask workload onto 2 nodes, providing a way to create and
measure CPU load on them.  

The purpose of this rather academic project is to get to know how K8s works and
acts, and to learn how to communicate with the nodes. 

Since I had to start somewhere, I assume a regular Linux user with sudo/root
access, and the group names "kube" and "docker" for the respective services.
"Works on my machine" (Arch linux t2.micro EC2 instance). 

### install docker, dockerd
`sudo pacman -Sy docker ethtool wget unzip containerd`
### install kubernetes
`sudo pacman -Sy kubectl kubernetes-control-plane kubernetes-node kubeadm`
### install python/pip
`sudo pacman -Sy python-pip`
### misc stuff 
`sudo pacman -Sy stress`

### install etcd
```bash
sudo pacman -Sy go 
mkdir pkg && cd pkg
git clone https://aur.archlinux.org/etcd.git
cd etcd
makepkg 
sudo pacman -U etcd-.*.pkg.tar.zst 
cd ../..
```
### install necessary python modules
#### sudo pip makes sure to install the necessary Python modules system-wide.
#### !!! DOUBLE check to mention same dependencies in $app/docker/Dockerfile
sudo pip3 install kubernetes psutil flask  



### Flask Workload
The 
.
├── app
│   ├── main.py
│   └── requirements.txt
├── docker
│   └── Dockerfile
├── kubernetes
│   └── deployment.yaml
├── LICENSE
└── README.md

# Init and start cluster.

sudo systemctl enable kubelet && sudo systemctl start kubelet
sudo systemctl enable docker  && sudo systemctl start docker 
sudo groupadd docker kube  		# this may fail, since the groups are created at installation 
sudo usermod -a -G docker,kube $USER
sudo su - $USER 				# relogin with new group env. 
sudo kubeadm init --pod-network-cidr=10.10.0.0/16 --ignore-preflight-errors=NumCPU,Mem
# !!! Opening the permissions for the kubelet certificate to the kube group. 
# !!! I would rather ask a Kubernetes Guru if that's the right idea.
sudo chgrp kube /var/lib/kubelet/pki/kubelet*pem
sudo chmod g+r /var/lib/kubelet/pki/kubelet*pem
mkdir -p ~/.kube
sudo cp -i /etc/kubernetes/admin.conf ~/.kube/config
sudo chown :kube ~/.kube/config
sudo chmod chmod g+rw .kube/config

