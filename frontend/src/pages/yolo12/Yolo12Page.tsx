import React from "react";
import DetectionPage from "../DetectionPage";

const Yolo12Page: React.FC = () => {
  return (
    <DetectionPage
      type="yolo"
      modes={[
        "yolo12n_german",
        "yolo12s_german",
        "yolo12m_german",
        "yolo12l_german",
        "yolo12n_french",
        "yolo12s_french",
        "yolo12m_french",
        "yolo12l_french",
      ]}
      title="YOLOv12 Object Detection"
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default Yolo12Page;
