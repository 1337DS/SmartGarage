import paramiko

def start():
  host = "192.168.0.113"
  port = 22
  username = "pi"
  password = "SmartGarage"
  
  command = 'export DISPLAY=:0 ; vlc "/home/pi/garage/garage_zu.mp4" --quiet --fullscreen'
  
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(host, port, username, password)
  print("start1")
  stdin, stdout, stderr = ssh.exec_command(command)
  print("start2")
  stdout.channel.set_combine_stderr(True)
  print("start3")
  #output = stdout.readlines()
  print("start4")
if __name__ == "__main__":
  start()
