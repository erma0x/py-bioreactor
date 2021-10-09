# Bioreactor backend software
In Development: IoT and microbiology with Python, Raspberry and Arduino for a self-controlled system for the growth of microorganisms 


Scarico in contemporanea

strumentazione
	elettrovalvole
	timer
	rele'/transistor

nutrienti
	CO2
	Peptoni, zucchero, lipidi
	Acqua sterilizzata 30min

DB
	tempo
	quantita'

OD
	DB
		valore OD
		tempo misura
		colonna
	strumentazione
		laser
		fotoresistenza

Salinita'
	strumentazione
		2 elettrovalvole
		timer
	DB
		valore 
		tempo misura
		colonna

pH
	DB
		valore ph
		tempo misura
		colonna
	strumentazione
		Phaccamentro
		transistor

temperatura
	strumentazione
		fascia riscaldante
		cella di Peltie'
		termometro

lettura temperatura
	termometro
	DB
		valore
		tempo
		colonna

reservoir
	strumentazione
		elettrovalvola
	DB
		tempo
		quantita'

aria
	strumentazione
		elettrovalvola
		pompa peristalsica per l'aria
	DB
		intensita'
		tempo ciclo on/off
