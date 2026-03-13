import React from "react";
import DetectionPage from "../../DetectionPage";
import combinedFlag from "../../../assets/images/combined.png";

const RFDetrSegPageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="rfdetr-seg"
      modes={["rfdetr-nano-seg-combined", "rfdetr-small-seg-combined"]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={combinedFlag}
            alt="Combined"
            style={{ width: 30, borderRadius: 3 }}
          />
          RFDetr Object Segmentation
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={true}
    />
  );
};

export default RFDetrSegPageCombined;
