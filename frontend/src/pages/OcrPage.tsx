import React from "react";
import DetectionPage from "./DetectionPage";

const OcrPage = () => (
  <DetectionPage
    modes={["pytesseract", "easyocr"]}
    title="OCR Text Recognition"
    gradient="linear-gradient(135deg, #43cea2, #185a9d)"
    polygon={false}
  />
);

export default OcrPage;
