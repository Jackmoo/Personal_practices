#! /bin/bash
#==============================================================#
#   Description:  Unixbench script                             #
#   Original credit to:                                        #
#       Author: Teddysun <i@teddysun.com>                      #
#       Intro:  https://teddysun.com/245.html                  #
#==============================================================#
cur_dir=./unixbench_src

# Check System
[[ $EUID -ne 0 ]] && echo 'Error: This script must be run as root!' && exit 1
[[ -f /etc/redhat-release ]] && os='centos'
[[ ! -z "`egrep -i debian /etc/issue`" ]] && os='debian'
[[ ! -z "`egrep -i ubuntu /etc/issue`" ]] && os='ubuntu'
[[ "$os" == '' ]] && echo 'Error: Your system is not supported to run it!' && exit 1

# Install necessary libaries
if [ "$os" == 'centos' ]; then
    yum -y install make automake gcc autoconf gcc-c++ time perl-Time-HiRes
else
    apt-get -y update
    apt-get -y install make automake gcc autoconf time perl
fi

# Create new soft download dir
mkdir -p ${cur_dir}
cd ${cur_dir}

# Download UnixBench5.1.3
<<COMMENT
if [ -s UnixBench5.1.3.tgz ]; then
    echo "UnixBench5.1.3.tgz [found]"
else
    echo "UnixBench5.1.3.tgz not found!!!download now..."
    if ! wget -c http://dl.teddysun.com/files/UnixBench5.1.3.tgz; then
        echo "Failed to download UnixBench5.1.3.tgz, please download it to ${cur_dir} directory manually and try again."
        exit 1
    fi
fi
tar -zxvf UnixBench5.1.3.tgz && rm -f UnixBench5.1.3.tgz
COMMENT

# Clone from github
git clone https://github.com/kdlucas/byte-unixbench.git
cd byte-unixbench/
cd UnixBench/

#Run unixbench
make
./Run

echo
echo
echo "======= Script description and score comparison completed! ======= "
echo
echo
