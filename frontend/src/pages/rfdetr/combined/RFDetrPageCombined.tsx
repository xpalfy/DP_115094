import React from "react";
import DetectionPage from "../../DetectionPage";
import combinedFlag from "../../../assets/images/combined.png";

const RFDetrPageCombined: React.FC = () => {
  return (
    <DetectionPage
      type="rfdetr"
      modes={[
        "rfdetr-nano-combined",
        "rfdetr-small-combined",
        "rfdetr-base-combined",
        "rfdetr-medium-combined",
        "rfdetr-large-combined",
      ]}
      title={
        <span style={{ display: "inline-flex", alignItems: "center", gap: 20 }}>
          <img
            src={combinedFlag}
            alt="Combined"
            style={{ width: 28, borderRadius: 3 }}
          />
          RFDetr Object Detection
        </span>
      }
      gradient="linear-gradient(135deg, #43cea2, #185a9d)"
      polygon={false}
    />
  );
};

export default RFDetrPageCombined;
