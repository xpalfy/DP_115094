import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo11Page: React.FC = () => {
  return (
    <DetectionPage
      modes={["yolo11n", "yolo11s", "yolo11m", "yolo11l"]}
      title="YOLOv11 Object Detection and Segmentation"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
    />
  );
};

export default Yolo11Page;
