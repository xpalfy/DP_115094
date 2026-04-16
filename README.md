# Detekcia a segmentácia písmen v historických rukopisoch

**Diplomová práca – Slovenská technická univerzita v Bratislave**  
Fakulta elektrotechniky a informatiky (FEI)  
Ústav informatiky a matematiky  
Akademický rok: 2025/2026  

---

## Autor

**Bc. Vincent Pálfy**  
Študijný program: aplikovaná informatika  
Študijný odbor: informatika  
Evidenčné číslo: FEI-16607-115094  
ID študenta: 115094  

Vedúci práce: Ing. Pavol Marák, PhD.  
Vedúci pracoviska: doc. Ing. Milan Vojvoda, PhD.

---

## Popis projektu

Cieľom diplomovej práce je vyvinúť a otestovať algoritmus na detekciu a segmentáciu písmen v historických rukopisoch. Práca je zameraná na rukopisy obsahujúce nešifrovaný text napísaný v nemeckom a francúzskom jazyku.

Historické rukopisné dokumenty predstavujú náročný problém pre súčasné OCR metódy najmä z dôvodu rozdielnej kvality zápisu, vysokej vnútrotriednej variability písmen, rôznej frekvencie výskytu znakov a odlišných grafických štýlov. Významnú úlohu zohráva aj poškodenie dokumentov, šum a celková nejednotnosť vizuálnej podoby rukopisov.

Projekt nadväzuje na diplomovú prácu **Ing. Dagmar Trabalíkovej**, ktorá vytvorila prvotný systém na rozpoznávanie písmen v historických rukopisoch.

---

## Hlavné úlohy práce

1. Naštudovať a popísať problematiku historických rukopisov, modelov YOLO a RF-DETR.
2. Analyzovať a zdokumentovať existujúce riešenia v skúmanej oblasti.
3. Reprodukovať výsledky diplomovej práce Ing. Dagmar Trabalíkovej.
4. Vytvoriť a analyzovať datasety obsahujúce anotácie písmen z nešifrovaných nemeckých a francúzskych dokumentov.
5. Zvoliť vhodné YOLO a RF-DETR modely na detekciu a segmentáciu a natrénovať ich na jednotlivých datasetoch samostatne, ako aj na zlúčenom datasete.
6. Vytvoriť webovú aplikáciu na testovanie modelov a vizualizáciu výsledkov.
7. Vyhodnotiť úspešnosť experimentov.
8. Vypracovať písomnú dokumentáciu.

---

## Použité technológie

Projekt je implementovaný najmä pomocou nasledujúcich technológií a nástrojov:

- Python
- PyTorch
- Ultralytics YOLO
- RF-DETR
- SAHI
- PyTesseract
- EasyOCR
- Label Studio
- Flask
- React
- Redux
- MUI
- Docker

---

## Datasety

Projekt pracuje s historickými rukopismi obsahujúcimi nešifrovaný text v

- nemeckom jazyku,
- francúzskom jazyku.

V rámci riešenia sa využívajú viaceré verzie datasetov vytvorené počas prípravy a spracovania dát. Anotácie sú vytvorené vo formátoch kompatibilných s modelmi YOLO a RF-DETR. Súčasťou projektu sú samostatné datasety pre nemecké a francúzske dokumenty, ako aj ich kombinovaná verzia.

---

## Webová aplikácia

Súčasťou projektu je webová aplikácia určená na:

- testovanie detekčných a segmentačných modelov,
- porovnanie rôznych režimov spracovania,
- zobrazenie priemerných tvarov písmen,
- prehliadanie ukážkových obrázkov datasetu s anotáciami,
- zobrazenie štatistík datasetov,
- vizualizáciu výsledkov inferencie na používateľom nahratých obrázkoch.

Aplikácia pozostáva z backendovej časti implementovanej vo frameworku Flask a frontendovej časti implementovanej pomocou Reactu.

---

## Spustenie projektu

Na spustenie projektu je potrebné mať nainštalovaný nástroj Docker Desktop. Inštalačný balík pre Windows je dostupný na oficiálnej stránke:

https://docs.docker.com/desktop/setup/install/windows-install/

Po otvorení koreňového priečinka projektu je možné aplikáciu spustiť príkazom:

```bash
docker compose up --build
```

Po úspešnom spustení je webová aplikácia dostupná na adrese:

```text
http://localhost:3000
```

Po ukončení práce je možné kontajnery zastaviť príkazom:

```bash
docker compose down
```

---

## Štruktúra projektu

Projekt obsahuje najmä tieto hlavné časti:

- `backend/` – backendová časť aplikácie a API endpointy
- `frontend/` – frontendová časť aplikácie a používateľské rozhranie
- `features/` – pomocné skripty na spracovanie dát, štatistiky a vizualizáci,
- `dataset/` – anotované datasety pre nemecké a francúzske dokumenty

---

## Literatúra

- Antal, E. et al. *Encrypted Documents and Cipher Keys From the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia.* International Conference on Historical Cryptology, 2023.
- Antal, E. et al. *HHCS: A Dataset of Cipher Symbol Annotations From Handwritten Historical Encrypted Documents for Machine Learning Tasks.* IEEE Access, 2026.
- Malashin, I. P. et al. *Recognition of Handwritten Characters in Birch-Bark Manuscripts via Object Detection.* IEEE Access, 2025.

---

## Výskumný projekt

Diplomová práca je zapojená do riešenia výskumného projektu:

**Využitie umelej inteligencie na spracovanie šifrovaných rukopisov**  
Kód projektu: **09I05-03-V02-00031**  
Program: **Plán obnovy a odolnosti SR**
