#!/usr/bin/env bash

# Install all the dependencies
sudo apt-get install git dconf-cli tmux vim

# Install Vundle
git clone https://github.com/VundleVim/Vundle.vim ~/.vim/bundle/Vundle.vim

# Install Ubuntu Mono
mkdir ~/.fonts
git clone https://github.com/pdf/ubuntu-mono-powerline-ttf.git ~/.fonts/ubuntu-mono-powerline-ttf
fc-cache -vf

# Install Solarized on the current GNOME profile
git clone https://github.com/Anthony25/gnome-terminal-colors-solarized.git
cd gnome-terminal-colors-solarized
./install.sh

# Copy config files to the home directory
cp ./vimrc ~/.vimrc
cp ./tmux.conf ~/.tmux.conf

# Install all of the plugins using Vundle
vim +PluginInstall
