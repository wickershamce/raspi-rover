TODO
====

1. try pyliblo for faster OSC implementation and python3 compatibility
2. make a battery voltage monitor circuit for both batteries

## Git command line cheat sheet
For first commit
* git init
* git add .
* git commit -m "First commit"
* git remote add origin REMOTE_REPO_URL
* git remote -v
* git push origin master

For subsequent commits
* git pull origin master
* git add FILE_TO_COMMIT or git add .
* git commit -m "MESSAGE"
* git push origin master

motor control:
EnA     in1     in2     Out1    Out2    Motor1
LOW     X       X       Z       Z       Stop
HIGH    HIGH    LOW                     forward
HIGH    LOW     HIGH                    backward
HIGH    HIGH    HIGH    
