import React from "react";
import DetectionPage from "../../DetectionPage";
import frFlag from "../../../assets/images/fr.png";
import deFlag from "../../../assets/images/de.png";

const Yolo8SegPageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n-seg-combined",
        "yolov8s-seg-combined",
        "yolov8m-seg-combined",
        "yolov8l-seg-combined",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={frFlag}
            alt="FR"
            style={{ width: 28, height: 20, borderRadius: 3 }}
          />
          <img
            src={deFlag}
            alt="DE"
            style={{ width: 28, height: 20, borderRadius: 3 }}
          />
          YOLOv8 Object Segmentation
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo8SegPageCombined;
