import React from "react";
import { Modal, Box, Typography, Button } from "@mui/material";

interface CroppedModalProps {
  open: boolean;
  box: any | null;
  croppedSrc: string | null;
  onClose: () => void;
}

const CroppedModal: React.FC<CroppedModalProps> = ({
  open,
  box,
  croppedSrc,
  onClose,
}) => {
  if (!box) return null;

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          bgcolor: "rgba(255,255,255,0.97)",
          borderRadius: 3,
          p: 4,
          backdropFilter: "blur(4px)",
          textAlign: "center",
          outline: "none",
          maxWidth: "80vw",
          maxHeight: "85vh",
          overflowY: "auto",
        }}
      >
        <Typography variant="h6" fontWeight="bold" mb={2}>
          {box?.label || "Detected Region"}
        </Typography>

        {croppedSrc && (
          <img
            src={croppedSrc}
            alt="Cropped detection"
            style={{
              maxWidth: "80vw",
              maxHeight: "70vh",
              borderRadius: "12px",
              border: "3px solid #1976d2",
              boxShadow: "0 6px 20px rgba(0,0,0,0.35)",
              objectFit: "contain",
            }}
          />
        )}

        {box?.confidence && (
          <Typography variant="body2" color="text.secondary" mt={1}>
            Confidence: {(box.confidence * 100).toFixed(1)}%
          </Typography>
        )}
        {box?.class && (
          <Typography variant="body2" color="text.secondary" mt={1}>
            Class: {box.class}
          </Typography>
        )}

        <Button
          variant="contained"
          onClick={onClose}
          sx={{ mt: 3, px: 4, py: 1, fontWeight: "bold" }}
        >
          Close
        </Button>
      </Box>
    </Modal>
  );
};

export default CroppedModal;
