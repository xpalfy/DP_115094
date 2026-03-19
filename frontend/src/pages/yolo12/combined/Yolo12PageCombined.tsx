import React from "react";
import DetectionPage from "../../DetectionPage";
import combinedFlag from "../../../assets/images/combined.png";

const Yolo12PageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo12n-combined",
        "yolo12s-combined",
        "yolo12m-combined",
        "yolo12l-combined",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={combinedFlag}
            alt="Combined"
            style={{ width: 30, borderRadius: 3 }}
          />
          YOLOv12 Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo12PageCombined;
