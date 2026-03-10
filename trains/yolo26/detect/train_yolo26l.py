from ultralytics import YOLO

MODEL_NAME = "yolo26l.pt"
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
        project="../runs/combined/train_yolo26l",
        name="v1_yolo26l",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/combined/train_yolo26l/v1_yolo26l\n")
