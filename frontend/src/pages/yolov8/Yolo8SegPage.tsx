import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo8SegPage: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolov8n-seg_german",
        "yolov8s-seg_german",
        "yolov8m-seg_german",
        "yolov8l-seg_german",
        "yolov8n-seg_french",
        "yolov8s-seg_french",
        "yolov8m-seg_french",
        "yolov8l-seg_french",
      ]}
      title="YOLOv8 Object Segmentation"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default Yolo8SegPage;
