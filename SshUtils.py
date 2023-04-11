#send info to RPi
import paramiko

def ssh_rpi(host, username, password, remote_script_path):
    # Set the command to run on the Raspberry Pi
    remote_command = f"python {remote_script_path}"

    # Create a new SSH client and connect to the Raspberry Pi
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=username, password=password)
    print("connected to Raspberry Pi")
    print("feeding...")

    # Run the command on the Raspberry Pi
    stdin, stdout, stderr = ssh.exec_command(remote_command)

    print("feeding done.")

    # Print the output of the command
    for line in stdout:
        print(line.strip())

    # Close the SSH connection
    ssh.close()

