from rfdetr import RFDETRSegLarge

DATASET_DIR = "./dataset/v6.4_coco_seg"
IMG_SIZE = 1024
EPOCHS = 500
PATIENCE = 100
BATCH = 4
DEVICE = "cuda"

if __name__ == "__main__":
    m = RFDETRSegLarge()

    m.train(
        dataset_dir=DATASET_DIR,
        img_size=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        patience=PATIENCE,
        output_dir="../runs/rf_detr/train_rf-detr-seg-large",
        run_name="v1_rf-detr-seg-large",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/rf_detr/train_rf-detr-seg-large/v1_rf-detr-seg-large\n")