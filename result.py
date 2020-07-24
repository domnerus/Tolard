import json
import os
import subprocess
import requests
import time

# procitaj config files

with open('config_0.json', 'r') as config_0:
    data_0 = config_0.read()

with open('config_1.json', 'r') as config_1:
    data_1 = config_1.read()

with open('config_2.json', 'r') as config_2:
    data_2 = config_2.read()

with open('config_3.json', 'r') as config_3:
    data_3 = config_3.read()

# parse config files
file_0 = json.loads(data_0)
file_1 = json.loads(data_1)
file_2 = json.loads(data_2)
file_3 = json.loads(data_3)

# putanja do foldera
leveldb_dir_0 = file_0['MasterNodeConfig']['leveldb_dir']
evm_state_dir_0 = file_0['MasterNodeConfig']['evm_state_dir']
# print(leveldb_dir_0)
# print(evm_state_dir_0)

leveldb_dir_1 = file_1['MasterNodeConfig']['leveldb_dir']
evm_state_dir_1 = file_1['MasterNodeConfig']['evm_state_dir']
# print(leveldb_dir_1)
# print(evm_state_dir_1)

leveldb_dir_2 = file_2['MasterNodeConfig']['leveldb_dir']
evm_state_dir_2 = file_2['MasterNodeConfig']['evm_state_dir']
# print(leveldb_dir_2)
# print(evm_state_dir_2)

leveldb_dir_3 = file_3['MasterNodeConfig']['leveldb_dir']
evm_state_dir_3 = file_3['MasterNodeConfig']['evm_state_dir']
# print(leveldb_dir_3)
# print(evm_state_dir_3)

###
# 1. Kreirati direktorije za baze podataka za svaki node
###

if not os.path.exists(leveldb_dir_0):
    os.makedirs(leveldb_dir_0)
    # print("Directory " , leveldb_dir_0 ,  " Created ")

if not os.path.exists(leveldb_dir_1):
    os.makedirs(leveldb_dir_1)
    # print("Directory " , leveldb_dir_1 ,  " Created ")

if not os.path.exists(leveldb_dir_2):
    os.makedirs(leveldb_dir_2)
    # print("Directory " , leveldb_dir_2 ,  " Created ")

if not os.path.exists(leveldb_dir_3):
    os.makedirs(leveldb_dir_3)
    # print("Directory " , leveldb_dir_3 ,  " Created ")

if not os.path.exists(evm_state_dir_0):
    os.makedirs(evm_state_dir_0)
    # print("Directory " , evm_state_dir_0 ,  " Created ")

if not os.path.exists(evm_state_dir_1):
    os.makedirs(evm_state_dir_1)
    # print("Directory " , evm_state_dir_1 ,  " Created ")

if not os.path.exists(evm_state_dir_2):
    os.makedirs(evm_state_dir_2)
    # print("Directory " , evm_state_dir_2 ,  " Created ")

if not os.path.exists(evm_state_dir_3):
    os.makedirs(evm_state_dir_3)
    # print("Directory " , evm_state_dir_3 ,  " Created ")

###
# 2. Pokrenuti cijelu mrežu (4 nodea) tako da se pokrene jedan po jedan node koristeći priložene konfiguracije i tolard aplikaciju
# tolard binary mora biti u PATHU i executable
###

p0 = subprocess.Popen(['tolard', '--config_path', 'config_0.json'], close_fds=True)
# print(p0.pid)
p1 = subprocess.Popen(['tolard', '--config_path', 'config_1.json'], close_fds=True)
# print(p1.pid)
p2 = subprocess.Popen(['tolard', '--config_path', 'config_2.json'], close_fds=True)
# print(p2.pid)
p3 = subprocess.Popen(['tolard', '--config_path', 'config_3.json'], close_fds=True)
# print(p3.pid)

# Pricekati par sekundi da se sve pokrene (Fixing problem: ConnectionRefusedError: [Errno 61] Connection refused)
time.sleep(5.0)

# urls za svaki node koji se provjerava sa curl - MasterNodeConfig.Peer.PrometheusPullConfig
node_url_ip_0 = file_0['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['ip_address']
node_url_port_0 = file_0['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['port']
node_url_path_0 = file_0['MasterNodeConfig']['Peer']['PrometheusPullConfig']['url_path']
node_url_0 = 'http://' + node_url_ip_0 + ':' + node_url_port_0 + node_url_path_0
# print(node_url_0)

node_url_ip_1 = file_1['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['ip_address']
node_url_port_1 = file_1['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['port']
node_url_path_1 = file_1['MasterNodeConfig']['Peer']['PrometheusPullConfig']['url_path']
node_url_1 = 'http://' + node_url_ip_1 + ':' + node_url_port_1 + node_url_path_1
# print(node_url_1)

node_url_ip_2 = file_2['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['ip_address']
node_url_port_2 = file_2['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['port']
node_url_path_2 = file_2['MasterNodeConfig']['Peer']['PrometheusPullConfig']['url_path']
node_url_2 = 'http://' + node_url_ip_2 + ':' + node_url_port_2 + node_url_path_2
# print(node_url_2)

node_url_ip_3 = file_3['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['ip_address']
node_url_port_3 = file_3['MasterNodeConfig']['Peer']['PrometheusPullConfig']['access_endpoint']['port']
node_url_path_3 = file_3['MasterNodeConfig']['Peer']['PrometheusPullConfig']['url_path']
node_url_3 = 'http://' + node_url_ip_3 + ':' + node_url_port_3 + node_url_path_3
# print(node_url_3)

# HTTP GET URL & pocetne vrijednosti tolar_total_blocks
resp0 = requests.get(node_url_0)
resp1 = requests.get(node_url_1)
resp2 = requests.get(node_url_2)
resp3 = requests.get(node_url_3)

###
# 3. Zapamtiti vrijednost metrike tolar_total_blocks na svim nodovima
###

ttb_0_init = resp0.text.find("tolar_total_blocks")
ttb_1_init = resp1.text.find("tolar_total_blocks")
ttb_2_init = resp2.text.find("tolar_total_blocks")
ttb_3_init = resp3.text.find("tolar_total_blocks")

print("Tolar total blocks node 0 init ", ttb_0_init)
print("Tolar total blocks node 1 init ", ttb_1_init)
print("Tolar total blocks node 2 init ", ttb_2_init)
print("Tolar total blocks node 3 init ", ttb_3_init)

###
# 4. Pustiti mrežu da radi 10s
###

time.sleep(5.0)  #odbiti pocetnih 5 sekundi

# cekati 10 sekundi
print("10 seconds run")

resp0_10 = requests.get(node_url_0)
resp1_10 = requests.get(node_url_1)
resp2_10 = requests.get(node_url_2)
resp3_10 = requests.get(node_url_3)

###
# 5. Ponovno provjeriti vrijednost metrike tolar_total_blocks na svim nodeovima te usporediti s prethodnom vrijednosti (trenutna vrijednost bi trebala biti znatno veća)
###
ttb_0_10s = resp0_10.text.find("tolar_total_blocks")
ttb_1_10s = resp1_10.text.find("tolar_total_blocks")
ttb_2_10s = resp2_10.text.find("tolar_total_blocks")
ttb_3_10s = resp3_10.text.find("tolar_total_blocks")

print("Tolar total blocks node 0 after 10 seconds ", ttb_0_10s, "TEST", ('FAILED!', 'PASSED!')[ttb_0_init < ttb_0_10s])
print("Tolar total blocks node 1 after 10 seconds ", ttb_1_10s, "TEST", ('FAILED!', 'PASSED!')[ttb_1_init < ttb_1_10s])
print("Tolar total blocks node 2 after 10 seconds ", ttb_2_10s, "TEST", ('FAILED!', 'PASSED!')[ttb_2_init < ttb_2_10s])
print("Tolar total blocks node 3 after 10 seconds ", ttb_3_10s, "TEST", ('FAILED!', 'PASSED!')[ttb_3_init < ttb_3_10s])

###
# 6. Zaustaviti (prisilno ugasiti) jedan node po izboru - ugasi node 0
###
p0.terminate()
print("Node 0 killed")

###
# 7. Zapamtiti vrijednost metrike tolar_total_blocks na preostalim nodeovima
###
resp1_10_v2 = requests.get(node_url_1)
resp2_10_v2 = requests.get(node_url_2)
resp3_10_v2 = requests.get(node_url_3)

ttb_1_10s_v2 = resp1_10_v2.text.find("tolar_total_blocks")
ttb_2_10s_v2 = resp2_10_v2.text.find("tolar_total_blocks")
ttb_3_10s_v2 = resp3_10_v2.text.find("tolar_total_blocks")

# print("Tolar total blocks node 1 after 10 seconds + 0 killed ", ttb_1_10s_v2)
# print("Tolar total blocks node 2 after 10 seconds + 0 killed ", ttb_2_10s_v2)
# print("Tolar total blocks node 3 after 10 seconds + 0 killed ", ttb_3_10s_v2)

###
# 8. Pustiti mrežu da radi 10s
###

time.sleep(10.0)

print("20 seconds run")

resp1_20 = requests.get(node_url_1)
resp2_20 = requests.get(node_url_2)
resp3_20 = requests.get(node_url_3)

ttb_1_20s = resp1_20.text.find("tolar_total_blocks")
ttb_2_20s = resp2_20.text.find("tolar_total_blocks")
ttb_3_20s = resp3_20.text.find("tolar_total_blocks")

###
# 9. Provjeriti vrijednost metrike tolar_total_blocks na preostala 3 nodea i potvrditi da se vrijednost ponovno povećala
###
print("Tolar total blocks node 1 after 20 seconds ", ttb_1_20s, "TEST", ('FAILED!', 'PASSED!')[ttb_1_10s_v2 < ttb_1_20s])
print("Tolar total blocks node 2 after 20 seconds ", ttb_2_20s, "TEST", ('FAILED!', 'PASSED!')[ttb_2_10s_v2 < ttb_2_20s])
print("Tolar total blocks node 3 after 20 seconds ", ttb_3_20s, "TEST", ('FAILED!', 'PASSED!')[ttb_3_10s_v2 < ttb_3_20s])

###
# 10.Zaustaviti (prisilno ugasiti) još jedan node po izboru - ugasi node 1
###
p1.terminate()
print("Node 1 killed")

###
# 11.Zapamtiti vrijednost metrike tolar_total_blocks na preostalim nodeovima
# 12.Pustiti mrežu da radi 10s
###
time.sleep(10.0)
print("30 seconds run")

resp2_30 = requests.get(node_url_2)
resp3_30 = requests.get(node_url_3)

ttb_2_30s = resp2_30.text.find("tolar_total_blocks")
ttb_3_30s = resp3_30.text.find("tolar_total_blocks")

###
# 13.Provjeriti vrijednost metrike tolar_total_blocks na preostala 2 nodea i potvrditi da se vrijednost nije povećala
###
# USPOREDITI e.g. ttb_3_30s &&  ttb_3_20s
print("Tolar total blocks node 2 after 30 seconds ", ttb_2_30s, "TEST", ('FAILED!', 'PASSED!')[ttb_2_20s == ttb_2_30s])
print("Tolar total blocks node 3 after 30 seconds ", ttb_3_30s, "TEST", ('FAILED!', 'PASSED!')[ttb_3_20s == ttb_3_30s])

###
# 14.Ugasiti ostale nodeove i završiti integracijski test s prikladnom porukom o rezultatu testa (koje provjere su ispravno prošle, a koje nisu)
###
p2.terminate()
p3.terminate()
print("Tolar test end.")