import React from "react";
import { Box, Typography } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { useDropzone } from "react-dropzone";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../../app/store";
import { setImage } from "../../features/image/imageSlice";

interface Props {
  onFileSelected: (file: File) => void;
}

const ImageUploader: React.FC<Props> = ({ onFileSelected }) => {
  const dispatch = useDispatch<AppDispatch>();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "image/png": [".png"],
      "image/jpeg": [".jpg", ".jpeg"],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (!file) return;

      onFileSelected(file);

      dispatch(
        setImage({
          filename: file.name,
          preview: URL.createObjectURL(file),
          type: file.type,
        })
      );
    },
  });

  return (
    <Box
      {...getRootProps()}
      sx={{
        mt: 4,
        border: "2px dashed #1976d2",
        borderRadius: 3,
        p: 6,
        cursor: "pointer",
        backgroundColor: isDragActive ? "#e3f2fd" : "#fafafa",
        transition: "0.25s",
        "&:hover": {
          backgroundColor: "#f5faff",
          borderColor: "#1565c0",
        },
      }}
    >
      <input {...getInputProps()} />
      <CloudUploadIcon sx={{ fontSize: 60, color: "#1976d2" }} />
      <Typography variant="h6" sx={{ mt: 2 }}>
        {isDragActive ? "Drop it here..." : "Drag & drop or click to upload"}
      </Typography>
    </Box>
  );
};

export default ImageUploader;
