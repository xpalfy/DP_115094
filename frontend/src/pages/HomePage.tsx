import React from "react";
import { Box, Paper, Typography, CssBaseline, Divider } from "@mui/material";

const HomePage: React.FC = () => {
  return (
    <>
      <CssBaseline />

      <Box
        sx={{
          minHeight: "calc(100vh - 65px)",
          background:
            "linear-gradient(135deg, #11998e 0%, #43cea2 50%, #38ef7d 100%)",
          py: 10,
          px: 3,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Box sx={{ width: "100%", maxWidth: 1150 }}>
          <Box
            sx={{
              textAlign: "center",
              color: "white",
              mb: 8,
            }}
          >
            <Typography
              variant="h2"
              fontWeight="bold"
              sx={{
                letterSpacing: "-0.02em",
                mb: 2,
              }}
            >
              Detection and Segmentation of Letters
              <br />
              in Historical Manuscripts
            </Typography>

            <Typography
              variant="h6"
              sx={{
                opacity: 0.9,
                maxWidth: 800,
                margin: "0 auto",
              }}
            >
              Master's thesis project comparing modern deep learning models for
              detecting and segmenting handwritten characters in historical
              German and French manuscripts.
            </Typography>

            <Typography
              sx={{
                mt: 3,
                opacity: 0.8,
              }}
            >
              Slovak University of Technology in Bratislava
            </Typography>
          </Box>

          <Paper
            elevation={18}
            sx={{
              borderRadius: 5,
              p: { xs: 4, md: 7 },
              background: "rgba(255,255,255,0.96)",
              backdropFilter: "blur(10px)",
              boxShadow: "0 25px 60px rgba(0,0,0,0.15)",
            }}
          >
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: {
                  xs: "1fr",
                  md: "1fr 1fr",
                },
                gap: 6,
              }}
            >
              <Box>
                <Typography
                  variant="h5"
                  fontWeight="bold"
                  gutterBottom
                  sx={{ color: "#11998e" }}
                >
                  Project Information
                </Typography>

                <Typography>
                  <b>University:</b> Slovak University of Technology in
                  Bratislava
                </Typography>
                <Typography>
                  <b>Faculty:</b> Faculty of Electrical Engineering and
                  Information Technology
                </Typography>
                <Typography>
                  <b>Department:</b> Institute of Informatics and Mathematics
                </Typography>
                <Typography>
                  <b>Author:</b> Vincent Pálfy
                </Typography>
                <Typography>
                  <b>Supervisor:</b> Ing. Pavol Marák, PhD.
                </Typography>
                <Typography>
                  <b>Academic Year:</b> 2025 / 2026
                </Typography>
                <Typography>
                  <b>Study Programme:</b> Applied Informatics
                </Typography>
              </Box>

              <Box>
                <Typography
                  variant="h5"
                  fontWeight="bold"
                  gutterBottom
                  sx={{ color: "#11998e" }}
                >
                  Project Overview
                </Typography>

                <Typography>
                  The goal of this thesis is to develop and compare algorithms
                  capable of detecting and segmenting individual letters in
                  unencrypted historical handwritten manuscripts written in
                  German and French.
                </Typography>

                <Typography sx={{ mt: 2 }}>
                  Historical manuscripts are challenging to process due to
                  varying handwriting styles, document quality, and the visual
                  similarity between certain characters. The work focuses on
                  small lowercase letters, which form the majority of the text
                  in these documents.
                </Typography>
              </Box>
            </Box>

            <Divider sx={{ my: 6 }} />

            <Typography
              variant="h5"
              fontWeight="bold"
              gutterBottom
              sx={{ color: "#11998e" }}
            >
              Research Approach
            </Typography>

            <Typography sx={{ mb: 2 }}>
              This work builds on the previous master's thesis of Ing. Dagmar
              Trabalíková, whose results on the German dataset are reproduced
              and extended in this project.
            </Typography>

            <Box sx={{ ml: 2 }}>
              <Typography>
                • Extension of the existing German manuscript dataset with
                additional annotated samples
              </Typography>
              <Typography>
                • Creation of a new annotated French manuscript dataset
              </Typography>
              <Typography>
                • Construction of a combined multilingual dataset from both
                sources
              </Typography>
              <Typography>
                • Training and evaluation of detection and segmentation models
                on each dataset separately and on the combined dataset
              </Typography>
              <Typography>
                • Development of a web application for testing trained models
                and visualizing their outputs
              </Typography>
            </Box>

            <Divider sx={{ my: 6 }} />

            <Typography
              variant="h5"
              fontWeight="bold"
              gutterBottom
              sx={{ color: "#11998e" }}
            >
              Machine Learning Models
            </Typography>

            <Typography>
              Two families of modern deep learning models are compared:
            </Typography>

            <Box sx={{ ml: 2, mt: 2 }}>
              <Typography>
                • YOLO models — YOLOv8, YOLO11, and YOLO26 for both detection
                and segmentation, and the experimental YOLO12 for detection only
              </Typography>
              <Typography>
                • RF-DETR — a transformer-based model used for both detection
                and segmentation
              </Typography>
            </Box>

            <Typography sx={{ mt: 2 }}>
              YOLO models were trained on the German, French, and combined
              datasets, while RF-DETR was trained only on the combined dataset
              due to the higher data requirements of transformer architectures.
              Each model was evaluated on the test set of the dataset it was
              trained on.
            </Typography>

            <Typography sx={{ mt: 2 }}>
              For inference on full-page documents, the SAHI technique is used
              to split large images into smaller tiles, which allows the models
              to detect characters that would otherwise be too small relative to
              the model's input size.
            </Typography>

            <Divider sx={{ my: 6 }} />

            <Typography
              variant="h5"
              fontWeight="bold"
              gutterBottom
              sx={{ color: "#11998e" }}
            >
              Research Project Context
            </Typography>

            <Typography>
              This thesis is part of the research project:
            </Typography>

            <Typography sx={{ mt: 2 }} fontWeight="bold">
              Artificial Intelligence for Processing Encrypted Historical
              Manuscripts
            </Typography>

            <Typography sx={{ mt: 1 }}>
              Project Code: 09I05-03-V02-00031
            </Typography>

            <Typography>
              Program: Recovery and Resilience Plan of the Slovak Republic
            </Typography>

            <Divider sx={{ my: 6 }} />

            <Typography
              variant="h5"
              fontWeight="bold"
              gutterBottom
              sx={{ color: "#11998e" }}
            >
              Web Application
            </Typography>

            <Typography>
              The web application provides a complete environment for working
              with the trained models and the underlying datasets:
            </Typography>

            <Box sx={{ ml: 2, mt: 2 }}>
              <Typography>
                • Inference — uploading images and running selected models with
                adjustable confidence threshold, optional SAHI processing, and
                segmentation masks where available
              </Typography>
              <Typography>
                • Dataset statistics — class distribution, train/val/test splits
                and basic information for each dataset version
              </Typography>
              <Typography>
                • Sample images — viewing original manuscript images together
                with their annotations
              </Typography>
              <Typography>
                • Average shapes — visual comparison of typical letter shapes
                across datasets
              </Typography>
            </Box>

            <Typography sx={{ mt: 2 }}>
              Detection results can be filtered by individual classes, which
              makes it easier to inspect model behaviour on specific characters.
            </Typography>
          </Paper>
        </Box>
      </Box>
    </>
  );
};

export default HomePage;
