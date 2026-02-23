import React, { useEffect } from "react";
import { Box } from "@mui/material";
import { Routes, Route, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../app/store";
import { clearImage } from "../features/image/imageSlice";
import {
  closeSidebar,
  setDetectionMode,
  setUseSahi,
  setConfidence,
  setUsePolygon,
} from "../features/ui/uiSlice";
import Header from "./Header";
import Sidebar from "./Sidebar";
import OcrPage from "../pages/OcrPage";
import Yolo12PageGerman from "../pages/yolo12/german/Yolo12PageGerman";
import Yolo11SegPageGerman from "../pages/yolo11/german/Yolo11SegPageGerman";
import Yolo11PageGerman from "../pages/yolo11/german/Yolo11PageGerman";
import Yolo8SegPageGerman from "../pages/yolov8/german/Yolo8SegPageGerman";
import Yolo8PageGerman from "../pages/yolov8/german/Yolo8PageGerman";
import Yolo12PageFrench from "../pages/yolo12/french/Yolo12PageFrench";
import Yolo11SegPageFrench from "../pages/yolo11/french/Yolo11SegPageFrench";
import Yolo11PageFrench from "../pages/yolo11/french/Yolo11PageFrench";
import Yolo8SegPageFrench from "../pages/yolov8/french/Yolo8SegPageFrench";
import Yolo8PageFrench from "../pages/yolov8/french/Yolo8PageFrench";
import AverageImagesPage from "../pages/AverageImagesPage";
import SampleImagesPage from "../pages/SampleImagesPage";

const Layout = () => {
  const location = useLocation();
  const dispatch = useDispatch();
  const open = useSelector((state: RootState) => state.ui.sidebarOpen);

  useEffect(() => {
    dispatch(clearImage());
    dispatch(closeSidebar());
    dispatch(setUseSahi(false));
    dispatch(setUsePolygon(false));
    dispatch(setConfidence(50));
    switch (location.pathname) {
      case "/yolo8-german":
        dispatch(setDetectionMode("yolov8n-german"));
        break;
      case "/yolo8-french":
        dispatch(setDetectionMode("yolov8n-french"));
        break;
      case "/yolo8-seg-german":
        dispatch(setDetectionMode("yolov8n-seg-german"));
        break;
      case "/yolo8-seg-french":
        dispatch(setDetectionMode("yolov8n-seg-french"));
        break;
      case "/yolo11-german":
        dispatch(setDetectionMode("yolo11n-german"));
        break;
      case "/yolo11-french":
        dispatch(setDetectionMode("yolo11n-french"));
        break;
      case "/yolo11-seg-german":
        dispatch(setDetectionMode("yolo11n-seg-german"));
        break;
      case "/yolo11-seg-french":
        dispatch(setDetectionMode("yolo11n-seg-french"));
        break;
      case "/yolo12-german":
        dispatch(setDetectionMode("yolo12n-german"));
        break;
      case "/yolo12-french":
        dispatch(setDetectionMode("yolo12n-french"));
        break;
      case "/ocr":
        dispatch(setDetectionMode("easyocr"));
        break;
      case "/":
        dispatch(setDetectionMode("yolov8n-german"));
        break;
      default:
        break;
    }
  }, [location.pathname, dispatch]);

  const handleDrawerClose = () => dispatch(closeSidebar());

  return (
    <>
      <Header />
      <Sidebar open={open} onClose={handleDrawerClose} />
      <Box component="main">
        <Routes>
          <Route path="/" element={<Yolo8PageGerman />} />
          <Route path="/yolo8-german" element={<Yolo8PageGerman />} />
          <Route path="/yolo8-seg-german" element={<Yolo8SegPageGerman />} />
          <Route path="/yolo11-german" element={<Yolo11PageGerman />} />
          <Route path="/yolo11-seg-german" element={<Yolo11SegPageGerman />} />
          <Route path="/yolo12-german" element={<Yolo12PageGerman />} />
          <Route path="/yolo8-french" element={<Yolo8PageFrench />} />
          <Route path="/yolo8-seg-french" element={<Yolo8SegPageFrench />} />
          <Route path="/yolo11-french" element={<Yolo11PageFrench />} />
          <Route path="/yolo11-seg-french" element={<Yolo11SegPageFrench />} />
          <Route path="/yolo12-french" element={<Yolo12PageFrench />} />
          <Route path="/ocr" element={<OcrPage />} />
          <Route path="/average" element={<AverageImagesPage />} />
          <Route path="/sample-images" element={<SampleImagesPage />} />
        </Routes>
      </Box>
    </>
  );
};

export default Layout;
