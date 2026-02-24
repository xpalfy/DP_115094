import React from "react";
import DetectionPage from "../../DetectionPage";
import frFlag from "../../../assets/images/fr.png";

const Yolo11SegPageFrench: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo11n-seg-french",
        "yolo11s-seg-french",
        "yolo11m-seg-french",
        "yolo11l-seg-french",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={frFlag}
            alt="FR"
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

export default Yolo11SegPageFrench;
