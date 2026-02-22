import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo11Page: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo11n_german",
        "yolo11s_german",
        "yolo11m_german",
        "yolo11l_german",
        "yolo11n_french",
        "yolo11s_french",
        "yolo11m_french",
        "yolo11l_french",
      ]}
      title="YOLOv11 Object Detection and Segmentation"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo11Page;
