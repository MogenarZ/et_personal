import os, re

for fil in [fil for fil in os.listdir(os.getcwd()) if ".txt" in fil]:
    #print(fil)
    changed = False
    with open(fil, "r") as prov_file:
        try:
            prov_data = prov_file.read()
        except:
            pass
        else:
            #East-West split of Christianity
            if "867.1.1 = { religion = catholic }" in prov_data:
                changed = True
                prov_data = prov_data.replace("867.1.1 = { religion = catholic }", "1054.7.20 = { religion = catholic }")

            if "867.1.1 = { religion = orthodox }" in prov_data:
                changed = True
                prov_data = prov_data.replace("867.1.1 = { religion = orthodox }", "1054.7.20 = { religion = orthodox }")

            
                                              
                
                

    


                            

    if changed:
        with open(fil, "w") as out_file:
            out_file.write(prov_data)
