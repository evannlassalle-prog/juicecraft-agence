# Masters vidéo 30 s (version du 2026-10-10 : prix sans TTC, « /mois » visible)

Chaque master est découpé en 3 morceaux (limite de 100 Mo par fichier sur GitHub). Pour le recoller, ouvrir un terminal dans ce dossier :

**Windows (invite de commandes)**
```
copy /b juicecraft_pub_30s_16x9_master.mp4.001+juicecraft_pub_30s_16x9_master.mp4.002+juicecraft_pub_30s_16x9_master.mp4.003 juicecraft_pub_30s_16x9_master.mp4
copy /b juicecraft_pub_30s_9x16_master.mp4.001+juicecraft_pub_30s_9x16_master.mp4.002+juicecraft_pub_30s_9x16_master.mp4.003 juicecraft_pub_30s_9x16_master.mp4
```

**macOS ou Linux**
```
cat juicecraft_pub_30s_16x9_master.mp4.00? > juicecraft_pub_30s_16x9_master.mp4
cat juicecraft_pub_30s_9x16_master.mp4.00? > juicecraft_pub_30s_9x16_master.mp4
```

Vérification : l'empreinte doit correspondre à `SHA256.txt`.
Windows : `certutil -hashfile juicecraft_pub_30s_16x9_master.mp4 SHA256`. macOS : `shasum -a 256 juicecraft_pub_30s_16x9_master.mp4`.

Le fichier recollé n'est pas suivi par Git (`.gitignore` exclut `*_master.mp4`).
