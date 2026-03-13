import React from "react";
import DetectionPage from "../../DetectionPage";
import deFlag from "../../../assets/images/de.png";

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
          <img src={deFlag} alt="DE" style={{ width: 30, borderRadius: 3 }} />
          YOLOv8 Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo8PageGerman;
