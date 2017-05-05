#!/usr/bin/env bash

# Install all the dependencies
sudo apt-get install git dconf-cli tmux vim build_essential cmake \
    python-dev python3-dev exuberant-ctags

# Install vim-plug
# This is already taken care of in the vimrc, but uncomment the following
# lines to do it in advance
# curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
#     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# Install Ubuntu Mono
mkdir ~/.fonts
git clone https://github.com/pdf/ubuntu-mono-powerline-ttf.git \
    ~/.fonts/ubuntu-mono-powerline-ttf
fc-cache -vf

# Install Solarized on the current GNOME profile
git clone https://github.com/Anthony25/gnome-terminal-colors-solarized.git
cd gnome-terminal-colors-solarized
./install.sh

# Install ripgrep 0.5.1
curl -fLO 'https://github.com/BurntSushi/ripgrep/releases/download/0.5.1/ripgrep-0.5.1-x86_64-unknown-linux-musl.tar.gz'
tar -zxvf ripgrep-0.5.1-x86_64-unknown-linux-musl.tar.gz
cp ripgrep-0.5.1-x86_64-unknown-linux-musl/rg /usr/bin

# Copy config files to the home directory
cp ./vimrc ~/.vimrc
cp ./tmux.conf ~/.tmux.conf

# Install all of the plugins using vim-plug
vim +PlugInstall
