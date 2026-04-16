import cv2
import numpy as np
from PIL import Image

from sahi.models.base import DetectionModel
from sahi.prediction import ObjectPrediction

from rfdetr import (
    RFDETRBase,
    RFDETRNano,
    RFDETRSmall,
    RFDETRMedium,
    RFDETRLarge,
    RFDETRSegNano,
    RFDETRSegSmall
)


class RFDETRDetectionModel(DetectionModel):

    def load_model(self):
        """Load appropriate RF-DETR model based on model path."""

        path = self.model_path
        device = self.device if isinstance(self.device, str) else self.device.type

        model_cls = self._select_model_class(path)

        self.model = model_cls(
            pretrain_weights=path,
            num_classes=len(self.category_mapping),
            device=device
        )

        self.model.optimize_for_inference()

    def _select_model_class(self, path: str):
        """Select correct model class from path name."""

        if "seg-nano" in path:
            return RFDETRSegNano
        if "seg-small" in path:
            return RFDETRSegSmall
        if "nano" in path:
            return RFDETRNano
        if "small" in path:
            return RFDETRSmall
        if "medium" in path:
            return RFDETRMedium
        if "large" in path:
            return RFDETRLarge

        return RFDETRBase

    def perform_inference(self, image: np.ndarray):
        """Run inference on input image."""

        image = Image.fromarray(image).convert("RGB")

        self._original_predictions = self.model.predict(
            image,
            threshold=float(self.confidence_threshold)
        )

    def convert_original_predictions(self, shift_amount=[0, 0], full_shape=None):
        """Convert model outputs to SAHI ObjectPrediction format."""

        preds = self._original_predictions
        object_prediction_list = []

        masks = self._get_masks(preds)

        for i, (bbox, score, class_id) in enumerate(zip(
                preds.xyxy,
                preds.confidence,
                preds.class_id
        )):

            x1, y1, x2, y2 = bbox
            cid = int(class_id)

            segmentation = self._extract_segmentation(masks, i)

            object_prediction_list.append(
                ObjectPrediction(
                    bbox=[float(x1), float(y1), float(x2), float(y2)],
                    category_id=cid,
                    category_name=self.category_mapping.get(str(cid), str(cid)),
                    score=float(score),
                    segmentation=segmentation,
                    shift_amount=shift_amount,
                    full_shape=full_shape
                )
            )

        self._object_prediction_list_per_image = [object_prediction_list]

    def _get_masks(self, preds):
        """Safely extract masks from predictions."""
        masks = getattr(preds, "masks", None)
        if masks is None:
            masks = getattr(preds, "mask", None)
        return masks

    def _extract_segmentation(self, masks, index):
        """Convert mask to polygon segmentation."""

        if masks is None or index >= len(masks):
            return None

        mask = (masks[index] > 0).astype(np.uint8)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        best = max(contours, key=cv2.contourArea)

        return [best.reshape(-1).astype(float).tolist()]