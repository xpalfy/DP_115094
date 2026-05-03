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

The image data of the processed historical documents is not available in the GitHub repository, as it cannot be publicly shared due to copyright restrictions. A limited portion of the image data is included only in the version submitted to AIS.

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

### Docker Installation

Before running the application for the first time, Docker and Docker Compose must be installed on the device. Installation packages are available on the official Docker website:

https://www.docker.com/products/docker-desktop/

For Windows and macOS, it is recommended to install **Docker Desktop**, which already includes Docker Compose. On Linux, Docker Engine and Docker Compose can be installed separately using the official repository of the relevant distribution. After installation, Docker must be started and its functionality verified using the command:

```bash
docker --version
```

Docker Compose functionality can be verified with:

```bash
docker compose version
```

### Preparation of Trained Models

The trained models are not part of the GitHub repository or the submitted ZIP archive due to their size. For the application to work correctly, they must be downloaded separately from the following link:

https://drive.google.com/drive/folders/1MR6I3FUrrvdnipNODqys6tQlXCxMnlVs?usp=drive_link

After downloading, the folder named `DP_115094_models` must be renamed to `runs`. If the folder with models is downloaded in multiple parts, these parts must first be merged into a single folder so that it contains all the necessary model files. The `runs` folder is then placed into the `backend` folder, which is located in the root directory of the project. The resulting structure must be as follows:

```
backend/runs
```

After correctly placing the `runs` folder, the trained models will be available to the backend part of the application and inference on uploaded images will be possible.

### Starting the Application

Before starting the application, Docker must be running after installation. The application offers two options for starting: a basic **CPU version** and an optional **GPU version** with CUDA support.

#### CPU Version

The basic CPU version is intended for ordinary devices and does not require an NVIDIA graphics card. This version is recommended in case the user does not have a configured environment for running Docker containers with GPU support. The application is started from the root directory of the project using the command:

```bash
docker compose -f docker-compose.cpu.yaml up --build
```

#### GPU Version

The GPU version is intended for devices with an NVIDIA GPU and properly configured CUDA support in the Docker environment. It is started using the command:

```bash
docker compose -f docker-compose.gpu.yaml up --build
```

To run the GPU version, the following are required:

- NVIDIA GPU,
- current NVIDIA driver,
- functional WSL2 environment in case of Windows,
- enabled WSL Integration in Docker Desktop,
- GPU support in Docker containers.

GPU functionality can be verified with:

```bash
nvidia-smi
```

GPU support in Docker can be verified with:

```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Accessing the Application

After successful build and startup of the containers, the web application is accessible at:

```
http://localhost:3000
```

The backend API interface is accessible at:

```
http://localhost:5000
```

### Stopping the Application

To stop the containers after use, run:

```bash
docker compose -f docker-compose.cpu.yaml down
```

Or for the GPU version:

```bash
docker compose -f docker-compose.gpu.yaml down
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