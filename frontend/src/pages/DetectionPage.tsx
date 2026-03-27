import React, { useState, useRef } from "react";
import {
  Box,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CssBaseline,
} from "@mui/material";

import { useDispatch, useSelector } from "react-redux";
import { RootState, AppDispatch } from "../app/store";
import { setDetections, clearImage } from "../features/image/imageSlice";
import { setDetectionMode, setConfidence } from "../features/ui/uiSlice";

import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import ImageUploader from "../components/DetectionPage/ImageUploader";
import DetectionPreview from "../components/DetectionPage/DetectionPreview";
import CroppedModal from "../components/DetectionPage/CroppedModal";
import SahiToggle from "../components/DetectionPage/SahiToggle";
import PolygonToggle from "../components/DetectionPage/PolygonToggle";
import LetterSelect from "../components/DetectionPage/LetterSelect";

interface Props {
  type: string;
  modes: string[];
  title: React.ReactNode;
  gradient: string;
  polygon: boolean;
}

const DetectionPage: React.FC<Props> = ({
  type,
  modes,
  title,
  gradient,
  polygon,
}) => {
  const dispatch = useDispatch<AppDispatch>();

  const { preview, detections } = useSelector(
    (state: RootState) => state.image,
  );

  const { useSahi, usePolygon, detectionMode, confidence } = useSelector(
    (state: RootState) => state.ui,
  );

  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedBox, setSelectedBox] = useState<any | null>(null);
  const [croppedSrc, setCroppedSrc] = useState<string | null>(null);

  const [selectedLetters, setSelectedLetters] = useState<string[]>([]);

  const imgRef = useRef<HTMLImageElement | null>(null);

  const handleRemove = () => {
    setFile(null);
    dispatch(clearImage());
    setSelectedLetters([]);
  };

  const handleDetect = async () => {
    if (!file) {
      toast.error("No file selected!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("mode", detectionMode || modes[0]);
    formData.append("useSAHI", String(useSahi));
    formData.append("usePolygon", String(polygon && usePolygon));
    formData.append("confidence", String(confidence));

    try {
      setLoading(true);

      const res = await fetch("http://localhost:5000/detect", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok || data.error) {
        toast.error(data.error || "Detection failed.");
        return;
      }

      const newDetections = data.detections || [];

      dispatch(setDetections(newDetections));

      const letters = Array.from(
        new Set<string>(newDetections.map((d: any) => d.class)),
      ).sort();

      setSelectedLetters(letters);

      if (newDetections.length) {
        toast.success(
          `Found ${newDetections.length} detections ${
            useSahi ? "(SAHI enabled)" : ""
          }`,
        );
      } else {
        toast.warn("No detections found.");
        setSelectedLetters([]);
      }
    } catch {
      toast.error("Detection failed.");
    } finally {
      setLoading(false);
    }
  };

  const letterOptions = Array.from(
    new Set<string>(detections.map((d: any) => d.class)),
  ).sort();

  const filteredDetections =
    selectedLetters.length === 0
      ? []
      : detections.filter((d: any) => selectedLetters.includes(d.class));

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
          background: gradient,
        }}
      >
        <Paper
          elevation={10}
          sx={{
            width: "100%",
            maxWidth: 700,
            p: 5,
            borderRadius: 4,
            textAlign: "center",
            backgroundColor: "rgba(255,255,255,0.95)",
            backdropFilter: "blur(8px)",
          }}
        >
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            {title}
          </Typography>

          <Typography variant="body1" color="text.secondary" gutterBottom>
            Upload an image and select your detection mode below.
          </Typography>

          <FormControl fullWidth sx={{ mt: 3 }}>
            <InputLabel id="mode-select-label">Detection Mode</InputLabel>

            <Select
              labelId="mode-select-label"
              value={detectionMode || modes[0]}
              label="Detection Mode"
              onChange={(e) => dispatch(setDetectionMode(e.target.value))}
            >
              {modes.map((m) => (
                <MenuItem key={m} value={m}>
                  {m}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {type !== "ocr" && (
            <Box
              sx={{
                display: "flex",
                gap: 5,
                mt: 3,
                alignItems: "center",
                justifyContent: "center",
                flexWrap: "wrap",
              }}
            >
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "flex-start",
                }}
              >
                <SahiToggle visible />
                {polygon && <PolygonToggle visible />}
              </Box>

              <FormControl sx={{ minWidth: 180 }}>
                <InputLabel>Confidence</InputLabel>

                <Select
                  value={confidence}
                  label="Confidence"
                  onChange={(e) =>
                    dispatch(setConfidence(Number(e.target.value)))
                  }
                >
                  {[25, 50, 75, 90].map((v) => (
                    <MenuItem key={v} value={v}>
                      {v}%
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
          )}

          {letterOptions.length > 0 && type !== "ocr" && (
            <LetterSelect
              options={letterOptions}
              selected={selectedLetters}
              onChange={setSelectedLetters}
              label="Letters"
            />
          )}

          {!preview ? (
            <ImageUploader onFileSelected={setFile} />
          ) : (
            <DetectionPreview
              preview={preview}
              detections={filteredDetections}
              imgRef={imgRef}
              onCrop={(det, cropped) => {
                setSelectedBox(det);
                setCroppedSrc(cropped);
              }}
              onRemove={handleRemove}
              onDetect={handleDetect}
              loading={loading}
            />
          )}
        </Paper>
      </Box>

      <CroppedModal
        open={!!selectedBox}
        box={selectedBox}
        croppedSrc={croppedSrc}
        onClose={() => {
          setSelectedBox(null);
          setCroppedSrc(null);
        }}
      />
    </>
  );
};

export default DetectionPage;
