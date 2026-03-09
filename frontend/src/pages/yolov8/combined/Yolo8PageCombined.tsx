import React from "react";
import DetectionPage from "../../DetectionPage";
import combinedFlag from "../../../assets/images/combined.png";

const Yolo8PageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n-combined",
        "yolov8s-combined",
        "yolov8m-combined",
        "yolov8l-combined",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={combinedFlag}
            alt="Combined"
            style={{ width: 30, borderRadius: 3 }}
          />
          YOLOv8 Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo8PageCombined;
