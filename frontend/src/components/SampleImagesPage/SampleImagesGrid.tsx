import React from "react";
import { Box, Paper, Typography, Tooltip } from "@mui/material";
import { SampleImage } from "../../pages/SampleImagesPage";

interface Props {
  images: SampleImage[];
  onSelect: (index: number) => void;
}

const SampleImagesGrid: React.FC<Props> = ({ images, onSelect }) => {
  if (images.length === 0)
    return (
      <Typography variant="body1" color="text.secondary" sx={{ mt: 4 }}>
        No sample images found.
      </Typography>
    );

  return (
    <Box
      sx={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: 3,
        mt: 3,
      }}
    >
      {images.map((img, index) => (
        <Tooltip key={img.filename} title={img.filename} arrow>
          <Paper
            elevation={6}
            onClick={() => onSelect(index)}
            sx={{
              p: 2,
              borderRadius: 3,
              textAlign: "center",
              width: 220,
              transition: "all 0.3s ease",
              cursor: "pointer",
              "&:hover": { transform: "scale(1.05)" },
            }}
          >
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              {img.filename}
            </Typography>
            <img
              src={img.image_url}
              alt={img.filename}
              style={{
                width: "100%",
                borderRadius: "8px",
                objectFit: "contain",
              }}
            />
          </Paper>
        </Tooltip>
      ))}
    </Box>
  );
};

export default SampleImagesGrid;
