

# install docker, dockerd
sudo pacman -Sy docker ethtool wget unzip containerd
# install kubernetes
sudo pacman -Sy kubectl kubernetes-control-plane kubernetes-node 
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
mkdir -p ~/Src/pyku && cd ~/Src/pyku 
git clone https://github.com/JasonHaley/hello-python.git


