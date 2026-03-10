from ultralytics import YOLO

MODEL_NAME = "yolo26n.pt"
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
        project="../runs/combined/train_yolo26n",
        name="v1_yolo26n",
        exist_ok=True
    )

    print("\nTraining completed. Model saved in ../runs/combined/train_yolo26n/v1_yolo26n\n")
