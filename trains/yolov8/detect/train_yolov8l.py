from ultralytics import YOLO

MODEL_NAME = "yolov8l.pt"
DATA_YAML = "data.yaml"
IMG_SIZE = 1024
EPOCHS = 500
PATIENCE = 100
BATCH = 4
DEVICE = "cuda"

if __name__ == "__main__":
    m = YOLO(MODEL_NAME)

    m.train(
        data=DATA_YAML,
        imgsz=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH,
        device=DEVICE,
        patience=PATIENCE,
        project="../runs/combined/train_yolov8l",
        name="v1_yolov8l",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/combined/train_yolov8l/v1_yolov8l\n")
