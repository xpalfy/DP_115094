from rfdetr import RFDETRBase

DATASET_DIR = "./dataset/v6.5_coco"
IMG_SIZE = 1024
EPOCHS = 250
PATIENCE = 50
BATCH = 4
DEVICE = "cuda"

if __name__ == "__main__":
    m = RFDETRBase()

    m.train(
        dataset_dir=DATASET_DIR,
        img_size=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        patience=PATIENCE,
        output_dir="../runs/rf_detr/train_rf-detr-base",
        run_name="v1_rf-detr-base",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/rf_detr/train_rf-detr-base/v1_rf-detr-base\n")