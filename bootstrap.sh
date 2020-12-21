#!/bin/bash

read -r -p "Install system packages? [y/N] " response
case "$response" in
  [yY])
    # System packages
    sudo apt-get update
    # sudo apt-get install --assume-yes nginx docker docker-compose dnsutils python-minimal python-pip g++ make
    sudo apt-get install --assume-yes dnsutils python-minimal python-pip make

    ;;
  *)
    ;;
esac

# Personal configuration
cd ~
if [ ! -d ~/dotfiles ]; then
    git clone https://github.com/keyan/dotfiles.git
    pushd dotfiles/
    ./install && popd
fi
