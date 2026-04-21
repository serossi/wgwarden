# wgwarden
Offline Wireguard mesh config Manager

Sunday Morning Vibecoded tool, but it works.

## What is this for ?
(re)generate mesh or partial Mesh (hybrid) configs for your wireguard Peers.
When you want static relyable config without any overhead and just plain wireguard, yet also dont wanna deal
manually with updating every peer and keep track on allowlists

Features: 
-Portable in Nature
-Simpel Storage in a Json file in the same directory as your executeable
-Any changes in Peerlist will instant reflect on the other peer
-Can Generate Valid Wireguard Keypairs if needed
-Can store Multiple different WGNetworks at once
-Very simple pro and con - it will NOT check IP overlaps etc... this is on purpose to allow you to have 2 Peers with similar config
-very lightweight, but Keep in ming, our json is not encrypted, keep it secure

<img width="1153" height="934" alt="image" src="https://github.com/user-attachments/assets/b262f1af-14a0-491f-98a5-826e8073c0de" />


## How to use:
Simply enter a Wireguard config but instead of an allow list we define
-a local Network list (that will then be used as allow List for connected Peers)
-a Peerlist - here we define which Peers are allowed to connect to the current Peer

Simply add multiple Peers, their Networks, and their Partners
You can freely choose which peer is allowed to which peer. 

After that click on each peer and either export via QR Code / via File / or Copy Paste
The configuration will be generated at this point based on Peer list and each Peer local Network

Yes you can Store multiple different WG Networks within one file. 
Only if a peer is linked to another it will affect that config. 

Copy a config: simple Rename a config you whish to copy. 
The you will get a new one with the new Name the old stays in Place.
yes, to rename and not copy you need to delete the old File, call it a feature, call it a bug, its how it works. 

Update config: Update Data on the Peer in question (or add a new one), after saving the changes, simply export the config of all affected
Peers
