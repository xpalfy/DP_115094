import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo8Page: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={["yolov8n", "yolov8s", "yolov8m", "yolov8l"]}
      title="YOLOv8 Object Detection"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo8Page;
