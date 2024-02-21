import GenerateQR as GQR
import ReadQR as RQR


GQR.generateQR("./")

print(RQR.decodeQR("./userQR.png"))
