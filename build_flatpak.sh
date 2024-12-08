#!/bin/bash

# Install Flatpak and Flatpak Builder
sudo apt-get update
sudo apt-get install -y flatpak flatpak-builder

# Add Flathub repository
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Build the Flatpak
flatpak-builder --force-clean build-dir net.sytes.brpxd.DockerBackup.yml
flatpak-builder --repo=repo build-dir net.sytes.brpxd.DockerBackup.yml
flatpak build-bundle repo docker_backup.flatpak net.sytes.brpxd.DockerBackup
