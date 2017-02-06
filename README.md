# Compilation avec Cmake et projet Clion

Instructions et note concernant l'utilisation de cmake pour générer le fichier binaire
pour flasher le stm32f407.

## Crosscompilation avec Cmake

### Générer les informations de compilation
Le projet est géré avec un cmake et un toolchain file.
Pour générer correctement les informations de compilation, il faut passer la définition
`-DCMAKE_TOOLCHAIN_FILE=arm-none-toolchain.cmake`
à la commande cmake.


### Toolchain et emplacement
(https://launchpad.net/gcc-arm-embedded)
La toolchain arm-none-eabi est utilisé et la configuration s'attend à ce qu'elle soit
installée dans les chemins standards:

-/usr/bin/arm-none-eabi-*
-/usr/arm-none-eabi


### Firmware

Le firmware peut être téléchargé à l'adresse suivante (nécessite de se connecter ou de fournir une adresse courriel valide)
https://my.st.com/content/my_st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32-standard-peripheral-libraries-expansions/stsw-stm32068.html

Déployer les fichiers sous: `/opt/stm32` (ce qui devrait donner _/opt/stm32/STM32F4-Discovery_FW_V1.1.0_)


### ST-Util

st-util est utilisé pour flasher le stm32f407 et démarrer un serveur de deboggage gdb
https://github.com/texane/stlink
(un paquet devrait exister pour les distro linux majeur et un binaire 32 bits et 64 bits existe pour windows)


### Make

Un makefile utilitaire est utilisé, celui-ci encapsule les tâches de flash et de démarrer le serveur de débogage


## Clion

1. Créer un nouveau projet en pointant sur le dossier design3/mcu
2. Créer le projet à partir de sources existantes
3. La console de Clion va avertir d'une erreur en tentant de générer les informations de compilation, ceci est **normale**
4. Aller dans file -> settings -> build, execution, deployment -> cmake | et modifier le champ "Cmake options"
5. `-DCMAKE_TOOLCHAIN_FILE=arm-none-toolchain.cmake`
6. supprimer le dossier _cmake-build-debug_ et tools -> cmake -> reset cache and reload project

Après ça, Clion devrait générer correctement les informations de compilation.


### Plugin Makefile

file -> settings -> plugins -> browse repository | chercher makefile et installer le plugin "Makefile support"


### Ajout de run configuration

run -> edit configurations
1. ajouter une nouvelle configuration "application", `target: design3-mcu.bin`
2. NB: cette run configuration ne peut s'exécuter puisqu'on produit un exécutable pour armv7, on l'ajoute pour l'utiliser
    comme pré-requis
3. ajouter une nouvelle configuration "makefile", pointer le fichier Makefile et choisir comme target "flash"
4. mettre en dépendance dans cette run configuration "design3-mcu.bin"
5. ajouter une nouvelle configuration "makefile", choisir comme target "debug"
6. ajouter une nouvelle configuration "gdb remote debug", cibler l'executable arm-none-eabi-gdb, préciser comme sysroot
    `/usr/arm-none-eabi` et comme fichier de symbole `cmake-build-debug/design3-mcu.elf`, mettre une dépendance sur la configuration
    makefile debug

La configuration makefile flash permet de flasher un stm32f407 s'il est connecté, et la configuration gdb remote debug
permet de lancer une session de débogage.
Les breakpoints fonctionnent correctement, ainsi que l'exécution d'expression arbitraire (alt+f8).
NB: lorsqu'on flash, la sortie dans la console est écrite en rouge.
TODO: voir s'il est possible d'ajouter les tâches externe dans le Cmake
