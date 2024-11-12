import mysql.connector
import os
os.system('cls' if os.name == 'nt' else 'clear')

PIWI_Server = 'Piwigo-ServerName'
PIWI_Database = 'Piwigo-Database'
PIWI_Account = 'Piwigo-Login'
PIWI_Password = 'Piwigo-Login-Password'

COPP_Server = 'Coppermine-ServerName'
COPP_Database = 'Coppermine-Database'
COPP_Account = 'Coppermine-Login'
COPP_Password = 'Coppermine-Login-Password'
COPP_PreTag = 'cpg_'

PIWI_Connect = mysql.connector.connect(
  host=PIWI_Server,
  database = PIWI_Database,
  user=PIWI_Account,
  password=PIWI_Password,
  buffered=True
)
COPP_Connect = mysql.connector.connect(
  host=COPP_Server,
  database = COPP_Database,
  user=COPP_Account,
  password=COPP_Password,
  buffered=True
)

PIWI_Cursor = PIWI_Connect.cursor()
COPP_Cursor = COPP_Connect.cursor()

COPP_Gallery = input("Please enter the coppermine gallery id (check adress bar, the number after 'album='): ")
print("Please enter the piwigo category id (Check adress bar, the number after 'category/'")
PIWI_Categorie = input("(Don't enter anything and press enter for the last category): ")

COPP_QUERY = "SELECT filename,pwidth,pheight,title,caption FROM cpg_pictures where aid = " + COPP_Gallery
COPP_Cursor.execute(COPP_QUERY)
COPP_ImagesInfo = COPP_Cursor.fetchall()

if len(PIWI_Categorie) == 0:
    PIWI_Last_Cat_QRY = "SELECT id FROM piwigo_categories order by id desc limit 1"
    PIWI_Cursor.execute(PIWI_Last_Cat_QRY)
    PIWI_Results = PIWI_Cursor.fetchall()
    for PIWI_RESULT in PIWI_Results:
        PIWI_Categorie = PIWI_RESULT[0]

PIWI_QUERY = "SELECT image_id FROM piwigo_image_category where category_id = "+str(PIWI_Categorie)
PIWI_Images = ""
PIWI_Cursor.execute(PIWI_QUERY)
PIWI_ImageIDs = PIWI_Cursor.fetchall()
for PIWI_ImageID in PIWI_ImageIDs:
    PIWI_Images = PIWI_Images + str(PIWI_ImageID[0]) +","
PIWI_Images = PIWI_Images.rstrip(",")

LoopCounter = 1
for COPP_ImageInfo in COPP_ImagesInfo:
    PIWI_UpdateQRY = "UPDATE piwigo_images set Comment = '"+COPP_ImageInfo[4]+"', name = '"+str(COPP_ImageInfo[3])+"' where file = '"+COPP_ImageInfo[0]+"'\
        and width = '"+str(COPP_ImageInfo[1])+"' and height = '"+str(COPP_ImageInfo[2])+"' and id in ("+PIWI_Images+")"
    # print(PIWI_UpdateQRY)
    PIWI_Cursor.execute(PIWI_UpdateQRY)
    if LoopCounter == 10:
        print('O',end="")
        LoopCounter = 1
    else:
        print('.',end="")
        LoopCounter = LoopCounter + 1
print('')
# 5781

COPP_Connect.close
PIWI_Connect.close
