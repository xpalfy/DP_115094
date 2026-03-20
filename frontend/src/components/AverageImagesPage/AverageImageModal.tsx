import React from "react";
import { Box, Typography, Modal, IconButton } from "@mui/material";
import { ArrowBack, ArrowForward, Close } from "@mui/icons-material";

interface AverageImageModalProps {
  open: boolean;
  selectedClass: string | null;
  images: Record<string, string>;
  onClose: () => void;
  onNavigate: (direction: "prev" | "next") => void;
}

const AverageImageModal: React.FC<AverageImageModalProps> = ({
  open,
  selectedClass,
  images,
  onClose,
  onNavigate,
}) => {
  if (!selectedClass) return null;

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: "fixed",
          inset: 0,
          backgroundColor: "rgba(0,0,0,0.5)",
          backdropFilter: "blur(4px)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 1300,
          p: { xs: 2, sm: 4 },
        }}
      >
        <Box
          sx={{
            position: "relative",
            backgroundColor: "#fff",
            borderRadius: 3,
            boxShadow: "0 8px 40px rgba(0,0,0,0.6)",
            p: { xs: 2, sm: 3 },
            width: { xs: "90vw", sm: "80vw", md: "60vw", lg: "50vw" },
            maxHeight: { xs: "80vh", md: "90vh" },
            overflow: "auto",
          }}
        >
          <IconButton
            onClick={onClose}
            sx={{
              position: "absolute",
              top: 8,
              right: 8,
              bgcolor: "rgba(255,255,255,0.8)",
              "&:hover": { bgcolor: "rgba(255,255,255,1)" },
            }}
          >
            <Close />
          </IconButton>

          <Typography
            variant="h5"
            fontWeight="bold"
            sx={{ mt: 2, mb: 4, textAlign: "center" }}
          >
            {selectedClass}
          </Typography>

          <Box
            component="img"
            src={images[selectedClass]}
            alt={`Average ${selectedClass}`}
            sx={{
              width: "80%",
              maxHeight: { xs: "60vh", sm: "70vh", md: "75vh" },
              objectFit: "contain",
              borderRadius: 2,
              marginBottom: 2,
              marginTop: 1,
              boxShadow: "0 6px 20px rgba(0,0,0,0.25)",
              display: "block",
              mx: "auto",
            }}
          />
        </Box>

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
            borderRadius: "50%",
            boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
            "&:hover": { bgcolor: "rgba(255,255,255,1)" },
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
            borderRadius: "50%",
            boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
            "&:hover": { bgcolor: "rgba(255,255,255,1)" },
          }}
        >
          <ArrowForward fontSize="large" />
        </IconButton>
      </Box>
    </Modal>
  );
};

export default AverageImageModal;
