import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo11SegPage: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo11n-seg_german",
        "yolo11s-seg_german",
        "yolo11m-seg_german",
        "yolo11l-seg_german",
        "yolo11n-seg_french",
        "yolo11s-seg_french",
        "yolo11m-seg_french",
        "yolo11l-seg_french",
      ]}
      title="YOLOv11 Object Segmentation"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo11SegPage;
