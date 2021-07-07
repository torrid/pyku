This source installs and configures a (local) kubernetes cluster from scratch,
and deploys a Python/Flask workload onto *n* nodes, providing a way to create and
measure CPU load on them.  

The purpose of this rather academic project is to get into K8s and to learn how
to communicate with the Pods/Deployment. 

Since I had to start somewhere, I assume a regular Linux user with sudo/root
access, and the group names "kube" and "docker" for the respective services.

### Notes
I got stuck in the Routing and Proxying realm of K8s, so the Loadbalancer
Deployment doesn't work yet and the fun part begins only there: Do statistics
over different scenarios and – ultimately – provide fancy graphics! 

Usually one would use the "stress" cmdline tool for this kind of scenario, but
I resorted to some simple Float arithmetics for now.

I also had to considerably upgrade my host on AWS:
Kubernetes, even Minikube just doesn't run nicely on 1 vcore, with never-enough
RAM, and it wouldn't provide useful data anyway. On the bright side, vertically
scaling MyLittleEC2 instance was *really* easy. 

The stress method returns only after $STRESSTIME seconds, which is braindead.
I'd solve that with fork/SIGALARM IPC, if I had the time. 

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
### Install required python modules
```bash
sudo pip install -r requirements.txt
```
Doing sudo pip makes sure to install the necessary Python modules system-wide. 
(Only needed for locally testing main.py.)


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
| Url | Description | Output 
| --- | --- | --- 
| /stress | Create CPU load for 60 seconds. | hostname, seconds
| /cpu | Return LoadAverage (psutil.getloadavg()[0]) | hostname, load
| /insight | Environment of the current pod/process. | environment


### Install Workload on Docker and Kubernetes
```bash 
docker image rm load-and-stress
docker build -f Dockerfile -t load-and-stress:latest . 
minikube start
eval $(minikube docker-env) 
kubectl delete deployment --all 
kubectl apply -f deployment.yaml
kubectl replace --force -f deployment.yaml 
# kubectl expose deployment load-and-stress --type=LoadBalancer --port=8080
minikube tunnel > /dev/null 2>&1 & 
minikube proxy >/dev/null 2>&1 &
kubectl get svc
url=$(kubectl get svc|grep load-and-stress|grep 8080| sed -e 's#  *#\t#gi'| cut -f 4,5 | cut -f 1 -d:| sed -e 's#\t#:#')
echo "http://${url}/"
```


### Links 
 * [Minikube](https://minikube.sigs.k8s.io/docs/handbook/)
 * [Flask](https://flask.palletsprojects.com/en/2.0.x/)
 * [Python on Kubernetes](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)
