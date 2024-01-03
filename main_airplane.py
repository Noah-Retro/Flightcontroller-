import nrf24
from src.Libs.transmition import Tx_Thread

data = 0
tx = Tx_Thread()
print("Started thread in 1")
tx.run(data)
print("Started")

while True:
    print(data)
