# Tolard
Unit testing of nodes written in Python
Zadatak – QA

Tolar HashNet je distribuirana mreža nodeova koji na decentralizirani način izvršavaju
određene zadatke koji dolaze od strane korisnika. Svaki node u mreži je u stanju
verificirati rezultat izvršavanja zadataka te biti siguran da su ostali nodeovi došli do istog
rezultata. Verifikaciju osigurava algoritam koji omogućuje da su svi rezultati izvršavanja
zadataka na svim nodeovima Tolar HashNet-a jednaki te se oni u tom obliku spremaju u
bazu podataka svakog nodea (sukladno tome njihove pojedinačne baze podataka su
ujedno i replike jedna druge).
Svrha ovog zadatka je implementirati jednostavan integracijski test koji će provjeriti da
mreža nodeva radi sukladno načelima spomenutog algoritma na način da se prate
metrike koje producira svaki od nodeova.
Svaki node bilježi metrike samo za sebe i te metrike su dostupne na određenom portu
koji stoji na raspolaganju svima koji te metrike žele čitati. Treba uzeti u obzir da svi
nodeovi međusobno komuniciraju te su metrike svakog nodea dostupne aplikacijama za
testiranje kao što je prikazano na sljedećoj shemi:

Upute za pokretanje lokalne Tolar HashNet mreže
U sklopu zadatka nužno je pridržavati se navedenih uputa za pokretanje Tolar HashNet
mreže jer su one neophodne da bi se implementirao korektni integracijski test.
Uz tekst zadatka priložena je tolard aplikacija s kojom je moguće pokrenuti jedan node
na način da se eksplicitno kroz argumente aplikacije preda put do konfiguracije tog
pojedinačnog nodea. Svaki node ima svoju konfiguraciju jer se razlikuju portovi, gdje su
locirane baze podataka itd.

Prije pokretanja mreže potrebno je kreirati direktorije za baze podataka za svaki
pojedinačni node, direktoriji su definirani u svakoj konfiguraciji pod sljedećim JSON
poljima:
"leveldb_dir": "/tmp/db/MasterNode_0",
"evm_state_dir": "/tmp/evm_db/MasterNode_0"
Naravno, ovo su unaprijed postavljene vrijednosti koje se mogu po potrebi podesiti u
konfiguracijama ukoliko je potrebno.
Zatim je moguće pokrenuti mrežu od ukupno 4 nodea na način da se koriste priložene
konfiguracije: config_0.json, config_1.json, config_2.json, config_3.json
Svaki node se pokreće pojedinačno sa svojom konfiguracijom kao odvojeni proces:
./tolard --config_path config_0.json
Ukoliko se pojave bilo kakvi problemi, baze podataka je moguće obrisati tako da se
obriše sadržaj njihovih direktorija te se mreža pokrene ispočetka (clean start).
Ostale postavke u konfiguraciji nije preporučljivo mijenjati, ali ukoliko se za to ukaže
potreba, treba samo uzeti u obzir da se sve promjene u jednoj konfiguraciji propagiraju
kroz sve ostale jer konfiguracija pojedinačnog nodea ujedno sadržava i informacije o
ostalim nodeovima u mreži (NetworkConfiguration.seeds). Postavke pojedinačnog
nodea se nalaze definirane u MasterNodeConfig polju unutar konfiguracije tog nodea.
Upute za implementaciju integracijskog testa
Odabir jezika, tehnologije, alata i ostalog za potrebe implementacije integracijskog testa
je prepušteno kandidatu na odabir. Poželjno je odabrati nešto s čim kandidat ima najviše
iskustva i znanja. Ideja zadatka nije ispitivanje poznavanja nekog jezika/tehnologije nego
samo želimo vidjeti kako netko pristupa problemu s kojim se susreće.
Zadatak je promatrati metrike na svim nodeovima dok je mreža pokrenuta te bi
integracijski test trebao biti u stanju ispitati što se događa s određenom metrikom dok je
mreža pokrenuta te što se dogodi nakon što se određeni broj nodeova prisilno ugasi.
Kao priprema, prvo je potrebno zaviriti u konfiguracije nodeova (točnije pod
MasterNodeConfig.Peer.PrometheusPullConfig) gdje se nalazi sljedeći podatak:
"PrometheusPullConfig": {
"bind_endpoint": {
"ip_address": "127.0.0.1",
"port": "9500"
},
"access_endpoint": {
"ip_address": "127.0.0.1",
"port": "9500"
},

"url_path": "\/metrics"
}
Ovo govori na koji se HTTP endpoint moguće spojiti da bi se pročitale metrike koje je
spremio taj konkretni node, odnosno točnije endpoint izgleda ovako:
http://127.0.0.1:9500/metrics
Pomoću HTTP GET requesta moguće je dohvatiti sve metrike za taj node u ovom
trenutku, npr. pomoću curl naredbe:
curl -XGET http://localhost:9500/metrics
Rezultat izgleda poprilično glomazno (ovo je samo isječak od svega što se nudi pod
metrikama):
# HELP exposer_bytes_transferred bytesTransferred to metrics services
# TYPE exposer_bytes_transferred counter
exposer_bytes_transferred 71528.000000
# HELP exposer_total_scrapes Number of times metrics were scraped
# TYPE exposer_total_scrapes counter
exposer_total_scrapes 3.000000
# HELP exposer_request_latencies Latencies of serving scrape requests, in microseconds
# TYPE exposer_request_latencies summary
exposer_request_latencies_count 3
exposer_request_latencies_sum 28575.000000
exposer_request_latencies{quantile="0.500000"} 5993.000000
exposer_request_latencies{quantile="0.900000"} 10666.000000
exposer_request_latencies{quantile="0.990000"} 10666.000000
# TYPE tolar_events_count counter
tolar_events_count 0.000000
# TYPE tolar_transactions_count counter
tolar_transactions_count 0.000000
# TYPE tolar_rejected_events_count counter
tolar_rejected_events_count 0.000000
# TYPE tolar_rejected_transactions_count
counter tolar_rejected_transactions_count 0.000000
# TYPE tolar_agreed_events_count counter
tolar_agreed_events_count 0.000000

Ideja je koncentrirati se samo na jednu određenu metriku, a to je
tolar_total_blocks. Samo nju je potrebno ispitati u integracijskom testu.
Scenarij za integacijski test
Integracijski test bi se trebao odvijati sukladno sljedećem testnom scenariju:
1. Kreirati direktorije za baze podataka za svaki node (ili obrisati postojeće)
2. Pokrenuti cijelu mrežu (4 nodea) tako da se pokrene jedan po jedan node koristeći
priložene konfiguracije i tolard aplikaciju
3. Zapamtiti vrijednost metrike tolar_total_blocks na svim nodeovima
4. Pustiti mrežu da radi 10s
5. Ponovno provjeriti vrijednost metrike tolar_total_blocks na svim nodeovima
te usporediti s prethodnom vrijednosti (trenutna vrijednost bi trebala biti znatno
veća)
6. Zaustaviti (prisilno ugasiti) jedan node po izboru
7. Zapamtiti vrijednost metrike tolar_total_blocks na preostalim nodeovima
8. Pustiti mrežu da radi 10s
9. Provjeriti vrijednost metrike tolar_total_blocks na preostala 3 nodea i
potvrditi da se vrijednost ponovno povećala
10.Zaustaviti (prisilno ugasiti) još jedan node po izboru
11.Zapamtiti vrijednost metrike tolar_total_blocks na preostalim nodeovima
12.Pustiti mrežu da radi 10s
13.Provjeriti vrijednost metrike tolar_total_blocks na preostala 2 nodea i
potvrditi da se vrijednost nije povećala
14.Ugasiti ostale nodeove i završiti integracijski test s prikladnom porukom o
rezultatu testa (koje provjere su ispravno prošle, a koje nisu)

End
