from ultralytics import YOLO

MODEL_NAME = "yolo11n-seg.pt"
DATA_YAML = "data.yaml"
IMG_SIZE = 1024
EPOCHS = 50
BATCH = 8
DEVICE = "cuda"

if __name__ == "__main__":
    m = YOLO(MODEL_NAME)

    m.train(
        data=DATA_YAML,
        imgsz=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        project="../runs/combined/train_yolo11n-seg",
        name="v1_yolo11n-seg",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/combined/train_yolo11n-seg/v1_yolo11n-seg\n")
