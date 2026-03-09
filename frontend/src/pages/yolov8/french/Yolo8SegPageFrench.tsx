import React from "react";
import DetectionPage from "../../DetectionPage";
import frFlag from "../../../assets/images/fr.png";

const Yolo8SegPageFrench: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n-seg-french",
        "yolov8s-seg-french",
        "yolov8m-seg-french",
        "yolov8l-seg-french",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img src={frFlag} alt="FR" style={{ width: 30, borderRadius: 3 }} />
          YOLOv8 Object Segmentation
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo8SegPageFrench;
