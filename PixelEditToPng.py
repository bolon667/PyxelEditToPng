from PIL import Image
import json
import zipfile
import sys

class PyxelEditCli:
    def __init__(self, pixelFilePathArr: str):
        for path in pixelFilePathArr:
            self.saveMergedPic(path)
    def saveMergedPic(self, pixelFilePath: str):
        self.loadNewPyxelFile(pixelFilePath)
        pic = self.getMergedPic()
        picFilePath = pixelFilePath.replace(".pyxel", ".png")
        pic.save(picFilePath)
        pic.close()

    def loadNewPyxelFile(self, pixelFilePath: str):
        self.archive = zipfile.ZipFile(pixelFilePath, 'r')

        self.jsonData = json.loads(self.archive.read('docData.json'))
        self.tileWidth = int(self.jsonData["canvas"]["tileWidth"])
        self.tileHeight = int(self.jsonData["canvas"]["tileHeight"])
        self.imgHeight = self.jsonData["canvas"]["height"]
        self.imgWidth = self.jsonData["canvas"]["width"]
        self.imgWidthInTiles = int(self.imgWidth/self.tileWidth)
    def getMergedPic(self):
        resultImg = Image.new("RGBA", (self.imgWidth, self.imgHeight))
        for layerInd in reversed(self.jsonData["canvas"]["layers"]):
            #Setting of layer may be?!?
            layerData = self.jsonData["canvas"]["layers"][layerInd]
            tileRefs = layerData["tileRefs"]

            for tileRefKey, tileRefVal in tileRefs.items():
                tileRefKey = int(tileRefKey)
                x_tile_pos = tileRefKey % self.imgWidthInTiles
                y_tile_pos = int(tileRefKey/self.imgWidthInTiles)
                
                tile_image_name = "tile" + str(tileRefVal["index"]) + ".png"
                
                print(tile_image_name)
                putTile = Image.open(self.archive.open(tile_image_name))
                resultImg.paste(putTile, (x_tile_pos*self.tileWidth, y_tile_pos*self.tileHeight), putTile)
                putTile.close()
                #print(x_tile_pos, y_tile_pos)
                #Put tile on image
        return resultImg


## ->  MAIN THING  <- ##

def startCLI():
    if len(sys.argv) < 2:
        print("Put at least 1 .pyxel file on ths cli")
        input("Press ENTER to close\n")
        return
    cli = PyxelEditCli(sys.argv[1:])
    input("Done. Press ENTER to close\n")

startCLI()