import React from "react";
import DetectionPage from "../../DetectionPage";
import frFlag from "../../../assets/images/fr.png";

const Yolo8PageFrench: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n-french",
        "yolov8s-french",
        "yolov8m-french",
        "yolov8l-french",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img src={frFlag} alt="FR" style={{ width: 28, borderRadius: 3 }} />
          YOLOv8 Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo8PageFrench;
