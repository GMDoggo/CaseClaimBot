# SOAR Automation

## Objective
As a SOC analyst working within Swimlane, a SOAR platform, the goal of this project was to streamline the alert handling process by automating the case claiming and assignment procedure. The objective was to build a rudimentary system using **PyAutoGUI** and **image detection** to automatically claim incoming alerts and assign them to myself as they appeared in the queue. The overall goal was to reduce the response time to alerts, improve the efficiency of the SOC workflow, and minimize manual intervention, allowing analysts to focus on more complex tasks.

### Skills Learned
- Proficiency in **Python scripting** for automating repetitive tasks and improving workflow efficiency.
- Practical experience in **task automation** for operational efficiency in cybersecurity environments.
- Ability to create **automated solutions** that reduce manual intervention and improve response time to security alerts.


### Tools Used

- **Swimlane** SOAR platform for managing and automating security workflows in the SOC.
- **Python** as the primary programming language for scripting automation tasks.
- **PyAutoGUI** for automating GUI interactions and image detection to claim alerts.
### Notice:
While this project may seem incredibly niche (let’s face it, automating alert claims using image detection isn’t something you’ll find in every cybersecurity job description), it was surprisingly effective for streamlining the workflow in a busy SOC.

That said, if you want to dive in and replicate this setup, here’s the installation process.

### CaseClaimBot Installation
1. **Install Python 3.10 (not compatible with other major versions)**
2. **Clone/download this repository**
3. **Open the project folder in your IDE of choice (Visual Studio Code recommended)**
4. **Open the repository folder in a terminal window**
5. **Create a virtual environment:**
   ```bash
   py -3.10 -m venv env
6. **Open the repository folder in a terminal window**
   i. **Create a virtual environment:**
      ```bash
      py -3.10 -m venv env
      ```
   ii. **Activate the newly created virtual environment:**
      ```bash
      .\env\Scripts\activate
      ```
   iii. **Install the dependencies:**
      ```bash
      pip install -r requirements.txt
      ```
7. **Run the script (may need to restart IDE for it to recognize installed dependencies):**
   ```bash
   ./src/*caseclaimer.py*

