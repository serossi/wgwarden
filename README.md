# wgwarden
Offline Wireguard Static mesh config Manager and generator.  
Keep and update all your Wireguard configs in one Place, export (auto) updated config Files locally. 


Sunday Morning Vibecoded tool, but it works.

### What is this for ?
(re)generate Static mesh or partial Mesh (hybrid) configs for your wireguard Peers.  
When you want static relyable config without any overhead and just plain wireguard, yet also dont wanna deal  
manually with updating every peer and keep track on allowlists  

### Features:  
  - keep all your Wireguard configs in one place  
  	- freely add or remove Peer connections and update all affected peers at once  
  	- regenerate updated allow IP lists of multiple peers  
  	- export via file / copy paste / QRCode  
  	- Can Generate Valid Wireguard Keypairs if needed
    - Any changes in Peerlist will instant reflect on the other peer
      
  - Portable in Nature, Simpel Storage in a Json file in the same directory as your executeable    
  	- Can store Multiple different WGNetworks at once  
  	- Very simple pro and con - it will NOT check IP overlaps etc... this is on purpose to allow you to have 2 Peers with similar config  
  	- very lightweight, but Keep in mind, our json is not encrypted, keep it secure  

<img width="1153" height="934" alt="image" src="https://github.com/user-attachments/assets/b262f1af-14a0-491f-98a5-826e8073c0de" />


## How to use:
Simply enter a Wireguard config but instead of an allow list we define  
	- a local Network list: The IP`s  / Networks to allow to all connected Peers (kinda reverse allow list)  
	- Peerlist: freely choose which peer is allowed to connect to the current Peer,  
							this will also add all local networks of the other peer to the current peers allowlist


After that click on each peer and either export via QR Code / via File / or Copy Paste
The configuration will be generated at this point based on Peer list and each Peer local Network

Yes you can Store multiple different WG Networks within one file. 
Only if a peer is linked to another it will affect that config. 

Copy a config: simple Rename a config you whish to copy. 
The you will get a new one with the new Name the old stays in Place.
yes, to rename and not copy you need to delete the old File, call it a feature, call it a bug, its how it works. 

Update config: Update Data on the Peer in question (or add a new one), after saving the changes, simply export the config of all affected
Peers
