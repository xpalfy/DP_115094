import React from "react";
import {
  Box,
  Paper,
  Typography,
  Tooltip,
  CircularProgress,
} from "@mui/material";

interface AverageImagesGridProps {
  images: Record<string, string>;
  loading: boolean;
  onSelect: (classKey: string) => void;
}

const AverageImagesGrid: React.FC<AverageImagesGridProps> = ({
  images,
  loading,
  onSelect,
}) => {
  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          mt: 6,
        }}
      >
        <CircularProgress color="primary" />
      </Box>
    );
  }

  const keys = Object.keys(images);

  if (keys.length === 0) {
    return (
      <Typography variant="body1" color="text.secondary" sx={{ mt: 4 }}>
        No average images found.
      </Typography>
    );
  }

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
      {keys.map((cls) => (
        <Tooltip key={cls} title={`Class: ${cls}`} arrow>
          <Paper
            elevation={6}
            onClick={() => onSelect(cls)}
            sx={{
              p: 2,
              borderRadius: 3,
              textAlign: "center",
              width: 160,
              transition: "all 0.3s ease",
              cursor: "pointer",
              "&:hover": {
                transform: "scale(1.05)",
                boxShadow: "0 8px 25px rgba(0,0,0,0.2)",
              },
            }}
          >
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              {cls}
            </Typography>

            <img
              src={images[cls]}
              alt={`Average ${cls}`}
              style={{
                width: "100%",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                objectFit: "contain",
                display: "block",
              }}
            />
          </Paper>
        </Tooltip>
      ))}
    </Box>
  );
};

export default AverageImagesGrid;
