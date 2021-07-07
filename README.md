This source installs and configures a (local) kubernetes cluster from scratch,
and deploys a Python/Flask workload onto 2 nodes, providing a way to create and
measure CPU load on them.  

The purpose of this rather academic project is to get into K8s and to learn how
to communicate with the nodes. 

Since I had to start somewhere, I assume a regular Linux user with sudo/root
access, and the group names "kube" and "docker" for the respective services.
*Works on my machine™* (Arch linux t3.small EC2 instance). 

### Install docker, dockerd, kubernetes, pip, the stress cmdline tool
```bash
sudo pacman -Sy docker ethtool wget unzip containerd
sudo pacman -Sy minikube
sudo pacman -Sy python-pip
```

### Install etcd from AUR (https://aur.archlinux.org/etcd.git)
```bash
sudo pacman -Sy go 
mkdir pkg && cd pkg
git clone https://aur.archlinux.org/etcd.git
cd etcd
makepkg 
sudo pacman -U etcd-.*.pkg.tar.zst 
cd ../..
```
### Install necessary python modules
(Doing sudo pip makes sure to install the necessary Python modules system-wide.)
```bash
sudo pip install -r requirements.txt
```


### Flask Workload
This was taken from https://github.com/JasonHaley/hello-python.git, and
extended by the CPU stressing and Load Average functions.
```
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
```

### Build and Deploy docker image
```bash
docker build -f Dockerfile -t load-and-stress:latest . 
docker run -p 5001:5000 load-and-stress
```

### Initialize Kubernetes & Deploy on Kubernetes

```bash 
docker image rm load-and-stress
docker build -f Dockerfile -t load-and-stress:latest . 
minikube start
eval $(minikube docker-env) 
kubectl apply -f deployment.yaml
kubectl replace --force -f deployment.yaml 
kubectl expose deployment load-and-stress --type=LoadBalancer --port=8080
minikube tunnel > /dev/null 2>&1 & 
url=$(kubectl get svc|grep load-and-stress|grep 8080| sed -e 's#  *#\t#gi'| cut -f 4,5 | cut -f 1 -d:| sed -e 's#\t#:#')
echo "http://${url}/"
```

### Methods

| Url | Description | Output |
| --- | --- | --- |
| /stress | Create CPU load for 60 seconds. | hostname, seconds
| /cpu | Return LoadAverage (psutil.getloadavg()[0]) | hostname, load
| /insight | Environment of the current pod/process. | environment


