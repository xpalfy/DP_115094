import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo8SegPage: React.FC = () => {
  return (
    <DetectionPage
      modes={["yolov8n-seg", "yolov8s-seg", "yolov8m-seg", "yolov8l-seg"]}
      title="YOLOv8 Object Segmentation"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo8SegPage;
