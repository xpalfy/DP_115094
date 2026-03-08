import React from "react";
import DetectionPage from "../../DetectionPage";
import frFlag from "../../../assets/images/fr.png";
import deFlag from "../../../assets/images/de.png";

const Yolo26SegPageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo26n-seg-combined",
        "yolo26s-seg-combined",
        "yolo26m-seg-combined",
        "yolo26l-seg-combined",
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
          YOLOv26 Object Segmentation
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo26SegPageCombined;
