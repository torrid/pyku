

# install docker, dockerd
sudo pacman -Sy docker ethtool wget unzip containerd
# install kubernetes
sudo pacman -Sy kubectl kubernetes-control-plane kubernetes-node 
# install python/pip
sudo pacman -Sy python-pip

# install etcd
sudo pacman -Sy go 
mkdir pkg && cd pkg
git clone https://aur.archlinux.org/etcd.git
cd etcd
makepkg 
sudo pacman -U etcd-.*.pkg.tar.zst 
cd ../..

# misc stuff 
sudo pacman -Sy stress 

# install necessary python modules
pip3 install kubernetes psutil flask  


# Flask Workload
mkdir -p ~/Src/pyku && cd ~/Src/pyku 
git clone https://github.com/JasonHaley/hello-python.git

