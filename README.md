# Detection and Segmentation of Letters in Historical Manuscripts

**Master's Thesis – Slovak University of Technology in Bratislava**  
Faculty of Electrical Engineering and Information Technology (FEI)  
Institute of Informatics and Mathematics  
Academic Year: 2025/2026  

---

## Author

**Bc. Vincent Pálfy**  
Study Programme: Applied Informatics  
Field of Study: Informatics  
Reference Number: FEI-16607-115094  
Student ID: 115094  

Thesis Supervisor: Ing. Pavol Marák, PhD.  
Head of Department: doc. Ing. Milan Vojvoda, PhD.

---

## Project Description

The aim of this master's thesis is to develop and test an algorithm for the detection and segmentation of letters in historical manuscripts. The work focuses on manuscripts containing unencrypted text written in German and French.

Historical handwritten documents present a challenging problem for current OCR methods, primarily due to varying writing quality, high intra-class variability of letters, different character frequencies, and diverse graphical styles. Document damage, noise, and the overall visual inconsistency of manuscripts also play a significant role.

The project builds upon the master's thesis of **Ing. Dagmar Trabalíková**, who created the initial system for recognizing letters in historical manuscripts.

---

## Main Tasks

1. Study and describe the topic of historical manuscripts and the YOLO and RF-DETR models.
2. Analyze and document existing solutions in the field.
3. Reproduce the results of the master's thesis by Ing. Dagmar Trabalíková.
4. Create and analyze datasets containing letter annotations from unencrypted German and French documents.
5. Select appropriate YOLO and RF-DETR models for detection and segmentation, and train them on individual datasets separately as well as on the merged dataset.
6. Develop a web application for testing models and visualizing results.
7. Evaluate the success of the experiments.
8. Prepare written documentation.

---

## Technologies Used

The project is implemented primarily using the following technologies and tools:

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

## Datasets

The project works with historical manuscripts containing unencrypted text in:

- German,
- French.

Multiple versions of datasets created during data preparation and processing are used throughout the project. Annotations are produced in formats compatible with YOLO and RF-DETR models. The project includes separate datasets for German and French documents, as well as a combined version.

---

## Web Application

The project includes a web application designed for:

- Testing detection and segmentation models,
- Comparing different processing modes,
- Displaying average letter shapes,
- Browsing sample dataset images with annotations,
- Displaying dataset statistics,
- Visualizing inference results on user-uploaded images.

The application consists of a backend implemented in the Flask framework and a frontend implemented using React.

---

## Running the Project

Docker Desktop must be installed to run the project. The installation package for Windows is available on the official website:

https://docs.docker.com/desktop/setup/install/windows-install/

After opening the root project folder, the application can be started with the command:

```bash
docker compose up --build
```

Once successfully started, the web application is accessible at:

```
http://localhost:3000
```

To stop the containers after use, run:

```bash
docker compose down
```

---

## Project Structure

The project contains the following main components:

- `backend/` – backend part of the application and API endpoints
- `frontend/` – frontend part of the application and user interface
- `features/` – helper scripts for data processing, statistics, and visualization
- `dataset/` – annotated datasets for German and French documents

---

## References

- Antal, E. et al. *Encrypted Documents and Cipher Keys From the 18th and 19th Century in the Archives of Aristocratic Families in Slovakia.* International Conference on Historical Cryptology, 2023.
- Antal, E. et al. *HHCS: A Dataset of Cipher Symbol Annotations From Handwritten Historical Encrypted Documents for Machine Learning Tasks.* IEEE Access, 2026.
- Malashin, I. P. et al. *Recognition of Handwritten Characters in Birch-Bark Manuscripts via Object Detection.* IEEE Access, 2025.

---

## Research Project

This master's thesis is part of the following research project:

**Using Artificial Intelligence for Processing Encrypted Manuscripts**  
Project Code: **09I05-03-V02-00031**  
Programme: **Recovery and Resilience Plan of the Slovak Republic**
