from rfdetr import RFDETRSegMedium

DATASET_DIR = "./dataset/v6.4_coco_seg"
IMG_SIZE = 1024
EPOCHS = 250
PATIENCE = 50
BATCH = 4
DEVICE = "cuda"

if __name__ == "__main__":
    m = RFDETRSegMedium()

    m.train(
        dataset_dir=DATASET_DIR,
        img_size=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        patience=PATIENCE,
        output_dir="../runs/rf_detr/train_rf-detr-seg-medium",
        run_name="v1_rf-detr-seg-medium",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/rf_detr/train_rf-detr-seg-medium/v1_rf-detr-seg-medium\n")