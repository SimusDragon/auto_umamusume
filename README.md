# Auto Umamusume - Automated Training for Umamusume Pretty Derby (PC)

This is a macro designed to automate **Careers** in the game *Umamusume Pretty Derby*
It follows a dynamic decision-making system to optimize training actions turn by turn

## Requirements
- **Operating system:** Windows
- Python
- Run the following to install Python packages:	```pip install -r requirements.txt```
- **Tesseract OCR:** Must be installed at: "C:\Program Files\Tesseract-OCR"

## Conditions
- The game must be set to **English**
- The game window must be **completely visible**
- Works in **fullscreen** or **windowed** mode
- In windowed mode, only the **playable area** needs to be visible
- High screen resolution is required (the window should match your screen's height)
- The mouse must **remain still** during macro execution

## Warnings & Limitations
- The macro does **not** have a pause/resume feature — avoid interacting with the mouse while it's running
- Includes deliberate delays between actions to reduce errors and tolerate connection issues (e.g. race loading screens)
- Some events may be unrecognized due to unusual symbols or long names. If the macro gets stuck, choose an option manually — it will continue
- Event data is stored manually. If the game receives an update with new content, the macro will not recognize the new events unless updated

## How to use it
- Start the macro using interface.py

## Get Started
**Skip the intro and make sure "SKIP x2" is enabled**  
Start the macro once you've reached the playable phase
You can activate it using the GUI button or the `F8` key

## How It Works

### Training
- **Before the Training N° 15**: Prioritizes *support affinity*
- **Training priority:**
  - **If Energy > ~75%**: Speed > Stamina > Power > Guts > Wit
  - **If Energy < ~75%**: Speed > Wit > Stamina > Power > Guts
  - Only stats **below the soft cap** (1050) are considered
- *Friendship (rainbow) training is not detected*

### Resting
- Rests when energy drops below **~40%**

### Recreation
- If mood is **below Great** and energy is **below ~80%**

### Races
- Only when **required to reach the goal**
- Automatically enters **mandatory progress races**

### Skills
- Learns skills in **descending list order**
- Only triggers if:
  - Training N° 15 >
  - Skill points ≥ 300

### Infirmary
- Will **always choose** if the option is available

### Events

**Event choice priority:**
1. Energy (if not full)
2. Mood (if not maxed)
3. Skill / Hint
4. Skill points
5. Speed
6. Wit
7. Stamina / Power
8. Random stat
9. Guts
10. Any stat above the soft cap
11. Energy (if already full)
12. Mood (if already maxed)

**Special cases:**
- Claw machine events should catch the first uma
- Inspiration events may not always trigger correctly

## No Guaranteed Success
This macro attempts to follow smart strategies, but it does **not guarantee victories or optimal results**
You may still need to adjust your team, supports, and route manually for best performance

## Contribute
Feel free to open issues, suggest improvements, or submit pull requests to enhance the macro’s logic, event handling, or performance. Or fork the project and build your own version
