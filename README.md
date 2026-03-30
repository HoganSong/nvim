# You can download a specific version of neovim on Linux with
    curl -LO https://github.com/neovim/neovim/releases/download/v<specific version>/nvim-linux-x86_64.appimage
    chmod u+x nvim-linux-x86_64.appimage
    mv nvim-linux-x86_64.appimage ~/.local/bin/nvim
    echo 'export PATH="~/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc

If you ever want this setup don't forget to follow these two steps you dumb fuck

# 1. Clone the packer.nvim repository and install it:

> Unix, Linux Installation

    git clone --depth 1 https://github.com/wbthomason/packer.nvim\
     ~/.local/share/nvim/site/pack/packer/start/packer.nvim

> Windows Powershell Installation
    
    git clone https://github.com/wbthomason/packer.nvim "$env:LOCALAPPDATA\nvim-data\site\pack\packer\start\packer.nvim"


# 2. nvim into lua/thehogan/packer.lua and :so, :PackerSync

