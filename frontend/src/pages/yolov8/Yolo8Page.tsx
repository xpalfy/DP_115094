import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo8Page: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n_german",
        "yolov8s_german",
        "yolov8m_german",
        "yolov8l_german",
        "yolov8n_french",
        "yolov8s_french",
        "yolov8m_french",
        "yolov8l_french",
      ]}
      title="YOLOv8 Object Detection"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo8Page;
