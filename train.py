# train.py
import argparse
import yaml
from ultralytics import YOLO

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.yaml')
    args = parser.parse_args()

    config = load_config(args.config)

    model = YOLO('yolov8n.pt')  # Pretrained small model
    model.train(
        data='coco128.yaml',        # Example dataset
        epochs=config['epochs'],
        imgsz=config['imgsz'],
        batch=config['batch_size'],
        lr0=config['learning_rate']
    )

if __name__ == "__main__":
    main()
