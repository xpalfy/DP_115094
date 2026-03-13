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
          {/* HERO */}

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
              Master's thesis project exploring deep learning models for
              detecting handwritten characters in historical German and French
              manuscripts.
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

          {/* MAIN PANEL */}

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
            {/* PROJECT + OVERVIEW */}

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
                  The goal of this thesis is to develop algorithms capable of
                  detecting and segmenting letters in historical handwritten
                  manuscripts containing German and French texts.
                </Typography>

                <Typography sx={{ mt: 2 }}>
                  Historical manuscripts present major challenges for modern OCR
                  systems due to inconsistent handwriting styles, variations in
                  letter quality, and high intra-class variability.
                </Typography>
              </Box>
            </Box>

            <Divider sx={{ my: 6 }} />

            {/* RESEARCH APPROACH */}

            <Typography
              variant="h5"
              fontWeight="bold"
              gutterBottom
              sx={{ color: "#11998e" }}
            >
              Research Approach
            </Typography>

            <Typography sx={{ mb: 2 }}>
              This work extends the research of Ing. Dagmar Trabalíková, who
              developed an initial handwritten character recognition system.
            </Typography>

            <Box sx={{ ml: 2 }}>
              <Typography>
                • Expansion of annotated German manuscript datasets
              </Typography>
              <Typography>
                • Creation of annotated French manuscript datasets
              </Typography>
              <Typography>
                • Training deep learning detection and segmentation models
              </Typography>
              <Typography>
                • Evaluation on individual and combined datasets
              </Typography>
              <Typography>
                • Development of a web interface for model testing
              </Typography>
            </Box>

            <Divider sx={{ my: 6 }} />

            {/* MODELS */}

            <Typography
              variant="h5"
              fontWeight="bold"
              gutterBottom
              sx={{ color: "#11998e" }}
            >
              Machine Learning Models
            </Typography>

            <Typography>
              Several modern deep learning architectures are explored:
            </Typography>

            <Box sx={{ ml: 2, mt: 2 }}>
              <Typography>• YOLOv8 object detection models</Typography>
              <Typography>
                • YOLO11 and YOLO26 experimental architectures
              </Typography>
              <Typography>
                • RF-DETR transformer-based detection model
              </Typography>
            </Box>

            <Typography sx={{ mt: 2 }}>
              The models are trained on German and French datasets independently
              and evaluated on a combined multilingual dataset.
            </Typography>

            <Divider sx={{ my: 6 }} />

            {/* PROJECT CONTEXT */}

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

            {/* WEB APP */}

            <Typography
              variant="h5"
              fontWeight="bold"
              gutterBottom
              sx={{ color: "#11998e" }}
            >
              Web Application
            </Typography>

            <Typography>
              This web application allows users to upload historical manuscript
              images and test trained AI models for letter detection and
              segmentation.
            </Typography>

            <Typography sx={{ mt: 2 }}>
              The system visualizes detected characters, segmentation masks, and
              allows filtering of detected classes to analyze model performance.
            </Typography>
          </Paper>
        </Box>
      </Box>
    </>
  );
};

export default HomePage;
