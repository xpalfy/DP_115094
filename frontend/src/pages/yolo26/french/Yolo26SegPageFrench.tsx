import React from "react";
import DetectionPage from "../../DetectionPage";
import frFlag from "../../../assets/images/fr.png";

const Yolo26SegPageFrench: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo26n-seg-french",
        "yolo26s-seg-french",
        "yolo26m-seg-french",
        "yolo26l-seg-french",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={frFlag}
            alt="FR"
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

export default Yolo26SegPageFrench;
