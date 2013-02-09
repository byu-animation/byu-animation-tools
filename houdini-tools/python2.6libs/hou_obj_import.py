# Used to import multiple .obj files into houdini

objsString = hou.ui.selectFile(multiple_select=True) #select files
objsList = [o.strip() for o in objsString.split(';')] #splits paths into list (objsList[0] returns path of file)
count = len(objsList) #number of selected files
subnet = hou.node("/obj").createNode("subnet") #creates subnet node
shopnet = hou.node(subnet.path()).createNode("shopnet") #creates shopnet node
n = 0

for x in range (0,count): #create loop
        #create geo
        geo =  hou.node(subnet.path()).createNode("geo") #creates the geometry node in subnet
        node = hou.node(geo.path() + "/file1") #accesses file node
        node.setParms({'file': objsList[n]}) #assigns file path to file node
        pathList = objsList[n].split('/') #splits path into a list
        nameList = pathList[-1].split('.') #splits name.obj into list
        isName = nameList[0] #selects name
        geo.setName(isName) #changes geo name
        #assigns ubershader
        uber = hou.node(shopnet.path()).createNode("chasm_ubershader") #creates ubershader in shopnet
        geo.setParms({'shop_materialpath': "../shopnet1/chasm_ubershader1"}) #assigns shader to geo
        uber.setName(isName + "_ubershader") #changes ubershader name
        
        n = n + 1
