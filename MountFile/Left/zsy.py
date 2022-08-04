import zipfile
import os   #（单个）不用

zipfile=zipfile.ZipFile(r"lujing.zip","w".zipfile.zipfile.zipfile.ZIP_DEFLATED)
zipfile.write(r"lujing.txt")
zipfile.close()  # 压缩（单个）


# savfepath=r"lujing" #解压缩（单个）

# zipfile=zipfile.ZipFile(r"lujing","r") #code
# for filename in zipfile.namelist():
#     data=zipfile.read(filename)

#     filelist=filename.splist("/")
#     mysavfepath=savfepath
#     savfepath savfepath+=("\\"+filelist[len(filelist) -1])
#     print(filelist)
#     file=open(savfepath,"wb")
#     file.write(data)
#     file.close()



# myzipfile=zipfile.ZipFile(r"lujing","w".zipfile.ZIP_DEFLATED)
# dirpath=r"lujing"
# for dir_path,filename,filenames in os.walk(dirpath):
#     for filename in filenames:
#         myzipfile.write(os.path.join(dir_path.filename))

# myzipfile.close()   #压缩文件夹













