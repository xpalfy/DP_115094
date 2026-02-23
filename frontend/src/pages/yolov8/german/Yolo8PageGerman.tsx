import React from "react";
import DetectionPage from "../../DetectionPage";

const Yolo8PageGerman: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n-german",
        "yolov8s-german",
        "yolov8m-german",
        "yolov8l-german",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src="https://flagcdn.com/w40/de.png"
            alt="DE"
            style={{ width: 28, height: 20, borderRadius: 3 }}
          />
          YOLOv8 Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo8PageGerman;
