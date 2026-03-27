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

const VERSION_OPTIONS = {
  v4: ["v4", "v4.1"],
  v5: ["v5", "v5.1"],
  v6: ["v6", "v6.1"],
} as const;

const AverageImagesPage: React.FC = () => {
  const [images, setImages] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [selectedClass, setSelectedClass] = useState<string | null>(null);
  const [baseVersion, setBaseVersion] = useState<"v4" | "v5" | "v6">("v4");
  const [variant, setVariant] = useState<
    "v4" | "v4.1" | "v5" | "v5.1" | "v6" | "v6.1"
  >("v4");

  const classKeys = Object.keys(images);

  useEffect(() => {
    const fetchImages = async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `http://localhost:5000/average_images?v=${variant}`,
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
  }, [variant]);

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
    [selectedClass, classKeys],
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

      <Box
        sx={{
          minHeight: "calc(100vh - 65px)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          p: 6,
          background:
            "linear-gradient(135deg, #11998e 0%, #43cea2 50%, #38ef7d 100%)",
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
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Average Character Images
          </Typography>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            Visual representation of average letter shapes from your dataset.
          </Typography>

          <Box
            sx={{
              display: "flex",
              justifyContent: "flex-end",
              gap: 2,
              mt: 3,
              mb: 3,
              mr: 3,
            }}
          >
            <FormControl sx={{ minWidth: 120 }}>
              <InputLabel>Base</InputLabel>
              <Select
                value={baseVersion}
                label="Base"
                onChange={(e) => {
                  const newBase = e.target.value as "v4" | "v5" | "v6";
                  setBaseVersion(newBase);
                  setVariant(VERSION_OPTIONS[newBase][0]);
                }}
              >
                <MenuItem value="v4">v4</MenuItem>
                <MenuItem value="v5">v5</MenuItem>
                <MenuItem value="v6">v6</MenuItem>
              </Select>
            </FormControl>

            {/* VERSION SELECT */}
            <FormControl sx={{ minWidth: 160 }}>
              <InputLabel>Version</InputLabel>
              <Select
                value={variant}
                label="Version"
                onChange={(e) =>
                  setVariant(
                    e.target.value as
                      | "v4"
                      | "v4.1"
                      | "v5"
                      | "v5.1"
                      | "v6"
                      | "v6.1",
                  )
                }
              >
                {VERSION_OPTIONS[baseVersion].map((v) => (
                  <MenuItem key={v} value={v}>
                    {v}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>

          <AverageImagesGrid
            images={images}
            loading={loading}
            onSelect={handleOpen}
          />
        </Paper>
      </Box>

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
