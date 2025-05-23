import Scan
from src.NetUtils import NetUtils
from src.ScoreDevices import ScoreDevices

s = Scan.Scan()
current_scan = s.scan()
s.get_current_results(current_scan)

