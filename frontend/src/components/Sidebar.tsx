import React, { useState } from "react";
import {
  Drawer,
  Box,
  Typography,
  IconButton,
  Divider,
  List,
  ListItemButton,
  ListItemText,
  Collapse,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import { Link, useLocation } from "react-router-dom";

const drawerWidth = 240;

const Sidebar = ({ open, onClose }: { open: boolean; onClose: () => void }) => {
  const location = useLocation();
  const active = (path: string) => location.pathname === path;

  // State for collapsible sections
  const [openYolo8, setOpenYolo8] = useState(true);
  const [openYolo11, setOpenYolo11] = useState(false);
  const [openYolo12, setOpenYolo12] = useState(false);

  return (
    <Drawer
      anchor="left"
      open={open}
      onClose={onClose}
      sx={{
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          background: "linear-gradient(180deg, #2193b0, #6dd5ed)",
          color: "#fff",
          borderRight: "none",
          boxShadow: "4px 0 20px rgba(0,0,0,0.2)",
        },
      }}
    >
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          px: 2,
          py: 1,
        }}
      >
        <Typography variant="subtitle1" fontWeight="bold" sx={{ pr: 2 }}>
          Xpalfy
        </Typography>
        <IconButton onClick={onClose} sx={{ color: "white" }}>
          <CloseIcon />
        </IconButton>
      </Box>

      <Divider sx={{ borderColor: "rgba(255,255,255,0.3)" }} />

      {/* Navigation */}
      <List>
        {/* YOLOv8 Section */}
        <ListItemButton onClick={() => setOpenYolo8(!openYolo8)}>
          <ListItemText primary="YOLOv8 Models" />
          {openYolo8 ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openYolo8} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <SidebarLink
              to="/yolo8"
              label="Character Detection (YOLOv8)"
              active={active("/yolo8") || active("/")}
              onClick={onClose}
            />
            <SidebarLink
              to="/yolo8-seg"
              label="Character Segmentation (YOLOv8)"
              active={active("/yolo8-seg")}
              onClick={onClose}
            />
          </List>
        </Collapse>

        {/* YOLOv11 Section */}
        <ListItemButton onClick={() => setOpenYolo11(!openYolo11)}>
          <ListItemText primary="YOLOv11 Models" />
          {openYolo11 ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openYolo11} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <SidebarLink
              to="/yolo11"
              label="Character Detection (YOLOv11)"
              active={active("/yolo11")}
              onClick={onClose}
            />
            <SidebarLink
              to="/yolo11-seg"
              label="Character Segmentation (YOLOv11)"
              active={active("/yolo11-seg")}
              onClick={onClose}
            />
          </List>
        </Collapse>

        {/* YOLOv12 Section */}
        <ListItemButton onClick={() => setOpenYolo12(!openYolo12)}>
          <ListItemText primary="YOLOv12 Models" />
          {openYolo12 ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openYolo12} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <SidebarLink
              to="/yolo12"
              label="Character Detection (YOLOv12)"
              active={active("/yolo12")}
              onClick={onClose}
            />
          </List>
        </Collapse>

        {/* OCR */}
        <Divider sx={{ borderColor: "rgba(255,255,255,0.3)", my: 1 }} />
        <SidebarLink
          to="/ocr"
          label="Optical Character Recognition (OCR)"
          active={active("/ocr")}
          onClick={onClose}
        />
      </List>

      {/* Footer */}
      <Box sx={{ flexGrow: 1 }} />
      <Divider sx={{ borderColor: "rgba(255,255,255,0.2)" }} />
      <Box sx={{ textAlign: "center", py: 2 }}>
        <Typography variant="body2" color="rgba(255,255,255,0.8)">
          © 2025 Slovak University of Technology in Bratislava
        </Typography>
      </Box>
    </Drawer>
  );
};

// Reusable sidebar link
const SidebarLink = ({
  to,
  label,
  active,
  onClick,
}: {
  to: string;
  label: string;
  active: boolean;
  onClick: () => void;
}) => (
  <ListItemButton
    component={Link}
    to={to}
    onClick={onClick}
    selected={active}
    sx={{
      pl: 4,
      borderRadius: 1,
      mx: 1,
      my: 0.3,
      "&.Mui-selected": {
        backgroundColor: "rgba(255,255,255,0.2)",
        fontWeight: "bold",
      },
      "&:hover": {
        backgroundColor: "rgba(255,255,255,0.15)",
      },
    }}
  >
    <ListItemText
      primaryTypographyProps={{
        sx: {
          color: active ? "#fff" : "rgba(255,255,255,0.9)",
          fontWeight: active ? "bold" : "normal",
          fontSize: 14,
        },
      }}
      primary={label}
    />
  </ListItemButton>
);

export default Sidebar;
