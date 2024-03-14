from Steganography import HideInImage, ExtractFromImage

seed, key, iv = HideInImage.HideInImage().hideInImage("C:/Users/MrIzzat/PycharmProjects/Usable Security Project/TestFiles/cat.jpg",
                                      "C:/Users/MrIzzat/PycharmProjects/Usable Security Project/TestFiles/largetext.txt",
                                      "./temp.png")


ExtractFromImage.ExtractFromImage().extractFromImage("./temp.png","./",seed,key,iv)