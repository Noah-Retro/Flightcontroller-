import nrf24
from src.Libs.transmition import Tx_Thread

data = 0
tx = Tx_Thread()
tx.run(data)


while True:
    print(data)
