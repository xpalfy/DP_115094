from rfdetr import RFDETRSegSmall

DATASET_DIR = "./dataset/v6.4_coco_seg"
IMG_SIZE = 1024
EPOCHS = 100
BATCH = 8
PATIENCE = 25
DEVICE = "cuda"

if __name__ == "__main__":
    m = RFDETRSegSmall()

    m.train(
        dataset_dir=DATASET_DIR,
        img_size=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        patience=PATIENCE,
        output_dir="../runs/rf_detr/train_rf-detr-seg-small",
        run_name="v1_rf-detr-seg-small",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/rf_detr/train_rf-detr-seg-small/v1_rf-detr-seg-small\n")