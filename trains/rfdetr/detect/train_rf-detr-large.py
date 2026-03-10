from rfdetr import RFDETRLarge

DATASET_DIR = "./dataset/v6.5_coco"
IMG_SIZE = 1024
EPOCHS = 500
PATIENCE = 100
BATCH = 4
WORKERS = 8
DEVICE = "cuda"
AMP = True

if __name__ == "__main__":
    m = RFDETRLarge()

    m.train(
        dataset_dir=DATASET_DIR,
        img_size=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        patience=PATIENCE,
        workers=WORKERS,
        amp=AMP,
        output_dir="../runs/rf_detr/train_rf-detr-large",
        run_name="v1_rf-detr-large",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/rf_detr/train_rf-detr-large/v1_rf-detr-large\n")