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
import Yolo12Page from "../pages/yolo12/Yolo12Page";
import Yolo11SegPage from "../pages/yolo11/Yolo11SegPage";
import Yolo11Page from "../pages/yolo11/Yolo11Page";
import Yolo8SegPage from "../pages/yolov8/Yolo8SegPage";
import Yolo8Page from "../pages/yolov8/Yolo8Page";
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
      case "/yolo8":
        dispatch(setDetectionMode("yolov8n_german"));
        break;
      case "/yolo8-seg":
        dispatch(setDetectionMode("yolov8n-seg_german"));
        break;
      case "/yolo11":
        dispatch(setDetectionMode("yolo11n_german"));
        break;
      case "/yolo11-seg":
        dispatch(setDetectionMode("yolo11n-seg_german"));
        break;
      case "/yolo12":
        dispatch(setDetectionMode("yolo12n_german"));
        break;
      case "/ocr":
        dispatch(setDetectionMode("easyocr"));
        break;
      case "/":
        dispatch(setDetectionMode("yolov8n_german"));
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
          <Route path="/" element={<Yolo8Page />} />
          <Route path="/yolo8" element={<Yolo8Page />} />
          <Route path="/yolo8-seg" element={<Yolo8SegPage />} />
          <Route path="/yolo11" element={<Yolo11Page />} />
          <Route path="/yolo11-seg" element={<Yolo11SegPage />} />
          <Route path="/yolo12" element={<Yolo12Page />} />
          <Route path="/ocr" element={<OcrPage />} />
          <Route path="/average" element={<AverageImagesPage />} />
          <Route path="/sample-images" element={<SampleImagesPage />} />
        </Routes>
      </Box>
    </>
  );
};

export default Layout;
