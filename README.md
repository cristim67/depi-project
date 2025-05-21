# Proiect Decizie și Estimare în Prelucrarea Informației

## Descriere

Acest proiect realizează analiza și vizualizarea semnalelor ECG (electrocardiogramă) din baza de date PhysioNet, oferind statistici de bază și diverse grafice utile pentru interpretarea semnalului.

## Funcționalități

- Încărcarea unui segment de semnal ECG dintr-un fișier PhysioNet
- Calculul și afișarea statisticilor de bază (media, varianță, deviație standard)
- Plotarea semnalului ECG
- Plotarea funcției de repartiție empirică (ECDF)
- Plotarea densității de probabilitate (PDF) cu histogramă și KDE
- Plotarea funcției de autocorelare
- Plotarea densității spectrale de putere (PSD)
- Salvarea automată a graficelor în directorul `grafice/`

## Instalare

1. Clonează acest repository:

```bash
   git clone https://github.com/cristim67/depi-project.git
   cd depi-project
```

2. Instalează dependențele necesare:

```bash
   pip3 install -r requirements.txt
```

   Dacă nu ai un fișier `requirements.txt`, instalează manual:

```bash
   pip3 install numpy matplotlib wfdb loguru scipy
```

## Utilizare

Scriptul principal este `app.py`. Poate fi rulat din linia de comandă cu diverse argumente:

```bash
python3 app.py --path <cale_catre_physionet> --record <id_fisier> --channel <canal> --start <start> --end <end> --fs <frecventa> --save <True/False>
```

### Exemple

Rulare cu valorile implicite (segment din `chf01`):

```bash
python3 app.py
```

Rulare cu parametri personalizați:

```bash
python3 app.py --path physionet.org/files/chfdb/1.0.0/ --record chf02 --channel 1 --start 5000 --end 10000 --fs 250 --save True
```

Rulare cu toate fișierele din directorul PhysioNet:

```bash
python3 app.py --run_all_records True
```

### Argumente

- `--path`: Calea către directorul cu fișiere PhysioNet (default: `physionet.org/files/chfdb/1.0.0/`)
- `--record`: ID-ul fișierului de analizat (ex: `chf01`)
- `--channel`: Canalul ECG de analizat (default: 0)
- `--start`: Indexul de start pentru segmentul analizat (default: 10000)
- `--end`: Indexul de final pentru segmentul analizat (default: 15000)
- `--fs`: Frecvența de eșantionare în Hz (default: 250)
- `--save`: Salvează graficele în directorul `grafice/` (default: True)
- `--run_all_records`: Rulează toate fișierele din directorul PhysioNet (default: False)
- `--help`: Afisează parametrii pentru script

## Structura proiectului

```bash
├── app.py
├── grafice
│   ├── autocorrelation
│   │   ├── chf01.png
│   │   ├── chf02.png
│   │   ├── ... (până la chf15.png)
│   ├── ecdf
│   │   ├── chf01.png
│   │   ├── ... (până la chf15.png)
│   ├── ecg_signal
│   │   ├── chf01.png
│   │   ├── ... (până la chf15.png)
│   ├── pdf
│   │   ├── chf01.png
│   │   ├── ... (până la chf15.png)
│   └── psd
│       ├── chf01.png
│       ├── ... (până la chf15.png)
├── LICENSE
├── physionet.org
│   ├── files
│   │   └── chfdb
│   │       └── 1.0.0
│   │           ├── ANNOTATORS
│   │           ├── chf01.dat
│   │           ├── chf01.ecg
│   │           ├── chf01.hea
│   │           ├── chf01.hea-
│   │           ├── chf02.dat
│   │           ├── chf02.ecg
│   │           ├── chf02.ecg-
│   │           ├── chf02.hea
│   │           ├── chf02.hea-
│   │           ├── ... (până la chf15.hea-)
│   │           ├── index.html
│   │           ├── RECORDS
│   │           └── SHA256SUMS.txt
│   └── robots.txt
├── README.md
└── requirements.txt
```

## Autori

Cristi Miloiu - 442A

Duta Florin - 442A 