import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def backup_docker_images():
    # Get the output folder from the user
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    # Clear the terminal panel
    terminal_panel.delete(1.0, tk.END)

    # Execute `docker images` to get the list of images
    result = subprocess.run(['docker', 'images', '--format', '{{.Repository}} {{.Tag}} {{.ID}}'], capture_output=True, text=True)
    if result.returncode != 0:
        messagebox.showerror("Error", f"Failed to get Docker images: {result.stderr}")
        return

    # Parse the output
    images = result.stdout.strip().split('\n')
    for image in images:
        parts = image.split()
        if len(parts) == 3:
            repository, tag, image_id = parts
            # Format the filename
            filename = f"{repository.replace('/', '_').replace('.', '_')}-{tag.replace('.', '_')}_{image_id}.tar"
            filepath = os.path.join(output_folder, filename)

            # Log the start of the save process
            log_message(f"Saving {repository}:{tag} to {filepath}")

            # Execute `docker save` to create the backup
            save_command = ['docker', 'save', '-o', filepath, f"{repository}:{tag}"]
            save_result = subprocess.run(save_command, capture_output=True, text=True)
            if save_result.returncode != 0:
                log_message(f"Failed to save image {repository}:{tag}: {save_result.stderr}")
            else:
                log_message(f"Saved {repository}:{tag} to {filepath}")

    log_message("Backup process completed.")

def log_message(message):
    terminal_panel.insert(tk.END, message + "\n")
    terminal_panel.see(tk.END)  # Scroll to the end

# Create the main window
root = tk.Tk()
root.title("Docker Image Backup Tool")

# Create a terminal panel
terminal_panel = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, bg='black', fg='white')
terminal_panel.pack(pady=10)

# Create a button to trigger the backup process
backup_button = tk.Button(root, text="Backup Docker Images", command=backup_docker_images)
backup_button.pack(pady=20)

# Run the application
root.mainloop()
