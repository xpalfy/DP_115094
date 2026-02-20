# Detekcia a segmentácia písmen v historických rukopisoch

**Diplomová práca – Slovenská technická univerzita v Bratislave**  
Fakulta elektrotechniky a informatiky (FEI)  
Ústav informatiky a matematiky  
Akademický rok: 2025/2026  

---

## Autor

**Bc. Vincent Pálfy**  
Študijný program: Aplikovaná informatika  
Evidenčné číslo: FEI-16607-115094  
ID študenta: 115094  

Vedúci práce: Ing. Pavol Marák, PhD.  
Vedúci pracoviska: doc. Ing. Milan Vojvoda, PhD.  

Termín odovzdania: **15. 05. 2026**

---

## Popis projektu

Cieľom diplomovej práce je vyvinúť a otestovať algoritmus na **detekciu a segmentáciu písmen v historických rukopisoch**, konkrétne v nešifrovaných dokumentoch v nemeckom a francúzskom jazyku.

Historické rukopisy predstavujú významnú výzvu pre moderné OCR systémy z dôvodu:

- vysokej vnútrotriednej variability písmen,
- rozdielnej kvality zápisu,
- rôznej frekvencie výskytu znakov,
- rozmanitých grafických štýlov,
- degradácie dokumentov.

Projekt nadväzuje na diplomovú prácu Ing. Dagmar Trabalíkovej, ktorá vytvorila prvotný systém na rozpoznávanie písmen.

---

## Hlavné ciele

1. Rozšíriť existujúci dataset anotácií písmen v nemeckých dokumentoch.
2. Vytvoriť nový dataset anotácií písmen vo francúzskych dokumentoch.
3. Implementovať a natrénovať modely:
   - YOLO (rodina modelov pre objektovú detekciu)
   - RF-DETR (transformerový model pre detekciu objektov)
4. Porovnať výsledky modelov:
   - na samostatných datasetoch
   - na zlúčenom datasete
5. Vyvinúť webovú aplikáciu na:
   - testovanie modelov
   - vizualizáciu výsledkov detekcie
6. Vyhodnotiť experimenty pomocou relevantných metrík (mAP, precision, recall, IoU).
7. Vypracovať kompletnú dokumentáciu.

---

## Použité technológie

- Python
- PyTorch
- Ultralytics YOLO
- RF-DETR
- OpenCV
- Label Studio (anotácie)
- Flask (backend web aplikácie)
- React (frontend)
- Docker

---

## Datasety

Projekt pracuje s historickými rukopismi obsahujúcimi:

- nešifrovaný text,
- nemecký jazyk,
- francúzsky jazyk,
- vysokú vizuálnu variabilitu písma.

Anotácie budú vytvorené vo formáte kompatibilnom s YOLO a RF-DETR.

---

## Literatúra

- Antal, E. et al. (2023). *Encrypted Documents and Cipher Keys From the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia.* International Conference on Historical Cryptology.
- Antal, E. et al. (2026). *HHCS: A Dataset of Cipher Symbol Annotations From Handwritten Historical Encrypted Documents for Machine Learning Tasks.* IEEE Access.
- Malashin, I. P. et al. (2025). *Recognition of Handwritten Characters in Birch-Bark Manuscripts via Object Detection.* IEEE Access.

---

## Licencia

Diplomová práca je súčasťou výskumného projektu:

**Využitie umelej inteligencie na spracovanie šifrovaných rukopisov**  
Kód projektu: 09I05-03-V02-00031  
Program: Plán obnovy a odolnosti SR

Tento projekt je vypracovaný ako diplomová práca na FEI STU v Bratislave.  
Použitie dát a modelov podlieha podmienkam výskumného projektu.