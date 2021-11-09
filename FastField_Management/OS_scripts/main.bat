REM Description: runs the fastfield manager software to update Databses & Organize Daily's on Run Time

cd "C:\Users\james\OneDrive\Documents\Coding Projects\Python Projects\Takeoff AI\FastField_Management\OS_scripts"
CALL activate walker

C:/Users/james/anaconda3/envs/walker/python.exe "c:/Users/james/OneDrive/Documents/Coding Projects/Python Projects/Takeoff AI/FastField_Management/main.py"

CALL conda deactivate

echo "FastDaily Organizer Complete"
cmd /k