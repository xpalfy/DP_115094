from ultralytics import YOLO

MODEL_NAME = "yolo12m.pt"
DATA_YAML = "data.yaml"
IMG_SIZE = 1024
EPOCHS = 250
PATIENCE = 50
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
        project="../runs/combined/train_yolo12m",
        name="v1_yolo12m",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/combined/train_yolo12m/v1_yolo12m\n")
