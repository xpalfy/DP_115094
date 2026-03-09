import React from "react";
import DetectionPage from "../../DetectionPage";
import combinedFlag from "../../../assets/images/combined.png";

const Yolo26PageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo26n-combined",
        "yolo26s-combined",
        "yolo26m-combined",
        "yolo26l-combined",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={combinedFlag}
            alt="Combined"
            style={{ width: 28, borderRadius: 3 }}
          />
          YOLOv26 Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo26PageCombined;
