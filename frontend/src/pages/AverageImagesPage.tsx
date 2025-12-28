import React, { useEffect, useState, useCallback } from "react";
import {
  Box,
  Typography,
  Paper,
  CssBaseline,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import AverageImagesGrid from "../components/AverageImagesPage/AverageImagesGrid";
import AverageImageModal from "../components/AverageImagesPage/AverageImageModal";

const AverageImagesPage: React.FC = () => {
  const [images, setImages] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [selectedClass, setSelectedClass] = useState<string | null>(null);
  const [version, setVersion] = useState<"v4" | "v5">("v4");

  const classKeys = Object.keys(images);

  // ==============================
  // FETCH AVERAGE IMAGES
  // ==============================
  useEffect(() => {
    const fetchImages = async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `http://localhost:5000/average_images?v=${version}`
        );
        if (!res.ok) throw new Error(`Server returned ${res.status}`);

        const data = await res.json();
        if (data.error) {
          toast.error(data.error);
          return;
        }

        if (data.images) setImages(data.images);
        else toast.warn("No images found in response.");
      } catch (err) {
        console.error(err);
        toast.error("Failed to fetch average images.");
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, [version]);

  // ==============================
  // MODAL HANDLERS
  // ==============================
  const handleOpen = (cls: string) => {
    setSelectedClass(cls);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedClass(null);
  };

  const handleNavigate = useCallback(
    (direction: "prev" | "next") => {
      if (!selectedClass || classKeys.length === 0) return;
      const currentIndex = classKeys.indexOf(selectedClass);
      if (currentIndex === -1) return;

      const newIndex =
        direction === "next"
          ? (currentIndex + 1) % classKeys.length
          : (currentIndex - 1 + classKeys.length) % classKeys.length;

      setSelectedClass(classKeys[newIndex]);
    },
    [selectedClass, classKeys]
  );

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!open) return;
      if (e.key === "ArrowRight") handleNavigate("next");
      if (e.key === "ArrowLeft") handleNavigate("prev");
      if (e.key === "Escape") handleClose();
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, handleNavigate]);

  return (
    <>
      <CssBaseline />
      <ToastContainer position="top-center" autoClose={3000} />

      {/* PAGE WRAPPER */}
      <Box
        sx={{
          minHeight: "calc(100vh - 65px)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          p: 6,
          background: "linear-gradient(135deg, #11998e, #38ef7d)",
        }}
      >
        <Paper
          elevation={10}
          sx={{
            width: "100%",
            maxWidth: 1200,
            p: 5,
            borderRadius: 4,
            textAlign: "center",
            backgroundColor: "rgba(255,255,255,0.95)",
            backdropFilter: "blur(8px)",
          }}
        >
          {/* HEADER */}
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Average Character Images
          </Typography>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            Visual representation of average letter shapes from your dataset.
          </Typography>

          {/* VERSION SELECT */}
          <Box
            sx={{
              display: "flex",
              justifyContent: "flex-end",
              mt: 3,
              mb: 3,
              mr: 3,
            }}
          >
            <FormControl sx={{ minWidth: 160 }}>
              <InputLabel id="version-select-label">Dataset version</InputLabel>
              <Select
                labelId="version-select-label"
                value={version}
                label="Dataset version"
                onChange={(e) => setVersion(e.target.value as "v4" | "v5")}
                sx={{ minWidth: 160 }}
              >
                <MenuItem value="v4">v4</MenuItem>
                <MenuItem value="v5">v5</MenuItem>
              </Select>
            </FormControl>
          </Box>

          {/* GRID */}
          <AverageImagesGrid
            images={images}
            loading={loading}
            onSelect={handleOpen}
          />
        </Paper>
      </Box>

      {/* MODAL */}
      <AverageImageModal
        open={open}
        selectedClass={selectedClass}
        images={images}
        onClose={handleClose}
        onNavigate={handleNavigate}
      />
    </>
  );
};

export default AverageImagesPage;
