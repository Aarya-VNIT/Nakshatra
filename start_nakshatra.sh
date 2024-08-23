# /home/vnit/Documents/Nakshatra/start_nakshatra.sh
#!/bin/bash
{
    echo "Starting Nakshatra App..."
    date

    # Activate the virtual environment
    source /home/vnit/Documents/Nakshatra/.venv/bin/activate
    echo "Virtual environment activated."

    # Run the Python script
    /usr/bin/lxterminal -e /bin/bash -c "source /home/vnit/Documents/Nakshatra/.venv/bin/activate; python3 /home/vnit/Documents/Nakshatra/main.py; echo 'Press Enter to close...'; read"
    echo "Python script executed."

    echo "Nakshatra App finished."
} >> /home/vnit/Documents/Nakshatra/nakshatra.log 2>&1
