from ultralytics import YOLO

# Load your trained model
model = YOLO('model/best.pt')  # path to best model


def scanImg(imguri):
    results = model(imguri, conf=0.1)
    output = []
    for r in results:
        boxes = r.boxes.xyxy.tolist()        # bounding boxes as list of [x1, y1, x2, y2]
        confidences = r.boxes.conf.tolist()  # confidence scores
        class_ids = r.boxes.cls.tolist()     # class indices
        output.append({
            "boxes": boxes,
            "confidences": confidences,
            "class_ids": class_ids,
        })
    return output

def FetchModel():
    return model


def main():
    ... #Testing Locally

if __name__ == "__main__":
    main()
