import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Button,
  Stack,
  CircularProgress,
} from "@mui/material";

interface DetectionPreviewProps {
  preview: string;
  detections: any[];
  imgRef: React.RefObject<HTMLImageElement | null>;
  onCrop: (det: any, cropped: string) => void;
  onRemove: () => void;
  onDetect: () => void;
  loading: boolean;
}

const DetectionPreview: React.FC<DetectionPreviewProps> = ({
  preview,
  detections,
  imgRef,
  onCrop,
  onRemove,
  onDetect,
  loading,
}) => {
  const [imageDims, setImageDims] = useState({ w: 1, h: 1 });
  const [renderDims, setRenderDims] = useState({ w: 1, h: 1 });

  const cropFromOriginal = (det: any) => {
    if (!imgRef.current) return;
    const [x1, y1, x2, y2] = det.bbox;
    const img = imgRef.current;

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const cropWidth = x2 - x1;
    const cropHeight = y2 - y1;
    canvas.width = cropWidth;
    canvas.height = cropHeight;

    ctx.drawImage(
      img,
      x1,
      y1,
      cropWidth,
      cropHeight,
      0,
      0,
      cropWidth,
      cropHeight
    );
    const dataUrl = canvas.toDataURL("image/png");
    onCrop(det, dataUrl);
  };

  return (
    <Box mt={5} textAlign="center">
      <Typography variant="h6" gutterBottom>
        Preview with Detections
      </Typography>

      <Box
        sx={{
          position: "relative",
          display: "inline-block",
          borderRadius: 3,
          overflow: "hidden",
          boxShadow: "0 6px 18px rgba(0,0,0,0.15)",
          maxWidth: "100%",
        }}
      >
        <img
          ref={imgRef}
          src={preview}
          alt="Uploaded preview"
          crossOrigin="anonymous"
          style={{
            maxWidth: "100%",
            maxHeight: "80vh",
            display: "block",
          }}
          onLoad={(e) => {
            const img = e.currentTarget;
            setImageDims({ w: img.naturalWidth, h: img.naturalHeight });
            setRenderDims({ w: img.width, h: img.height });
          }}
        />

        {detections.map((det: any, i: number) => {
          const [x1, y1, x2, y2] = det.bbox;
          const scaleX = renderDims.w / imageDims.w;
          const scaleY = renderDims.h / imageDims.h;

          return (
            <Box
              key={i}
              onClick={() => cropFromOriginal(det)}
              sx={{
                position: "absolute",
                left: `${x1 * scaleX}px`,
                top: `${y1 * scaleY}px`,
                width: `${(x2 - x1) * scaleX}px`,
                height: `${(y2 - y1) * scaleY}px`,
                border: "2px solid #ff3b3b",
                borderRadius: "3px",
                backgroundColor: "rgba(255,0,0,0.25)",
                cursor: "pointer",
                transition: "all 0.2s ease-in-out",
                "&:hover": {
                  backgroundColor: "rgba(255,0,0,0.45)",
                  borderColor: "#ff5555",
                },
              }}
            />
          );
        })}
      </Box>

      <Stack direction="row" spacing={2} justifyContent="center" mt={3}>
        <Button variant="outlined" color="error" onClick={onRemove}>
          Remove
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={onDetect}
          disabled={loading}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : "Detect"}
        </Button>
      </Stack>
    </Box>
  );
};

export default DetectionPreview;
