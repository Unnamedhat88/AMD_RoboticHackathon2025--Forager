# Grocery Sorting Robot

## Overview
This project targets the AMD Open Robotics Hackathon 2025. It implements a vision-guided robotic arm for sorting grocery items.

## Architecture
- **Perception**: Grounding DINO + SAM for detection and segmentation.
- **Manipulation**: 6-DoF Arm control (SO-ARM101).
- **Logic**: Task planning and inventory management.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the main application: `python main.py`

## Structure
- `perception/`: Camera and Vision models.
- `manipulation/`: Arm control and grasping.
- `logic/`: High-level task planning.
- `ui/`: User interface.