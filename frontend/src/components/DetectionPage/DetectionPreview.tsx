import React, { useState } from "react";
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
      cropHeight,
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
            setImageDims({
              w: img.naturalWidth,
              h: img.naturalHeight,
            });
          }}
        />

        {detections.length > 0 && (
          <>
            <svg
              style={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
                pointerEvents: "none",
              }}
              viewBox={`0 0 ${imageDims.w} ${imageDims.h}`}
              preserveAspectRatio="none"
            >
              {detections.map((det: any, i: number) => {
                const hasPoly =
                  Array.isArray(det.polygon) && det.polygon.length > 2;

                if (hasPoly) {
                  const points = det.polygon
                    .map(([x, y]: [number, number]) => `${x},${y}`)
                    .join(" ");

                  return (
                    <polygon
                      key={i}
                      points={points}
                      fill="rgba(0,255,0,0.40)"
                      stroke="#00ff66"
                      strokeWidth={3}
                    />
                  );
                }

                const [x1, y1, x2, y2] = det.bbox;

                return (
                  <rect
                    key={i}
                    x={x1}
                    y={y1}
                    width={x2 - x1}
                    height={y2 - y1}
                    fill="rgba(255,0,0,0.40)"
                    stroke="#ff0000"
                    strokeWidth={3}
                    rx={3}
                    ry={3}
                  />
                );
              })}
            </svg>

            <svg
              style={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
              }}
              viewBox={`0 0 ${imageDims.w} ${imageDims.h}`}
              preserveAspectRatio="none"
            >
              {detections.map((det: any, i: number) => {
                const [x1, y1, x2, y2] = det.bbox;

                return (
                  <rect
                    key={i}
                    x={x1}
                    y={y1}
                    width={x2 - x1}
                    height={y2 - y1}
                    fill="transparent"
                    style={{ cursor: "pointer" }}
                    onClick={() => cropFromOriginal(det)}
                  />
                );
              })}
            </svg>
          </>
        )}
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
