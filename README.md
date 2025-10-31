A simple TCP Client-Server program emulating the relationship between a remote control and a TV.

Written as part of the [IDATA2304](https://www.ntnu.edu/studies/courses/IDATA2304) Computer communication and network programming course at NTNU Ålesund.

---

#### How to run

1. Load up your favorite Python-able IDE.
2. Clone the repository to your computer, or download it as a ZIP and extract it to your go-to 
   folder for super exciting Python projects such as this one.
3. Run server.py
4. Run remote_control.py
5. The remote control should connect to the server, and you should be prompted to enter commands.
6. Optional: Run several instances of the remote control (`python .\smarttvapp\client\remote_control.py` or an IDE that supports running in concurrent terminals).

---

#### Commands
- get : Returns the current state of the TV
- set power <on/off> : Turns the TV on or off
- set channel <up/down> : Changes the channel up or down by 1
- exit/quit : Closes the remote control application

Example usage:

- `set power on` : turn the TV on.
- `set channel up` : move the channel up (default channel : 1) by 1.
- `get` : returns the current state, channel 2 on a TV that is on.
