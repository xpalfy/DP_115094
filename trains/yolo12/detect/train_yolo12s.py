from ultralytics import YOLO

MODEL_NAME = "yolo12s.pt"
DATA_YAML = "data.yaml"
IMG_SIZE = 1024
EPOCHS = 100
PATIENCE = 25
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
        patience=PATIENCE,
        project="../runs/combined/train_yolo12s",
        name="v1_yolo12s",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/combined/train_yolo12s/v1_yolo12s\n")
