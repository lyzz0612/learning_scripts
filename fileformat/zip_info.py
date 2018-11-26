#coding=utf8
import os
import struct

END_LOCATOR_SIGNATURE = int('0x06054b50', 16)
file_path = "Docs.zip"

class EndLocator:
	def __init__(self):
		self.signature = int("0x06054b50", 16)
		self.elDiskNumber = 0  				#当前磁盘编号
		self.elStartDiskNumber = 0			#中央目录开始位置的磁盘编号
		self.elEntriesOnDisk = 0			#该磁盘上所记录的核心目录数量
		self.elEntriesInDirectory = 0		#中央目录结构总数
		self.elDirectorySize = 0			#中央目录的大小
		self.elDirectoryOffset = 0			#中央目录开始位置相对于文件头的偏移
		self.elCommentLen = 0				#注释长度
		self.elComment = ""					#注释内容
		self.total_len = 0

	def parse(self, end_text):
		struct_text = end_text[:22]
		end_data = struct.unpack("<I4HIIH", struct_text)

		self.elDiskNumber = end_data[1]
		self.elStartDiskNumber = end_data[2]
		self.elEntriesOnDisk = end_data[3]
		self.elEntriesInDirectory = end_data[4]
		self.elDirectorySize = end_data[5]
		self.elDirectoryOffset = end_data[6]
		self.elCommentLen = end_data[7]
		self.elComment = end_text[23:23+self.elCommentLen]
		self.total_len = len(end_text)

	def print_info(self):
		print "\n"
		print "=======================EndLocator======================="
		print "中央目录结束节大小为: %d" %(self.elCommentLen + 22)
		if self.elCommentLen + 22 < self.total_len:
			print "\t其后还有冗余字节: %d" %(self.total_len - self.elCommentLen - 22)
		print "目录结束标记：%s" %(hex(self.signature))
		print "当前磁盘编号: %d" %(self.elDiskNumber)
		print "中央目录开始位置的磁盘编号：%d" %(self.elStartDiskNumber)
		print "该磁盘上所记录的核心目录数量：%d" %(self.elEntriesOnDisk)
		print "中央目录结构总数：%d" %(self.elEntriesInDirectory)
		print "中央目录的大小: %d" %(self.elDirectorySize)
		print "中央目录开始位置相对于文件头的偏移：%d" %(self.elDirectoryOffset)
		print "注释长度：%d" %(self.elCommentLen)
		print "注释内容：%s" %(self.elComment)
		print "\n"

class DirEntry:
	def __init__(self):
		self.reset()

	def reset(self):
		self.signature = 0		  			#中央目录文件header标识（0x02014b50）
		self.deVersionMadeBy = 0		  	#压缩所用的pkware版本
		self.deVersionToExtract = 0		  	#解压所需pkware的最低版本
		self.deFlags = 0		  			#通用位标记
		self.deCompression = 0		  		#压缩方法
		self.deFileTime = 0		  			#文件最后修改时间
		self.deFileDate = 0		  			#文件最后修改日期
		self.deCrc = 0		  				#CRC-32校验码
		self.deCompressedSize = 0		  	#压缩后的大小
		self.deUncompressedSize = 0		  	#未压缩的大小
		self.deFileNameLength = 0		  	#文件名长度
		self.deExtraFieldLength = 0		  	#扩展域长度
		self.deFileCommentLength = 0		#文件注释长度
		self.deDiskNumberStart = 0		  	#文件开始位置的磁盘编号
		self.deInternalAttributes = 0		#内部文件属性
		self.deExternalAttributes = 0		#外部文件属性
		self.deHeaderOffset = 0		  		#本地文件头的相对位移
		self.deFileName = ""		  		#目录文件名
		self.deExtraField = ""		  		#扩展域
		self.deFileComment = ""		 		#文件注释内容

	def parse(self, file_obj):
		self.reset()
		struct_text = file_obj.read(46)
		if len(struct_text) != 46:
			return False
		struct_data = struct.unpack("<I6H3I5HII", struct_text)
		self.signature = struct_data[0]
		self.deVersionMadeBy = struct_data[1]
		self.deVersionToExtract = struct_data[2]
		self.deFlags = struct_data[3]
		self.deCompression = struct_data[4]
		self.deFileTime = struct_data[5]
		self.deFileDate = struct_data[6]
		self.deCrc = struct_data[7]
		self.deCompressedSize = struct_data[8]
		self.deUncompressedSize = struct_data[9]
		self.deFileNameLength = struct_data[10]
		self.deExtraFieldLength = struct_data[11]
		self.deFileCommentLength = struct_data[12]
		self.deDiskNumberStart = struct_data[13]
		self.deInternalAttributes = struct_data[14]
		self.deExternalAttributes = struct_data[15]
		self.deHeaderOffset = struct_data[16]
		self.deFileName = file_obj.read(self.deFileNameLength)
		self.deExtraField = file_obj.read(self.deExtraFieldLength)
		self.deFileComment = file_obj.read(self.deFileCommentLength)
		return True
	def print_info(self):
		print "\n"
		print "=======================DirEntry======================="
		print "中央目录文件header标识: %s" %(hex(self.signature))
		print "压缩所用的pkware版本: %d" %(self.deVersionMadeBy)
		print "解压所需pkware的最低版本: %d" %(self.deVersionToExtract)
		print "通用位标记: %d" %(self.deFlags)
		print "压缩方法:%d" %(self.deCompression)
		print "文件最后修改时间: %02d:%02d:%02d" %(self.deFileTime>>11, (self.deFileTime>>5)&0x3F, (self.deFileTime&0x1F) * 2)
		print "文件最后修改日期: %d-%02d-%02d" %((self.deFileDate>>9)+1980, (self.deFileDate>>5)&0xF, self.deFileDate&0x1F)
		print "CRC-32校验码：%d" %(self.deCrc)
		print "压缩后的大小：%d" %(self.deCompressedSize)
		print "未压缩的大小：%d" %(self.deUncompressedSize)
		print "文件名长度：%d" %(self.deFileNameLength)
		print "扩展域长度：%d" %(self.deExtraFieldLength)
		print "文件注释长度：%d" %(self.deFileCommentLength)
		print "文件开始位置的磁盘编号：%d" %(self.deDiskNumberStart)
		print "内部文件属性：%d" %(self.deInternalAttributes)
		print "外部文件属性：%d" %(self.deExternalAttributes)
		print "本地文件头的相对位移：%d" %(self.deHeaderOffset)
		print "目录文件名：%s" %(self.deFileName)
		print "扩展域：%s" %(self.deExtraField)
		print "文件注释内容：%s" %(self.deFileComment)
		print "\n"

class ZipInfo:
	def __init__(self, file_path):
		self.file_path = file_path
		self.end_locator = EndLocator()
		self.parse_endlocator()

	def parse_endlocator(self):
		end_signature = struct.pack("I", END_LOCATOR_SIGNATURE)
		with open(self.file_path, "rb") as file_obj:
			end_text = None
			offset = -24
			while True:
				file_obj.seek(offset, 2)
				end_data = file_obj.read(24)
				locator_start_index = end_data.find(end_signature) 
				if locator_start_index == -1:
					offset = offset - 20
					if file_obj.tell() < 20:
						break
				else:
					locator_start_offset = offset + locator_start_index
					file_obj.seek(locator_start_offset, 2)
					end_text = file_obj.read()
					break
			file_obj.close()
			if not end_text:
				return
			self.end_locator.parse(end_text)
			self.end_locator.print_info()

	def get_file_info(self):
		file_info = DirEntry()
		with open(self.file_path, "rb") as file_obj:
			file_obj.seek(self.end_locator.elDirectoryOffset, 0)
			for i in range(10):
				is_success = file_info.parse(file_obj)
				if not is_success:
					break
				file_info.print_info()

def main():
	test = ZipInfo(file_path)
	test.get_file_info()
if __name__ == '__main__':
	main()
