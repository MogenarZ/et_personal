import os, re

def convert_provs(prov, nat, year, year_end):
    #find first line before start year
    for line in prov.split("\n"):
        maybe_date = re.findall("[\d]{3}\.[\d]{1,2}\.[\d]{1,2}", line)
        if len(maybe_date) > 0:
            prev_date = maybe_date[0]
            if int(maybe_date[0].split(".")[0]) > int(year):
                break
                
    prov = prov.replace(prev_date,
                        "\n"+year+".1.1 = { add_core = "+nat+" controller = "+nat+" owner = "+nat+" }\n"+year_end+".1.1 = { owner = ROM controller = ROM remove_core = "+nat+" }\n"+prev_date)
    return prov
    

GLL_provs = ("173", "175", "176", "197", "2598", "198", "199", "203", "4514", "200")
PLM_provs = ("4441", "2004", "2366", "324", "4429", "2364", "4436", "326", "365")
ROE_not_provs = ("462", "1856")
ROE_to_BYZ = "610.10.5 = { controller = BYZ owner = BYZ add_core = BYZ remove_core = ROE } # Byzantium Formed"
VAN_to_BYZ = """533.10.15 = { controller = BYZ add_core = BYZ }
534.3.1 = { owner = BYZ remove_core = VAN }"""
VAN_to_BYZ_new = """533.10.15 = { controller = ROE add_core = ROE }
534.3.1 = { owner = ROE remove_core = VAN }"""

for fil in [fil for fil in os.listdir(os.getcwd()) if ".txt" in fil]:
    #print(fil)
    changed = False
    with open(fil, "r") as prov_file:
        try:
            prov_data = prov_file.read()
        except:
            pass
        else:
            if re.findall("[\d]+", fil)[0] in GLL_provs and "owner = GLL" not in prov_data:
                changed = True
                prov_data = convert_provs(prov_data, "GLL", "268", "274")
                
            if re.findall("[\d]+", fil)[0] in PLM_provs and "owner = PLM" not in prov_data:
                changed = True
                prov_data = convert_provs(prov_data, "PLM", "270", "273")
            
            if "260.1.1 = { add_core = GLL revolt = { type = nationalist_rebels size = 1 } controller = REB " in prov_data:
                changed = True
                prov_data = prov_data.replace("260.1.1 = { add_core = GLL revolt = { type = nationalist_rebels size = 1 } controller = REB ",
                                              "260.1.1 = { add_core = GLL owner = GLL controller = GLL ")
                prov_data = prov_data.replace("268.1.1 = { controller = ROM remove_core = GLL revolt = {} ",
                                              "274.1.1 = { owner = ROM controller = ROM remove_core = GLL ")

            if "260.1.1 = { add_core = PLM revolt = { type = nationalist_rebels size = 2 } controller = REB }" in prov_data:
                changed = True
                prov_data = prov_data.replace("260.1.1 = { add_core = PLM revolt = { type = nationalist_rebels size = 2 } controller = REB ",
                                              "267.1.1 = { add_core = PLM owner = PLM controller = PLM ")
                prov_data = prov_data.replace("272.1.1 = { controller = ROM remove_core = PLM revolt = {} ",
                                              "273.1.1 = { controller = ROM remove_core = PLM owner = ROM ")

            if "260.1.1 = { add_core = PLM revolt = { type = nationalist_rebels size = 1 } controller = REB }" in prov_data:
                changed = True
                prov_data = prov_data.replace("260.1.1 = { add_core = PLM revolt = { type = nationalist_rebels size = 1 } controller = REB ",
                                              "267.1.1 = { add_core = PLM owner = PLM controller = PLM ")
                prov_data = prov_data.replace("272.1.1 = { controller = ROM remove_core = PLM revolt = {} ",
                                              "273.1.1 = { controller = ROM remove_core = PLM owner = ROM ")

            if "269.1.1 = { add_core = PLM revolt = { type = nationalist_rebels size = 1 } controller = REB " in prov_data:
                changed = True
                prov_data = prov_data.replace("269.1.1 = { add_core = PLM revolt = { type = nationalist_rebels size = 1 } controller = REB ",
                                              "269.1.1 = { add_core = PLM owner = PLM controller = PLM ")

            if "culture = briton" in prov_data and "owner = ROM" in prov_data and "owner = GLL" not in prov_data and re.findall("[\d]+", fil)[0] not in ("4486", "4487"):
                changed = True
                prov_data = convert_provs(prov_data, "GLL", "268", "274")

            if "culture = old_egyptian" in prov_data and "owner = ROM" in prov_data and "owner = PLM" not in prov_data and re.findall("[\d]+", fil)[0] not in ("2517", "2518", "357"):
                changed = True
                prov_data = convert_provs(prov_data, "PLM", "270", "273")

            if "395.1.17 = { controller = BYZ owner = BYZ add_core = BYZ remove_core = ROM } # Final division of the empire" in prov_data:
                changed = True
                ROE_line = "395.1.17 = { controller = ROE owner = ROE add_core = ROE remove_core = ROM } # Final division of the empire"
                prov_data = prov_data.replace("395.1.17 = { controller = BYZ owner = BYZ add_core = BYZ remove_core = ROM } # Final division of the empire",
                                              ROE_line)
                if re.findall("[\d]+", fil)[0] not in ROE_not_provs:
                    prov_data = prov_data.replace(ROE_line, ROE_line + "\n610.10.5 = { controller = BYZ owner = BYZ add_core = BYZ remove_core = ROE } # Byzantium Formed")

            if VAN_to_BYZ in prov_data:
                changed = True
                prov_data = prov_data.replace(VAN_to_BYZ, VAN_to_BYZ_new)

            if "543.1.1 = { owner = BYZ controller = BYZ add_core = BYZ remove_core = VAN }" in prov_data:
                changed = True
                prov_data = prov_data.replace("543.1.1 = { owner = BYZ controller = BYZ add_core = BYZ remove_core = VAN }",
                                              "543.1.1 = { owner = ROE controller = ROE add_core = ROE remove_core = VAN }\n"+ROE_to_BYZ)
            #fix
            if "534.3.1 = { owner = ROE remove_core = VAN }" in prov_data and ROE_to_BYZ not in prov_data:
                changed = True
                prov_data = prov_data.replace("534.3.1 = { owner = ROE remove_core = VAN }",
                                              "534.3.1 = { owner = ROE remove_core = VAN }\n"+ROE_to_BYZ)
            if "510.1.1 = { owner = BYZ controller = BYZ remove_core = GOS }" in prov_data:
                changed = True
                prov_data = prov_data.replace("510.1.1 = { owner = BYZ controller = BYZ remove_core = GOS }",
                                              "510.1.1 = { owner = ROE controller = ROE remove_core = GOS }")
                if ROE_to_BYZ not in prov_data:
                    prov_data = prov_data.replace("510.1.1 = { owner = ROE controller = ROE remove_core = GOS }",
                                                  "510.1.1 = { owner = ROE controller = ROE remove_core = GOS }\n"+ROE_to_BYZ)
            if "540.1.1 = { owner = BYZ controller = BYZ add_core = BYZ remove_core = GOS }" in prov_data:
                changed = True
                prov_data = prov_data.replace("540.1.1 = { owner = BYZ controller = BYZ add_core = BYZ remove_core = GOS }",
                                              "540.1.1 = { owner = ROE controller = ROE add_core = ROE remove_core = GOS }\n"+ROE_to_BYZ)

            if "591.1.1 = { owner = BYZ controller = BYZ add_core = BYZ remove_core = SAS }" in prov_data:
                changed = True
                prov_data = prov_data.replace("591.1.1 = { owner = BYZ controller = BYZ add_core = BYZ remove_core = SAS }",
                                              "591.1.1 = { owner = ROE controller = ROE add_core = ROE remove_core = SAS }\n"+ROE_to_BYZ)

            #doing manually because Belgrade hates life
            if "592.1.1 = { controller = BYZ }" in prov_data:
                changed = True
                prov_data = prov_data.replace("592.1.1 = { controller = BYZ }", "592.1.1 = { controller = ROE }")

            if "552.1.1 = { owner = BYZ controller = BYZ add_core = BYZ }" in prov_data:
                changed = True
                prov_data = prov_data.replace("552.1.1 = { owner = BYZ controller = BYZ add_core = BYZ }",
                                              "552.1.1 = { owner = ROE controller = ROE add_core = ROE }")
                prov_data = prov_data.replace("572.1.1 = { owner = GVI controller = GVI remove_core = BYZ }",
                                              "572.1.1 = { owner = GVI controller = GVI remove_core = ROE }")

            #time change for Rome split
            if "395.1.17 = { controller = ROW owner = ROW add_core = ROW remove_core = ROM } # Final division of the empire" in prov_data:
                changed = True
                prov_data = prov_data.replace("395.1.17 = { controller = ROW owner = ROW add_core = ROW remove_core = ROM } # Final division of the empire",
                                              "337.5.23 = { controller = ROW owner = ROW add_core = ROW remove_core = ROM } # Final division of the empire")

            if "395.1.17 = { controller = ROE owner = ROE add_core = ROE remove_core = ROM } # Final division of the empire" in prov_data:
                changed = True
                prov_data = prov_data.replace("395.1.17 = { controller = ROE owner = ROE add_core = ROE remove_core = ROM } # Final division of the empire",
                                              "337.5.23 = { controller = ROE owner = ROE add_core = ROE remove_core = ROM } # Final division of the empire")

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
