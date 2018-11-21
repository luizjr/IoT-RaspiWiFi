import subprocess
import fileinput
import os
import sys


def install_prereqs():
	project_path = os.path.dirname(os.path.abspath(__file__))
	print("Atualizando Apt...")
	os.system('apt update')
	print("Instalando Pré-requisitos via Apt...")
	os.system('apt install python3 bundler libsqlite3-dev dnsmasq nodejs rpi.gpio hostapd libxml2-dev libxslt-dev -y')
	print("Instalando as Ruby Gems necessárias. Isso pode levar alguns minutos...")
	os.system('gem install nokogiri --no-document -v 1.6.6.2 -- --use-system-libraries')
	os.system('bundle install --gemfile=' + project_path + '/Configuration_App/Gemfile')

def update_config_paths():
	project_path = os.path.dirname(os.path.abspath(__file__))

	os.system('sudo cp -a Reset_Device/static_files/rc.local.aphost.template Reset_Device/static_files/rc.local.aphost')
	os.system('sudo cp -a Reset_Device/static_files/rc.local.apclient.template Reset_Device/static_files/rc.local.apclient')
	os.system('sudo cp -a Reset_Device/reset.py.template Reset_Device/reset.py')

	with fileinput.FileInput("Reset_Device/static_files/rc.local.aphost", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset_Device/static_files/rc.local.apclient", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset_Device/reset.py", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close


#################################################################
#################################################################


print()
print("#####################################")
print("##### RaspiWiFi Headless Setup  #####")
print("#####################################")
print()
print()
install_prereqs_ans = input("Você gostaria de instalar arquivos de pré-requisito (isso pode levar até 5 minutos)? (y/n): ")

if(install_prereqs_ans == 'y'):
	print()
	print("Atualizando Sistema...")
	install_prereqs()
else:
	print()
	print()
	print("===================================================")
	print("---------------------------------------------------")
	print()
	print("Nenhum pré-requisito instalado. Continuando com a instalação do arquivo de configuração...")
	print()
	print("---------------------------------------------------")
	print("===================================================")
	print()
	print()
	print()
	print()
	print()
	print()
run_setup_ans = input("Você gostaria de executar a configuração inicial do Headless RaspiWiFi? (y/n): ")

if(run_setup_ans == 'y'):
	print("Updating config files and copying them...")
	update_config_paths()

	os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf.OLD')
	os.system('sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.OLD')
	os.system('sudo rm -f ./tmp/*')
	os.system('sudo cp ./Reset_Device/static_files/dhcpcd.conf.aphost /etc/dhcpcd.conf')
	os.system('sudo cp ./Reset_Device/static_files/dnsmasq.conf /etc/dnsmasq.conf')
	os.system('sudo cp ./Reset_Device/static_files/hostapd.conf /etc/hostapd/hostapd.conf')
	os.system('sudo cp ./Reset_Device/static_files/default_hostapd /etc/default/hostapd')
	os.system('sudo cp ./Reset_Device/static_files/rc.local.aphost /etc/rc.local')
	os.system('sudo chown root.netdev /etc/dhcpcd.conf')
	os.system('sudo chmod 664 /etc/dhcpcd.conf')
	os.system('sudo chown root.root /etc/hostapd/hostapd.conf')
	os.system('sudo chmod 644 /etc/hostapd/hostapd.conf')
	os.system('sudo chown root.root /etc/dnsmasq.conf')
	os.system('sudo chmod 644 /etc/dnsmasq.conf')
	os.system('sudo chown root.root /etc/default/hostapd')
	os.system('sudo chmod 644 /etc/default/hostapd')
	os.system('sudo chown root.root /etc/rc.local')
	os.system('sudo chmod 755 /etc/rc.local')

else:
	print()
	print()
	print("===================================================")
	print("---------------------------------------------------")
	print()
	print("Configuração inicial do RaspiWiFi foi cancelada. Nenhuma alteração feita.")
	print()
	print("---------------------------------------------------")
	print("===================================================")
	print()
	print()
	sys.exit(0)

print()
print()
reboot_ans = input("A configuração inicial está completa. Uma reinicialização é necessária, você gostaria de fazer isso agora? (y/n): ")

if(run_setup_ans == 'y' and reboot_ans == 'y'):
	os.system('sudo systemctl enable dnsmasq')
	os.system('sudo systemctl enable hostapd')
	os.system('sudo reboot')
