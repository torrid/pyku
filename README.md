

# install docker, dockerd
sudo pacman -Sy docker ethtool wget unzip containerd
# install kubernetes
sudo pacman -Sy kubectl kubernetes-control-plane kubernetes-node kubeadm
# install python/pip
sudo pacman -Sy python-pip
# misc stuff 
sudo pacman -Sy stress 

# install etcd
sudo pacman -Sy go 
mkdir pkg && cd pkg
git clone https://aur.archlinux.org/etcd.git
cd etcd
makepkg 
sudo pacman -U etcd-.*.pkg.tar.zst 
cd ../..

# install necessary python modules
# sudo pip makes sure to install the necessary Python modules system-wide.
# !!! DOUBLE check to mention same dependencies in $app/docker/Dockerfile
sudo pip3 install kubernetes psutil flask  



# Flask Workload
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

# init and start cluster

sudo systemctl enable kubelet && sudo systemctl start kubelet
sudo systemctl enable docker  && sudo systemctl start docker 
sudo groupadd docker kube  # this may fail, since the groups are created at installation 
sudo usermod -a -G docker,kube $USER
mkdir -p ~/.kube
sudo cp -i /etc/kubernetes/admin.conf ~/.kube/config
sudo chown :kube ~/.kube/config
sudo chmod chmod g+rw .kube/config

# !!! I had to ignore the usual kubernetes recommendations due to my crappy, 
# tiny EC2 instance. This should not happen in production. 
sudo kubeadm init --pod-network-cidr=10.10.0.0/16 --ignore-preflight-errors=NumCPU,Mem
