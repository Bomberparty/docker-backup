# Install PyInstaller
pip install pyinstaller

# Build the EXE
pyinstaller --onefile docker_backup.py

# Move the EXE to the desired location
Move-Item -Path "dist\docker_backup.exe" -Destination "docker_backup.exe"
