import React from "react";
import DetectionPage from "../../DetectionPage";
import deFlag from "../../../assets/images/de.png";

const Yolo12PageGerman: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo12n-german",
        "yolo12s-german",
        "yolo12m-german",
        "yolo12l-german",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img src={deFlag} alt="DE" style={{ width: 28, borderRadius: 3 }} />
          YOLOv12 Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo12PageGerman;
