

# install docker, dockerd
sudo pacman -S docker ethtool wget unzip containerd
# install kubernetes
sudo pacman -S kubectl kubernetes-control-plane kubernetes-node containerd

# install etcd
sudo pacman -S go 
mkdir ~/pkg
git clone https://aur.archlinux.org/etcd.git
cd etcd
makepkg 
sudo pacman -U etcd-.*.pkg.tar.zst 



# Flask Workload
mkdir -p ~/Src/pyku && cd ~/Src/pyku 
git clone https://github.com/JasonHaley/hello-python.git



