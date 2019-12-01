#!/usr/bin/python2
#-*- coding:utf-8-*-
import gdb
import os
import sys

#每次调试时，gbd自动判断是否开启PIE，
#拿到codebase 恢复正常的断点
class Break(gdb.Command):

	#help内容
	"""Break [symbol or address]
	Usage: bk breakpoints
	Example:
		(gdb) bk bk main or bk 0xdeadbeef
	"""

	#注册命令　名称
	def __init__(self):
		super(self.__class__, self).__init__("bk", gdb.COMMAND_USER)
		self.flag = 0
		self.code_base = 0
		self.e = None

	def dbg(self, msg):
		gdb.write(msg)

	def offset_to_addr(self, offset):
		if '0x' in offset:
			addr = int(offset, 16) + self.code_base
		else:
			addr = int(offset, 10) + self.code_base
		return hex(addr)

	def break_pie(self):
		#1. 得到code_base
		gdb.flush(gdb.STDOUT)
		ck_ret = gdb.execute("checksec", to_string = True)
		gdb.write(ck_ret)						#结果输出到stdout

		pie_state = ck_ret.split(':')[4]		#PIE_STATE & RELRO
		if 'ENABLED' in pie_state:
			gdb.execute('b* 0x000')				#tmp breakpoint
			try:
				gdb.execute('r')
			except Exception as e:				#gdb 不会忽略异常，python跳过异常
				self.e = e
				pass
			gdb.execute('delete 1')
			codebase = gdb.execute("codebase", to_string = True)
			self.dbg(codebase)
			self.code_base = int(codebase.split(':')[1][6:-1], 16)
			self.flag += 1

	def break_points(self, points):
		for bp in points:
			bp = self.offset_to_addr(bp)
			gdb.execute('b* ' + bp, to_string = True)


	def invoke(self, args, from_tty):
		#参数处理
		argv = gdb.string_to_argv(args)
		if len(argv) < 1:
			raise gdb.GdbError("输入参数数目不对，help bk获得用法")

		#具体功能实现
		#1、break PIE
		if self.flag == 0:
			self.break_pie()

		#2. 下真实断点
		self.break_points(argv)

		#3. 由于在拿PIE的时候没有正确处理异常，这里clean
		if self.flag == 1:
			self.flag += 1
			raise		
			
#　向gdb会话注册该自定义命令
Break()




