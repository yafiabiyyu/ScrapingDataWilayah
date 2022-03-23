import requests, json, os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DataWilayahScrap:
    def __init__(self):
        self.provinsi = []
        self.kabupaten = []
        self.kecamatan = []
        self.desa = []

    def getProv(self):
        json_file = open("provinsi.json", "w")
        prov_url = requests.get(
            "https://sig.bps.go.id/rest-bridging/getwilayah?level=provinsi"
        ).json()
        for i in range(len(prov_url)):
            print(
                "Ambil data provinsi : {}".format(
                    prov_url[i]["nama_bps"]
                )
            )
            self.provinsi.append(prov_url[i])
            # sleep(5)
        json_string = json.dumps(self.provinsi, indent=4)
        json_file.write(json_string)
        json_file.close()

    def getKab(self):
        for i in range(len(self.provinsi)):
            print(
                "Ambil data kabupaten dari provinsi : {}".format(
                    self.provinsi[i]["nama_bps"]
                )
            )
            kab_file = open(
                "kabupaten/{}.json".format(
                    self.provinsi[i]["kode_bps"]
                ),
                "w",
            )
            kab_url = requests.get(
                "https://sig.bps.go.id/rest-bridging/getwilayah?level=kabupaten&parent={}".format(
                    int(self.provinsi[i]["kode_bps"])
                )
            ).json()
            self.kabupaten.append([])
            for x in range(len(kab_url)):
                self.kabupaten[i].append(kab_url[x])
            json_string = json.dumps(self.kabupaten[i], indent=4)
            kab_file.write(json_string)
            kab_file.close()
            # sleep(5)

    def getKec(self):
        # Get Kode Kabupaten
        kab_kode_list = []
        for i in range(len(self.kabupaten)):
            for j in range(len(self.kabupaten[i])):
                kab_kode_list.append(self.kabupaten[i][j]["kode_bps"])

        # Get Kecamatan Data
        for i in range(len(kab_kode_list)):
            print(
                "Ambil data kecamatan dari kabupaten : {}".format(
                    kab_kode_list[i]
                )
            )
            kec_file = open(
                "kecamatan/{}.json".format(kab_kode_list[i]), "w"
            )
            kec_url = requests.get(
                "https://sig.bps.go.id/rest-bridging/getwilayah?level=kecamatan&parent={}".format(
                    int(kab_kode_list[i])
                )
            ).json()
            self.kecamatan.append([])
            for x in range(len(kec_url)):
                self.kecamatan[i].append(kec_url[x])
            json_string = json.dumps(self.kecamatan[i], indent=4)
            kec_file.write(json_string)
            kec_file.close()
            # sleep(5)

    def main(self):
        self.getProv()
        self.getKab()
        self.getKec()
        # self.getDes()


class DataWilayah:
    def __init__(self):
        self.provinsi = {}
        self.kabupaten = {}
        self.kecamatan = {}
        self.desa = {}

    def getProv(self):
        self.provinsi["kode_bps"] = []
        self.provinsi["nama_bps"] = []
        self.provinsi["kode_dagri"] = []
        self.provinsi["nama_dagri"] = []
        reqProv = requests.get(
            "https://sig.bps.go.id/rest-bridging/getwilayah?level=provinsi"
        ).json()
        for i in range(len(reqProv)):
            print(
                "Ambil Data Provinsi {}".format(reqProv[i]["nama_bps"])
            )
            self.provinsi["kode_bps"].append(
                str(reqProv[i]["kode_bps"])
            )
            self.provinsi["nama_bps"].append(reqProv[i]["nama_bps"])
            self.provinsi["kode_dagri"].append(reqProv[i]["kode_dagri"])
            self.provinsi["nama_dagri"].append(reqProv[i]["nama_dagri"])

    def getKab(self):
        self.kabupaten["kode_provinsi"] = []
        self.kabupaten["kode_bps"] = []
        self.kabupaten["nama_bps"] = []
        self.kabupaten["kode_dagri"] = []
        self.kabupaten["nama_dagri"] = []
        for i in range(len(self.provinsi["kode_bps"])):
            reqKab = requests.get(
                "https://sig.bps.go.id/rest-bridging/getwilayah?level=kabupaten&parent={}".format(
                    int(self.provinsi["kode_bps"][i])
                )
            ).json()
            for j in range(len(reqKab)):
                print(
                    "Ambil Data Kabupaten {}".format(
                        reqKab[j]["nama_bps"]
                    )
                )
                self.kabupaten["kode_provinsi"].append(
                    str(self.provinsi["kode_bps"][i])
                )
                self.kabupaten["kode_bps"].append(
                    str(reqKab[j]["kode_bps"])
                )
                self.kabupaten["nama_bps"].append(reqKab[j]["nama_bps"])
                self.kabupaten["kode_dagri"].append(
                    reqKab[j]["kode_dagri"]
                )
                self.kabupaten["nama_dagri"].append(
                    reqKab[j]["nama_dagri"]
                )

    def getKec(self):
        self.kecamatan["kode_kab/kota"] = []
        self.kecamatan["kode_bps"] = []
        self.kecamatan["nama_bps"] = []
        self.kecamatan["kode_dagri"] = []
        self.kecamatan["nama_dagri"] = []
        for i in range(len(self.kabupaten["kode_bps"])):
            reqKec = requests.get(
                "https://sig.bps.go.id/rest-bridging/getwilayah?level=kecamatan&parent={}".format(
                    int(self.kabupaten["kode_bps"][i])
                )
            ).json()
            for j in range(len(reqKec)):
                print(
                    "Ambil Data Kecamatan {}".format(
                        reqKec[j]["nama_bps"]
                    )
                )
                self.kecamatan["kode_kab/kota"].append(
                    str(self.kabupaten["kode_bps"][i])
                )
                self.kecamatan["kode_bps"].append(
                    str(reqKec[j]["kode_bps"])
                )
                self.kecamatan["nama_bps"].append(reqKec[j]["nama_bps"])
                self.kecamatan["kode_dagri"].append(
                    reqKec[j]["kode_dagri"]
                )
                self.kecamatan["nama_dagri"].append(
                    reqKec[j]["nama_dagri"]
                )

    def getDes(self):
        self.desa["kode_kec"] = []
        self.desa["kode_bps"] = []
        self.desa["nama_bps"] = []
        self.desa["kode_dagri"] = []
        self.desa["nama_dagri"] = []
        for i in range(len(self.kecamatan["kode_bps"])):
            reqDes = requests.get(
                "https://sig.bps.go.id/rest-bridging/getwilayah?level=desa&parent={}".format(
                    int(self.kecamatan["kode_bps"][i])
                )
            ).json()
            for j in range(len(reqDes)):
                print(
                    "Ambil Data Desa {}".format(reqDes[j]["nama_bps"])
                )
                self.desa["kode_kec"].append(
                    str(self.kecamatan["kode_bps"][i])
                )
                self.desa["kode_bps"].append(str(reqDes[j]["kode_bps"]))
                self.desa["nama_bps"].append(reqDes[j]["nama_bps"])
                self.desa["kode_dagri"].append(reqDes[j]["kode_dagri"])
                self.desa["nama_dagri"].append(reqDes[j]["nama_dagri"])

    def createExcel(self):
        df_prov = pd.DataFrame(self.provinsi)
        df_kab = pd.DataFrame(self.kabupaten)
        df_kec = pd.DataFrame(self.kecamatan)
        df_desa = pd.DataFrame(self.desa)
        write = pd.ExcelWriter("dataWilayah.xlsx", engine="xlsxwriter")
        df_prov.to_excel(write, sheet_name="Provinsi", index=False)
        df_kab.to_excel(write, sheet_name="Kabupaten", index=False)
        df_kec.to_excel(write, sheet_name="Kecamatan", index=False)
        df_desa.to_excel(write, sheet_name="Desa", index=False)
        write.save()

    def uploadToIPFS(self):
        w3_token = os.getenv("storage_token")
        root_url = "https://api.web3.storage/upload"
        files = {"file": open("dataWilayah.xlsx", "rb")}
        headers = {"Authorization": "Bearer " + w3_token}
        r = requests.post(root_url, files=files, headers=headers)
        print("CID Mu nih : {}".format(r.json()["cid"]))

    def main(self):
        self.getProv()
        self.getKab()
        self.getKec()
        self.getDes()
        self.createExcel()
        self.uploadToIPFS()


test = DataWilayah()
test.main()
