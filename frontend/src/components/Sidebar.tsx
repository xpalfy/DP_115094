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
import deFlag from "../assets/images/de.png";
import frFlag from "../assets/images/fr.png";
import combinedFlag from "../assets/images/combined.png";

const drawerWidth = 240;

const Sidebar = ({ open, onClose }: { open: boolean; onClose: () => void }) => {
  const location = useLocation();
  const active = (path: string) => location.pathname === path;

  // Top-level collapsibles
  const [openYolo8, setOpenYolo8] = useState(false);
  const [openYolo11, setOpenYolo11] = useState(false);
  const [openYolo12, setOpenYolo12] = useState(false);
  const [openYolo26, setOpenYolo26] = useState(false);
  const [openRFDetr, setOpenRFDetr] = useState(false);

  // Language-level collapsibles (YOLOv8)
  const [openY8German, setOpenY8German] = useState(false);
  const [openY8French, setOpenY8French] = useState(false);
  const [openY8Combined, setOpenY8Combined] = useState(false);

  // Language-level collapsibles (YOLOv11)
  const [openY11German, setOpenY11German] = useState(false);
  const [openY11French, setOpenY11French] = useState(false);
  const [openY11Combined, setOpenY11Combined] = useState(false);

  // Language-level collapsibles (YOLOv12)
  const [openY12German, setOpenY12German] = useState(false);
  const [openY12French, setOpenY12French] = useState(false);
  const [openY12Combined, setOpenY12Combined] = useState(false);

  // Language-level collapsibles (YOLOv26)
  const [openY26German, setOpenY26German] = useState(false);
  const [openY26French, setOpenY26French] = useState(false);
  const [openY26Combined, setOpenY26Combined] = useState(false);

  // Language-level collapsibles (RFDetr)
  const [openRFDetrCombined, setOpenRFDetrCombined] = useState(false);

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
            <SectionGroup
              label="German"
              flag={deFlag}
              open={openY8German}
              onToggle={() => setOpenY8German((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo8-german"
                label="Character Detection (YOLOv8)"
                active={active("/yolo8-german") || active("/")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo8-seg-german"
                label="Character Segmentation (YOLOv8)"
                active={active("/yolo8-seg-german")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="French"
              flag={frFlag}
              open={openY8French}
              onToggle={() => setOpenY8French((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo8-french"
                label="Character Detection (YOLOv8)"
                active={active("/yolo8-french")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo8-seg-french"
                label="Character Segmentation (YOLOv8)"
                active={active("/yolo8-seg-french")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="Combined"
              flag={combinedFlag}
              open={openY8Combined}
              onToggle={() => setOpenY8Combined((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo8-combined"
                label="Character Detection (YOLOv8)"
                active={active("/yolo8-combined")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo8-seg-combined"
                label="Character Segmentation (YOLOv8)"
                active={active("/yolo8-seg-combined")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>
          </List>
        </Collapse>

        {/* YOLOv11 Section */}
        <ListItemButton onClick={() => setOpenYolo11(!openYolo11)}>
          <ListItemText primary="YOLOv11 Models" />
          {openYolo11 ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openYolo11} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <SectionGroup
              label="German"
              flag={deFlag}
              open={openY11German}
              onToggle={() => setOpenY11German((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo11-german"
                label="Character Detection (YOLOv11)"
                active={active("/yolo11-german")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo11-seg-german"
                label="Character Segmentation (YOLOv11)"
                active={active("/yolo11-seg-german")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="French"
              flag={frFlag}
              open={openY11French}
              onToggle={() => setOpenY11French((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo11-french"
                label="Character Detection (YOLOv11)"
                active={active("/yolo11-french")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo11-seg-french"
                label="Character Segmentation (YOLOv11)"
                active={active("/yolo11-seg-french")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="Combined"
              flag={combinedFlag}
              open={openY11Combined}
              onToggle={() => setOpenY11Combined((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo11-combined"
                label="Character Detection (YOLOv11)"
                active={active("/yolo11-combined")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo11-seg-combined"
                label="Character Segmentation (YOLOv11)"
                active={active("/yolo11-seg-combined")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>
          </List>
        </Collapse>

        {/* YOLOv12 Section */}
        <ListItemButton onClick={() => setOpenYolo12(!openYolo12)}>
          <ListItemText primary="YOLOv12 Models" />
          {openYolo12 ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openYolo12} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <SectionGroup
              label="German"
              flag={deFlag}
              open={openY12German}
              onToggle={() => setOpenY12German((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo12-german"
                label="Character Detection (YOLOv12)"
                active={active("/yolo12-german")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="French"
              flag={frFlag}
              open={openY12French}
              onToggle={() => setOpenY12French((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo12-french"
                label="Character Detection (YOLOv12)"
                active={active("/yolo12-french")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="Combined"
              flag={combinedFlag}
              open={openY12Combined}
              onToggle={() => setOpenY12Combined((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo12-combined"
                label="Character Detection (YOLOv12)"
                active={active("/yolo12-combined")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>
          </List>
        </Collapse>

        {/* YOLOv26 Section */}
        <ListItemButton onClick={() => setOpenYolo26(!openYolo26)}>
          <ListItemText primary="YOLOv26 Models" />
          {openYolo26 ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openYolo26} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <SectionGroup
              label="German"
              flag={deFlag}
              open={openY26German}
              onToggle={() => setOpenY26German((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo26-german"
                label="Character Detection (YOLOv26)"
                active={active("/yolo26-german")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo26-seg-german"
                label="Character Segmentation (YOLOv26)"
                active={active("/yolo26-seg-german")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="French"
              flag={frFlag}
              open={openY26French}
              onToggle={() => setOpenY26French((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo26-french"
                label="Character Detection (YOLOv26)"
                active={active("/yolo26-french")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo26-seg-french"
                label="Character Segmentation (YOLOv26)"
                active={active("/yolo26-seg-french")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>

            <SectionGroup
              label="Combined"
              flag={combinedFlag}
              open={openY26Combined}
              onToggle={() => setOpenY26Combined((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/yolo26-combined"
                label="Character Detection (YOLOv26)"
                active={active("/yolo26-combined")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/yolo26-seg-combined"
                label="Character Segmentation (YOLOv26)"
                active={active("/yolo26-seg-combined")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>
          </List>
        </Collapse>

        {/* RFDetr Section */}
        <ListItemButton onClick={() => setOpenRFDetr(!openRFDetr)}>
          <ListItemText primary="RFDetr Models" />
          {openRFDetr ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={openRFDetr} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            <SectionGroup
              label="Combined"
              flag={combinedFlag}
              open={openRFDetrCombined}
              onToggle={() => setOpenRFDetrCombined((v) => !v)}
              level={1}
            >
              <SidebarLink
                to="/rfdetr-combined"
                label="Character Detection (RFDetr)"
                active={active("/rfdetr-combined")}
                onClick={onClose}
                level={2}
              />
              <SidebarLink
                to="/rfdetr-seg-combined"
                label="Character Segmentation (RFDetr)"
                active={active("/rfdetr-seg-combined")}
                onClick={onClose}
                level={2}
              />
            </SectionGroup>
          </List>
        </Collapse>

        {/* OCR */}
        <Divider sx={{ borderColor: "rgba(255,255,255,0.3)", my: 1 }} />
        <SidebarLink
          to="/ocr"
          label="Optical Character Recognition (OCR)"
          active={active("/ocr")}
          onClick={onClose}
          level={0}
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

/** 2nd-level group (e.g. German/French) with optional flag */
const SectionGroup = ({
  label,
  flag,
  open,
  onToggle,
  level,
  children,
}: {
  label: string;
  flag?: string;
  open: boolean;
  onToggle: () => void;
  level: 0 | 1 | 2;
  children: React.ReactNode;
}) => {
  const pl = level === 0 ? 2 : level === 1 ? 4 : 6;

  return (
    <>
      <ListItemButton onClick={onToggle} sx={{ pl }}>
        <ListItemText
          primary={
            <span
              style={{ display: "inline-flex", alignItems: "center", gap: 10 }}
            >
              {flag && (
                <img
                  src={flag}
                  alt={label}
                  style={{ width: 22, borderRadius: 2 }}
                />
              )}
              {label}
            </span>
          }
        />
        {open ? <ExpandLess /> : <ExpandMore />}
      </ListItemButton>

      <Collapse in={open} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          {children}
        </List>
      </Collapse>
    </>
  );
};

// Reusable sidebar link (supports nesting via level)
const SidebarLink = ({
  to,
  label,
  active,
  onClick,
  level,
}: {
  to: string;
  label: string;
  active: boolean;
  onClick: () => void;
  level: 0 | 1 | 2;
}) => {
  const pl = level === 0 ? 2 : level === 1 ? 6 : 8;

  return (
    <ListItemButton
      component={Link}
      to={to}
      onClick={onClick}
      selected={active}
      sx={{
        pl,
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
};

export default Sidebar;
