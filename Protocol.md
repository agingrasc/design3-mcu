# Commande standards
- 0x00 -> Move
- 0x01 -> Camera
- 0x02 -> Pencil
- 0x03 -> Led

# Commande de debug
Ces commandes servent pour les tests de sanity et l'identification.
- 0xa0 -> Application PWM sur un moteur
- 0xa1 -> Lecture d'un encodeur
- 0xa2 -> Toggle le pid

# Return code 
- 0x00 -> reception OK | execution OK
- 0x10 -> header check sum FAILURE
- 0x11 -> header invalide (pas assez de bytes)
- 0x12 -> payload invalide (pas assez de bytes)
- 0x20 -> command execution FAILURE