import gdb
import os
import sys
import shutil

class SelectUniqueCorpus(gdb.Command):
	"""
	Select Unique Corpus from Fuzz's output
	Usage: sqs argFmt Fuzz's ouput directory unique's directory
	Example:
			(gdb) sqs -i out unique
	"""

	# Regsiter sqs Command
	def __init__(self):
		super(self.__class__, self).__init__("sqs", gdb.COMMAND_USER)



	# entry point
	def invoke(self, args, from_tty):
		argv = gdb.string_to_argv(args)
		if len(argv) != 3:
			raise gdb.GdbError("Select Unique Corpus takes Three arguments")

		print("Select Unique Corpus")

		fmt = argv[0]
		corpusPath = argv[1]
		uniquePath = argv[2]
		uniqueTrace = []


		corpusName = os.listdir(corpusPath)
		uniqueName = os.listdir(uniquePath)

		total = len(uniqueName)
		# unique is not none
		# init uniqueTrace
		if total:
			for name in uniqueName:
				case = uniquePath + "/" + name
				runCmd = "r {} {}".format(fmt, case)
				try:
					reback = gdb.execute(runCmd, to_string = True)
					btrace = gdb.execute("bt", to_string = True)
					traces = btrace.split('\n')[:-1]
					traceUtils = tuple([trace.split(' ')[2] for trace in traces])
					uniqueTrace.append(traceUtils)
				except:
					continue

		for corpus in corpusName:
			case = corpusPath + "/" + corpus
			runCmd = "r {} {}".format(fmt, case)

			try: 
				reback = gdb.execute(runCmd, to_string = True)
				btrace = gdb.execute("bt", to_string = True)
				traces = btrace.split('\n')[:-1]
				traceUtils = tuple([trace.split(' ')[2] for trace in traces])

				if not (traceUtils in uniqueTrace):
					uniqueTrace.append(traceUtils)
					total += 1
					unique = uniquePath + "/" + corpus
					self.saveUnique(case, unique)

					print(traceUtils)
					input("continue")
			except:
				continue

		print("Done!!!")
		print("Total unique cases: {}".format(total))

	def saveUnique(self, corpus, unique):
		shutil.copyfile(corpus, unique)
		pass

SelectUniqueCorpus()
