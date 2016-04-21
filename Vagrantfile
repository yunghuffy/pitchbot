# -*- mode: ruby -*-
# vi: set ft=ruby :

root_bootstrap = <<-EOF
  apt-get update
  apt-get install -y git make python python-dev python-pip libffi-dev python-lxml
  pip install -U pip
  hash -r
  pip install virtualenv
  pip install mlbgame
  pip install slackbot
  pip install slackclient
EOF


Vagrant.configure(2) do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.provision :shell, inline: root_bootstrap
end
