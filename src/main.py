import Scan
from src.NetUtils import NetUtils
from src.ScoreDevices import ScoreDevices
from src.LiveMonitor import LiveMonitor

s = Scan.Scan()
lm = LiveMonitor(s)
lm.start()

