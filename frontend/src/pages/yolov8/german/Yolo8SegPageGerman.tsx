import React from "react";
import DetectionPage from "../../DetectionPage";

const Yolo8SegPageGerman: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n-seg-german",
        "yolov8s-seg-german",
        "yolov8m-seg-german",
        "yolov8l-seg-german",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src="https://flagcdn.com/w40/de.png"
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

export default Yolo8SegPageGerman;
