import React from "react";
import DetectionPage from "../../DetectionPage";
import combinedFlag from "../../../assets/images/combined.png";

const Yolo11SegPageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo11n-seg-combined",
        "yolo11s-seg-combined",
        "yolo11m-seg-combined",
        "yolo11l-seg-combined",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={combinedFlag}
            alt="Combined"
            style={{ width: 28, height: 20, borderRadius: 3 }}
          />
          YOLOv11 Object Segmentation
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo11SegPageCombined;
