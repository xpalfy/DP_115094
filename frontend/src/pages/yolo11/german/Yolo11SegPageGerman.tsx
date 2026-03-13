import React from "react";
import DetectionPage from "../../DetectionPage";
import deFlag from "../../../assets/images/de.png";

const Yolo11SegPageGerman: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo11n-seg-german",
        "yolo11s-seg-german",
        "yolo11m-seg-german",
        "yolo11l-seg-german",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img src={deFlag} alt="DE" style={{ width: 30, borderRadius: 3 }} />
          YOLOv11 Object Segmentation
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo11SegPageGerman;
