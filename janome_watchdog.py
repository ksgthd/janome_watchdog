#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from janome.tokenizer import Tokenizer
import time
import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

t = Tokenizer(mmap=True)

#BASEDIR = os.path.abspath(os.path.dirname(__file__))
BASEDIR = './text/'
OUTDIR = './out/'

def getext(filename):
	return os.path.splitext(filename)[-1].lower()

class ChangeHandler(FileSystemEventHandler):
	#
	def on_created(self, event):
		if event.is_directory:
			return
		if getext(event.src_path) in ('.txt',) and event.src_path.find("str_") > -1:
			with open(event.src_path, "r", encoding="utf-8") as f:
				lines = f.readlines()
			str_ = ""
			for line in lines:
				line_ = line.split("\n")
				str_ += line_[0] + " "
			print(str_)
			tokens = t.tokenize(str_.lower())
			this_token_ = []
			for token in tokens:
				if token.surface == "":
					continue
				#品詞を指定して出力
				if "名詞" in token.part_of_speech or "カスタム" in token.part_of_speech:
					this_token_.append(token.surface)
			path_sp = event.src_path.split("_")
			f = open(OUTDIR + '/' + "wakati_" + path_sp[len(path_sp)-1], "w", encoding="utf-8")
			f.write(" ".join(this_token_))
			f.close()
	"""
	#ファイル修正をトリガーとする処理
	def on_modified(self, event):
		if event.is_directory:
			return
		if getext(event.src_path) in ('.txt',):
			pass
	"""
	"""
	#ファイル削除をトリガーとする処理
	def on_deleted(self, event):
		if event.is_directory:
			return
		if getext(event.src_path) in ('.txt',):
			pass
	"""
if __name__ in '__main__':
	while 1:
		event_handler = ChangeHandler()
		observer = Observer()
		observer.schedule(event_handler, BASEDIR, recursive=True)
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()