import sys
sys.path.append('..')

from Utils import baseSession

bs = baseSession()
bs.set_proxies(7890)
bs.disable_log()
bs.enable_log()
bs.test_connection()
print(bs.log)

