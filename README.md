# password-manager
## Setup
### Install MySQL client
#### Debian 
```bash
sudo apt update
sudo apt install mariadb-server
sudo mysql_secure_installation
```
#### Arch
> Source: [Arch Wiki](https://wiki.archlinux.org/title/MariaDB)
```bash
pacman -S mariadb
mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
systemctl enable --now mariadb
mysql_secure_installation
```
#### NixOS
Add this in your `/etc/nixos/configuration.nix`
```nix
services.mysql = {
  enable = true;
  package = pkgs.mariadb;
};
```
### Configure MySQL
Login and create a new user
```bash
sudo mysql
```
```sql
CREATE USER 'passmgr'@'localhost' IDENTIFIED WITH authentication_plugin BY '<your-strong-password>';
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'passmgr'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
exit
```
### Install requirements
Install tkinter on your host
```bash
sudo apt-get install python3-tk
```
Setup python virtual environment and install other requirements
```bash
python -m venv venv
source venv/bin/activate
pip install -r requimrents.txt
```
 
#### On NixOS
```bash
nix-shell
```

## Usage
Just run the app using
```bash
python manager.py
```
And provide it the MySQL creds
