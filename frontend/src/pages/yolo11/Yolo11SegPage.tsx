import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo11SegPage: React.FC = () => {
  return (
    <DetectionPage
      modes={[
        "yolo11n-seg",
        "yolo11s-seg",
        "yolo11m-seg",
        "yolo11l-seg",
        "best",
      ]}
      title="YOLOv11 Object Segmentation"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
    />
  );
};

export default Yolo11SegPage;
