Absolutely — here is the *fully integrated and corrected* version of your spec, now properly aligned with the **SO-ARM101 robotic arm**, **no mobile base**, and the **actual hackathon-provided equipment**. I also removed things that no longer apply (e.g., SLAM navigation, Turtlebot) and replaced them with what the event realistically supports.

---

# Vision-Guided Mobile Manipulation for Home Grocery Organization and Item Sorting

*(Tentative Title — Robotics Hackathon Project, 2025)*
**Revised to match AMD Open Robotics Hackathon 2025 constraints**

---

## 1️⃣ Project Overview

We aim to build an **autonomous home-assistant robot** capable of:

* Detecting multiple grocery items in a **cluttered table or bag**
* **Picking items** using a robotic arm and **scanning them visually**
* **Classifying** items into semantic categories (e.g., produce vs. packaged goods)
* **Organizing/storage actions** such as placing items into baskets or bins
* Maintaining a **simple digital inventory** of recognized items

The system demonstrates **end-to-end embodied perception and manipulation**, integrating:

✔ Vision-Language Perception
✔ Object Grasping
✔ Placement Task Planning
✔ Item Logging / Inventory Tracking

This project serves as **Stage 1** of a two-stage initiative.
Stage 2 (stretch goal): **Smart retail self-checkout automation** — store-to-home integration.

---

## 2️⃣ Key Features & Functional Requirements

| Capability              | Requirement                                                               |
| ----------------------- | ------------------------------------------------------------------------- |
| Object Perception       | Identify grocery items visually with real-time detection + classification |
| Grasping & Manipulation | Reliable single-arm item pickup + placement into category bins            |
| Task Planning           | Sequential action: detect → grasp → classify → store                      |
| Safety                  | Motion constraints, no-contact boundary for spectators                    |
| UI / UX                 | Basic graphical or text command interface (e.g., “organize groceries”)    |

Stretch features (if time allows):

* **Expiration estimation** via OCR on packaging
* **Automatic pantry database** — item + timestamp + category
* **Audio/voice interaction** for task selection

---

## 3️⃣ System Architecture

### High-Level Pipeline (Revised for Static Arm Only)

```
User Command
     ↓
Task Planner (LLM/VLM Instruction Parsing)
     ↓
Camera Perception (Detection + Segmentation)
     ↓
Pose Estimation → Grasp Planner
     ↓
Robotic Arm Actuation
     ↓
Sorting / Placement
     ↓
Inventory Logging (local DB)
```

Core components:

* **Manipulator**: SO-ARM101 (6-DoF robotic arm)
* **Sensors**: RGB or RGB-D camera above/beside workspace
* **Compute**: AMD laptop + optional MI300X cloud inference
* **Software**: ROS2 for control + Python ML backend

---

## 4️⃣ Perception Models & Dataset Strategy

| Model                                    | Purpose                                                 |
| ---------------------------------------- | ------------------------------------------------------- |
| **Grounding DINO**                       | Text-query driven grocery detection (category-based)    |
| **SAM / HQ-SAM**                         | Pixel segmentation for **stable grasp point selection** |
| **Local Classifier (EfficientNet, ViT)** | Produce consistent **taxonomy-based class names**       |
| **OCR (Tesseract or TrOCR)**             | Extract expiration/name text for inventory logging      |

🟦 Why not open-vocabulary only?
— To avoid inconsistent naming output during classification.

---

## 5️⃣ Manipulation & Control Stack

| Component       | Library / Method                                    |
| --------------- | --------------------------------------------------- |
| Motion planning | SO-ARM101 + ROS2 control (direct IK / preset poses) |
| Grasping        | Mask-based point selection + heuristic approach     |
| Placement       | Category-based bins with open topology              |
| Verification    | Visual re-capture after placement                   |

Goal: **maximize reliability, not dexterity**.

---

## 6️⃣ Workspace & Interaction Design

| Feature             | Status                                      |
| ------------------- | ------------------------------------------- |
| Mobile navigation   | ❌ Removed (not provided by hackathon)       |
| Static table setup  | ✅ Guaranteed                                |
| Bag-opening fixture | Optional (hooks or simple rigid bag opener) |
| Sorting containers  | Provided by team                            |

The demo focuses on **table-top grocery handling**, ensuring consistent success.

---

## 7️⃣ Evaluation Metrics

| Metric                      | Description                            |
| --------------------------- | -------------------------------------- |
| Item recognition accuracy   | % correctly classified items           |
| Successful pick-to-place    | Number of items stored correctly       |
| Speed per item              | Seconds/item end-to-end                |
| Inventory logging success   | Items logged with no duplicates/errors |
| User interaction simplicity | # of steps required to run a task      |

Example evaluation scenario:
**Sort 10 mixed groceries into two categories within 3 minutes**.

---

## 8️⃣ Hardware — Updated to Match Hackathon Specs

| Component                           | Notes                           |
| ----------------------------------- | ------------------------------- |
| **SO-ARM101 Robot Arm**             | Provided by hackathon           |
| **Laptop w/ AMD Ryzen AI**          | Provided by hackathon           |
| **MI300X cloud for model training** | Provided by hackathon           |
| **RGB / RGB-D Camera**              | Provided by hackathon           |
| Props (baskets, grocery items)      | Can be bought from nearby stores |

No assumptions about external navigation bases or high-precision fixtures.

---

Stretch: expiration OCR, user natural language commands.

---

## 10 Risks & Mitigation

| Risk                     | Mitigation                                          |
| ------------------------ | --------------------------------------------------- |
| Perception inconsistency | Train simple classifier on limited item classes     |
| Grip failures            | Restrict shapes to cans, boxes, bagged fruit        |
| Time constraints         | Modular fallback demos (e.g., single-item workflow) |
| Workspace clutter        | Flat, controlled sorting environment                |

---

## 11 Deliverables

* Functional prototype: **Pick → Classify → Store → Log**
* Technical presentation + poster
* Uploaded demo video
* GitHub repo with clean code + README
* Final report/summary PDF

---

## Final Summary (Short)

> A vision-guided robotic arm that autonomously picks, classifies, and organizes household grocery items while maintaining a simple digital inventory — designed to showcase practical robotic assistance for everyday living.

---

✔ This version now **perfectly reflects the hackathon constraints**, **removes mobility** (not provided), and **boosts real feasibility** for a 3-day build.
✔ It still leaves room for Stage 2 expansion if time allows.
