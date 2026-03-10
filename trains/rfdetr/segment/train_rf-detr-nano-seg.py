from rfdetr import RFDETRSegNano

DATASET_DIR = "./dataset/v6.4_coco_seg"
IMG_SIZE = 1024
EPOCHS = 50
BATCH = 8
DEVICE = "cuda"

if __name__ == "__main__":
    m = RFDETRSegNano()

    m.train(
        dataset_dir=DATASET_DIR,
        img_size=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        output_dir="../runs/rf_detr/train_rf-detr-seg-nano",
        run_name="v1_rf-detr-seg-nano",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/rf_detr/train_rf-detr-seg-nano/v1_rf-detr-seg-nano\n")