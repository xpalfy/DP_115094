from rfdetr import RFDETRNano

DATASET_DIR = "./dataset/v6.5_coco"
IMG_SIZE = 1024
EPOCHS = 50
BATCH = 8
DEVICE = "cuda"

if __name__ == "__main__":
    m = RFDETRNano()

    m.train(
        dataset_dir=DATASET_DIR,
        img_size=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        output_dir="../runs/rf_detr/train_rf-detr-nano",
        run_name="v1_rf-detr-nano",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/rf_detr/train_rf-detr-nano/v1_rf-detr-nano\n")