# 🗣️ **Gesture & Voice-Controlled Flowchart Creator**  

### **🎯 Project Overview**  
This prototype enables users to create **flowcharts** using **hand gestures** and **voice commands**, powered by **Microsoft Azure** and **Mediapipe**.  

🔹 **Hand Gestures** – Use your **index and thumb** to adjust the size, position, and placement of flowchart elements.  
🔹 **Voice Commands** – Switch between shapes, modify colors, and add text effortlessly.  
🔹 **Seamless Integration** – Combines **Mediapipe** for gesture recognition and **Azure Voice-to-Text (VTT)** for speech processing.  

![image](https://github.com/user-attachments/assets/f2fffc7d-f020-4f42-a878-dcf2f24b3dc8)


---

## 🚀 **Features**  
✅ **Create Flowchart Shapes** – Place and resize using hand gestures.  
✅ **Customize Colors** – Change colors using voice commands.  
✅ **Add Text to Shapes** – Simply speak, and the text appears!  
✅ **Multi-Shape Support** – Switch between different flowchart elements dynamically.  

---

## 🛠 **Tech Stack**  
- **🖐️ Mediapipe** – Gesture Recognition  
- **🎤 Azure Speech Services (VTT)** – Voice-to-Text Processing  
- **🐍 Python** – Backend & Client-Side Scripts  

---

## ⚙️ **Installation**  

1️⃣ **Clone this repository:**  
```bash
git clone https://github.com/Stark16/Voice_Flowchart
cd Voice_Flowchart
```
  
2️⃣ **Install dependencies:**  
```bash
pip install -r requirements.txt
```

---

## ▶️ **How to Run**  

1️⃣ **Set up your Azure API Key**  
- Add your **Azure API Key** to the environment variables:  
  ```bash
  export AZURE_API_KEY="your_api_key_here"  # For Linux/macOS
  set AZURE_API_KEY="your_api_key_here"    # For Windows (CMD)
  ```

2️⃣ **Start the Gesture Recognition Server**  
```bash
python mediapipe_server.py
```

3️⃣ **Run the Voice Control Client**  
Open a **new terminal** and execute:  
```bash
python realtime_continues_speech.py
```

Now, start **creating flowcharts hands-free!** 🎉  

---
