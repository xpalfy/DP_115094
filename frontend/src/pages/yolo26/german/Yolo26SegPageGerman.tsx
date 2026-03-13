import React from "react";
import DetectionPage from "../../DetectionPage";
import deFlag from "../../../assets/images/de.png";

const Yolo26SegPageGerman: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo26n-seg-german",
        "yolo26s-seg-german",
        "yolo26m-seg-german",
        "yolo26l-seg-german",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img src={deFlag} alt="DE" style={{ width: 30, borderRadius: 3 }} />
          YOLOv26 Object Segmentation
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo26SegPageGerman;
