# Advanced Automotive Radar System

## Overview

My graduation project focused on developing an advanced automotive radar system operating in the **76–81 GHz frequency range** using the **Texas Instruments AWR2944EVM** radar platform.

The project was sponsored by Brightskies and aimed to build a complete radar processing pipeline capable of detecting objects, estimating their properties, tracking multiple targets, and recognizing human gestures using artificial intelligence.

The project combined multiple engineering disciplines including radar signal processing, embedded systems, antenna engineering, machine learning, and real-time data processing.

---

## Project Objective

Modern automotive systems rely heavily on radar sensors for applications such as:

* Object detection
* Collision avoidance
* Adaptive cruise control
* Autonomous driving assistance

The goal of this project was to develop a complete radar solution starting from raw radar signals and ending with intelligent interpretation of detected objects and gestures.

---

## Radar Processing Pipeline

The system implemented a complete signal processing workflow:

1. Radar signal acquisition using Texas Instruments AWR2944EVM.

2. Processing raw radar data to extract useful information from received signals.

3. Beat frequency estimation using FFT-based techniques.

4. Windowing optimization to improve frequency estimation accuracy and reduce spectral leakage.

5. Target detection using adaptive CFAR algorithms.

6. High-resolution angle estimation using MUSIC algorithm.

7. Multi-target clustering and tracking.

---

## My Technical Contribution

My main responsibility in the project was the communication and signal processing part, especially:

* Frequency estimation
* Windowing analysis and optimization
* Radar signal processing evaluation

I analyzed multiple windowing techniques and evaluated their impact on frequency estimation accuracy across different sweep times.

This work improved my understanding of:

* FMCW radar systems
* Beat signals
* FFT processing
* Spectral analysis
* Digital Signal Processing (DSP)

---

## Multi-Target Tracking

To achieve reliable object tracking, the system combined:

### DBSCAN Clustering

DBSCAN was used to group detected radar points into meaningful objects.

### Extended Kalman Filter (EKF)

An Extended Kalman Filter was implemented to estimate object states and track target movement over time.

This approach enabled stable multi-target tracking in real-time conditions.

---

## AI-Based Gesture Recognition

The project also included an AI-based gesture recognition system.

Deep learning models using:

* CNN (Convolutional Neural Network)
* GRU (Gated Recurrent Unit)

were developed to classify radar-based gestures.

The model achieved more than **93% classification accuracy**.

This part demonstrated how radar signals can be combined with machine learning techniques to create intelligent sensing systems.

---

## Hardware and Software Technologies

The project used:

### Hardware

* Texas Instruments AWR2944EVM
* 76–81 GHz FMCW Radar Sensor

### Software and Tools

* TI mmWave SDK
* MATLAB
* Python
* Machine Learning Frameworks
* Embedded Processing Tools

The system supported real-time visualization and Ethernet-based radar data acquisition.

---

## Skills and Knowledge Gained

This project significantly strengthened my knowledge in:

* Digital Signal Processing (DSP)
* FMCW Radar Systems
* Embedded Systems
* Machine Learning
* Artificial Intelligence
* Real-Time Systems
* Signal Analysis
* Wireless Communication Systems

It also improved my ability to work on complex multidisciplinary engineering projects that combine hardware, software, and AI.

---

## Project Impact

The project represented a complete engineering journey from understanding raw sensor signals to building an intelligent radar-based application.

It helped me develop strong problem-solving skills and reinforced my interest in combining software engineering, artificial intelligence, and advanced engineering systems.
