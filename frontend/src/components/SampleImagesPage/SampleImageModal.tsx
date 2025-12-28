import React, { useEffect, useRef } from "react";
import { Box, Typography, Modal, IconButton } from "@mui/material";
import { ArrowBack, ArrowForward, Close } from "@mui/icons-material";
import { SampleImage } from "../../pages/SampleImagesPage";

interface Props {
  open: boolean;
  image: SampleImage;
  onClose: () => void;
  onNavigate: (direction: "prev" | "next") => void;
}

const CLASS_COLORS = [
  "#00e676",
  "#ff1744",
  "#2979ff",
  "#ff9100",
  "#c51162",
  "#00b0ff",
  "#76ff03",
  "#b388ff",
  "#ffea00",
  "#8d6e63",
  "#00bfa5",
  "#d500f9",
  "#ff3d00",
  "#4caf50",
  "#0288d1",
  "#f44336",
  "#7c4dff",
  "#ff6d00",
  "#26c6da",
  "#ff80ab",
];

const SampleImageModal: React.FC<Props> = ({
  open,
  image,
  onClose,
  onNavigate,
}) => {
  const imgRef = useRef<HTMLImageElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const resizeObserverRef = useRef<ResizeObserver | null>(null);

  const drawAnnotations = () => {
    const img = imgRef.current;
    const canvas = canvasRef.current;

    if (!img || !canvas) return;

    const width = img.clientWidth;
    const height = img.clientHeight;

    if (!width || !height) {
      requestAnimationFrame(drawAnnotations);
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = width;
    canvas.height = height;

    const scaleX = width / image.width;
    const scaleY = height / image.height;

    ctx.clearRect(0, 0, width, height);
    ctx.lineWidth = 2;

    image.annotations.forEach((ann) => {
      const poly = ann.polygon;
      const classIndex = parseInt(ann.class);
      const color = CLASS_COLORS[classIndex % CLASS_COLORS.length];

      ctx.strokeStyle = color;
      ctx.fillStyle = color;

      ctx.beginPath();
      poly.forEach(([x, y], i) =>
        i === 0
          ? ctx.moveTo(x * scaleX, y * scaleY)
          : ctx.lineTo(x * scaleX, y * scaleY)
      );
      ctx.closePath();
      ctx.stroke();

      poly.forEach(([vx, vy]) => {
        ctx.beginPath();
        ctx.arc(vx * scaleX, vy * scaleY, 3, 0, Math.PI * 2);
        ctx.fill();
      });
    });
  };

  useEffect(() => {
    if (!open) return;

    const img = imgRef.current;
    if (!img) {
      requestAnimationFrame(() => {
        const retryImg = imgRef.current;
        if (retryImg) {
          if (retryImg.complete) drawAnnotations();
          else retryImg.onload = drawAnnotations;
        }
      });
      return;
    }

    if (img.complete) drawAnnotations();
    else img.onload = drawAnnotations;

    const handleResize = () => requestAnimationFrame(drawAnnotations);
    window.addEventListener("resize", handleResize);

    const ro = new ResizeObserver(() => requestAnimationFrame(drawAnnotations));
    ro.observe(img);
    resizeObserverRef.current = ro;

    return () => {
      window.removeEventListener("resize", handleResize);
      resizeObserverRef.current?.disconnect();
    };
  }, [open, image]);

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: "fixed",
          inset: 0,
          backgroundColor: "rgba(0,0,0,0.6)",
          backdropFilter: "blur(4px)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          p: { xs: 2, sm: 4 },
        }}
      >
        <Box
          sx={{
            position: "relative",
            backgroundColor: "#fff",
            borderRadius: 3,
            boxShadow: "0 8px 40px rgba(0,0,0,0.6)",
            p: 3,
            width: { xs: "95vw", sm: "85vw", md: "70vw" },
            maxHeight: "90vh",
            overflowY: "auto",
          }}
        >
          <IconButton
            onClick={onClose}
            sx={{
              position: "absolute",
              top: 8,
              right: 8,
              bgcolor: "rgba(255,255,255,0.85)",
              "&:hover": { bgcolor: "rgba(255,255,255,1)" },
            }}
          >
            <Close />
          </IconButton>

          <Typography
            variant="h5"
            fontWeight="bold"
            textAlign="center"
            marginTop={2}
            marginBottom={4}
            gutterBottom
          >
            {image.filename}
          </Typography>

          <Box sx={{ position: "relative", width: "100%" }}>
            <img
              ref={imgRef}
              src={image.image_url}
              alt={image.filename}
              style={{
                width: "100%",
                display: "block",
                borderRadius: 8,
              }}
            />

            <canvas
              ref={canvasRef}
              style={{
                position: "absolute",
                inset: 0,
                pointerEvents: "none",
              }}
            />
          </Box>
        </Box>

        {/* Navigation Controls */}
        <IconButton
          onClick={() => onNavigate("prev")}
          sx={{
            position: "fixed",
            left: { xs: 10, sm: 20 },
            top: "50%",
            transform: "translateY(-50%)",
            bgcolor: "rgba(255,255,255,0.85)",
            width: 56,
            height: 56,
            "&:hover": { bgcolor: "rgba(255,255,255,1)" },
            boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
          }}
        >
          <ArrowBack fontSize="large" />
        </IconButton>

        <IconButton
          onClick={() => onNavigate("next")}
          sx={{
            position: "fixed",
            right: { xs: 10, sm: 20 },
            top: "50%",
            transform: "translateY(-50%)",
            bgcolor: "rgba(255,255,255,0.85)",
            width: 56,
            height: 56,
            "&:hover": { bgcolor: "rgba(255,255,255,1)" },
            boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
          }}
        >
          <ArrowForward fontSize="large" />
        </IconButton>
      </Box>
    </Modal>
  );
};

export default SampleImageModal;
