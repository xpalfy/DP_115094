from ultralytics import YOLO

MODEL_NAME = "yolo12n.pt"
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
        project="../runs/combined/train_yolo12n",
        name="v1_yolo12n",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/combined/train_yolo12n/v1_yolo12n\n")
