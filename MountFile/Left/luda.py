import os
import sys

# fout=open('./目录大小.txt',"w")
directory=sys.argv[1]
sum_size=0

for root,dirs,files in os.walk(directory):
# for root,dirs,files in os.walk("c:\\):
    for file in files:
        sum_size +=os.path.getsize(os.path.join(root,file))
print(sum_size)
# sum_size=sum_size/1024/1024/1024
if sum_size >5012:

# print(sum_size)

# if file.endswith("sum_size >5012"):
#     fout.write(directory +"\n")

# fout.close()
    print("目录大小：",sum_size/1024/1024/1024,"GB","\n","Tree") 

else:
    print("目录大小：",sum_size/1024/1024/1024,"GB","\n","Fale") 

# fout.close()
