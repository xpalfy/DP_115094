import React, { useEffect, useState } from "react";
import {
  Box,
  Paper,
  Typography,
  CssBaseline,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import SampleImagesGrid from "../components/SampleImagesPage/SampleImagesGrid";
import SampleImageModal from "../components/SampleImagesPage/SampleImageModal";

export interface Annotation {
  class: string;
  polygon: number[][];
}

export interface SampleImage {
  filename: string;
  image_url: string;
  width: number;
  height: number;
  annotations: Annotation[];
}

const VERSION_OPTIONS = {
  v4: ["v4", "v4.4"],
  v5: ["v5", "v5.4"],
  v6: ["v6", "v6.4"],
} as const;

const SampleImagesPage: React.FC = () => {
  const [images, setImages] = useState<SampleImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const [baseVersion, setBaseVersion] = useState<"v4" | "v5" | "v6">("v4");
  const [variant, setVariant] = useState<
    "v4" | "v4.4" | "v5" | "v5.4" | "v6" | "v6.4"
  >("v4");
  const [split, setSplit] = useState<"train" | "val" | "test">("train");
  const [numImages, setNumImages] = useState<number>(10);

  const hasSplit = ["v4.4", "v5.4", "v6.4"].includes(variant);

  const fetchImages = async () => {
    try {
      setLoading(true);
      const res = await fetch(
        `http://localhost:5000/sample_images?v=${variant}&num=${numImages}&split=${split}`,
      );
      const data = await res.json();

      if (!res.ok || data.error) throw new Error(data.error);

      setImages(data.images || []);
    } catch (err) {
      console.error(err);
      toast.error("Failed to fetch sample images.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
  }, [variant, numImages, hasSplit ? split : null]);

  useEffect(() => {
    if (!hasSplit) {
      setSplit("train");
    }
  }, [variant]);

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
            maxWidth: 1300,
            p: 5,
            borderRadius: 4,
            textAlign: "center",
            backgroundColor: "rgba(255,255,255,0.95)",
            backdropFilter: "blur(8px)",
          }}
        >
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Sample Dataset Images
          </Typography>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            Random samples with YOLO polygon annotations.
          </Typography>

          <Box
            sx={{
              display: "flex",
              justifyContent: "flex-end",
              gap: 2,
              mt: 5,
              mb: 2,
              mr: 2,
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
            <FormControl sx={{ minWidth: 140 }}>
              <InputLabel>Version</InputLabel>
              <Select
                value={variant}
                label="Version"
                onChange={(e) =>
                  setVariant(
                    e.target.value as
                      | "v4"
                      | "v4.4"
                      | "v5"
                      | "v5.4"
                      | "v6"
                      | "v6.4",
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
            {hasSplit && (
              <FormControl sx={{ minWidth: 160 }}>
                <InputLabel>Split</InputLabel>
                <Select
                  value={split}
                  label="Split"
                  onChange={(e) =>
                    setSplit(e.target.value as "train" | "val" | "test")
                  }
                >
                  <MenuItem value="train">train</MenuItem>
                  <MenuItem value="val">val</MenuItem>
                  <MenuItem value="test">test</MenuItem>
                </Select>
              </FormControl>
            )}
            <FormControl sx={{ minWidth: 140 }}>
              <InputLabel>Samples</InputLabel>
              <Select
                value={numImages}
                label="Samples"
                onChange={(e) => setNumImages(e.target.value as number)}
              >
                <MenuItem value={5}>5</MenuItem>
                <MenuItem value={10}>10</MenuItem>
                <MenuItem value={20}>20</MenuItem>
              </Select>
            </FormControl>
          </Box>

          {loading ? (
            <Box sx={{ mt: 6, display: "flex", justifyContent: "center" }}>
              <CircularProgress color="primary" />
            </Box>
          ) : (
            <SampleImagesGrid
              images={images}
              onSelect={(i) => {
                setSelectedIndex(i);
                setOpen(true);
              }}
            />
          )}
        </Paper>
      </Box>

      {selectedIndex !== null && (
        <SampleImageModal
          open={open}
          image={images[selectedIndex]}
          onClose={() => {
            setOpen(false);
            setSelectedIndex(null);
          }}
          onNavigate={(d) =>
            setSelectedIndex((prev) =>
              prev === null
                ? null
                : d === "next"
                  ? (prev + 1) % images.length
                  : (prev - 1 + images.length) % images.length,
            )
          }
        />
      )}
    </>
  );
};

export default SampleImagesPage;
