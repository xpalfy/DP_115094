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

        path = self.model_path

        if "seg-nano" in path:
            model_cls = RFDETRSegNano
        elif "seg-small" in path:
            model_cls = RFDETRSegSmall
        elif "nano" in path:
            model_cls = RFDETRNano
        elif "small" in path:
            model_cls = RFDETRSmall
        elif "medium" in path:
            model_cls = RFDETRMedium
        elif "large" in path:
            model_cls = RFDETRLarge
        else:
            model_cls = RFDETRBase

        device = self.device if isinstance(self.device, str) else self.device.type

        self.model = model_cls(
            pretrain_weights=path,
            num_classes=len(self.category_mapping),
            device=device
        )

        self.model.optimize_for_inference()


    def perform_inference(self, image: np.ndarray):

        image = Image.fromarray(image).convert("RGB")

        self._original_predictions = self.model.predict(
            image,
            threshold=float(self.confidence_threshold)
        )


    def convert_original_predictions(self, shift_amount=[0, 0], full_shape=None):

        preds = self._original_predictions

        object_prediction_list = []

        for xyxy, score, class_id in zip(
            preds.xyxy,
            preds.confidence,
            preds.class_id
        ):

            x1, y1, x2, y2 = xyxy
            cid = int(class_id)

            object_prediction_list.append(

                ObjectPrediction(
                    bbox=[float(x1), float(y1), float(x2), float(y2)],
                    category_id=cid,
                    category_name=self.category_mapping.get(str(cid), str(cid)),
                    score=float(score),
                    shift_amount=shift_amount,
                    full_shape=full_shape
                )

            )

        self._object_prediction_list_per_image = [object_prediction_list]