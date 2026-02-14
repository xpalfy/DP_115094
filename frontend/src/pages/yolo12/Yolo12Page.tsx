import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo12Page: React.FC = () => {
  return (
    <DetectionPage
      modes={["yolo12n", "yolo12s", "yolo12m", "yolo12l"]}
      title="YOLOv12 Object Detection"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo12Page;
