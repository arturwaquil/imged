from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import PIL.Image
import PIL.ImageTk
# import numpy as np

class GUI(Tk):

	def __init__(self):
		Tk.__init__(self)
		self.title('Image Editor')
		self.resizable(0,0)

		self.imageLabel = Label(self)
		self.imageLabel.grid(row=0,column=0)

		self.openImage('cameraman.jpg')

		butFrame = Frame(self)
		butFrame.grid(row=0,column=1)

		# buttons here
		self.buttonQuit		= Button(butFrame, text='Quit',		 		command=self.quit				).pack(fill=BOTH, expand=1)
		self.buttonOpen		= Button(butFrame, text='Open image', 		command=self.openImage			).pack(fill=BOTH, expand=1)
		self.buttonSave		= Button(butFrame, text='Save image', 		command=self.saveImage			).pack(fill=BOTH, expand=1)
		self.buttonFlipHor 	= Button(butFrame, text='Flip Horizontally',command=self.flip('HORIZONTAL')	).pack(fill=BOTH, expand=1)
		self.buttonFlipVer 	= Button(butFrame, text='Flip Vertically', 	command=self.flip('VERTICAL')	).pack(fill=BOTH, expand=1)
		self.buttonGray 	= Button(butFrame, text='Grayscale', 		command=self.grayscale			).pack(fill=BOTH, expand=1)
		self.buttonQuant 	= Button(butFrame, text='Quantization', 	command=self.quantization		).pack(fill=BOTH, expand=1) 

	def updateLabel(self, img):
		tempImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
		tempImg = PIL.Image.fromarray(tempImg)
		tempImg = PIL.ImageTk.PhotoImage(image=tempImg)
		self.imageLabel.configure(image=tempImg)
		self.imageLabel.image = tempImg

	def openImage(self, filename=None):
		if filename is None:	# if the filename was not passed as a parameter
			try:
				filename = filedialog.askopenfilename(initialdir='~/Pictures',title='Open image') #, filetypes=(("image files", "*.jpg"),("all files", "*.*")))
			except(OSError, FileNotFoundError):
				messagebox.showerror('Error','Unable to find or open file <filename>')
			except Exception as error:
				messagebox.showerror('Error','An error occurred: <error>')

		if filename:	# if filename is not an empty string
			self.image = cv2.imread(filename)	
			self.updateLabel(self.image)

	def saveImage(self):
		try:
			filename = filedialog.asksaveasfilename(initialdir='~/Pictures',title='Save image')
		except Exception as error:
			messagebox.showerror('Error','An error occurred: <error>')

		if filename:
			cv2.imwrite(filename, self.image)

	def flip(self, direction):
		pass	

	def grayscale(self):
		b = self.image[:,:,0]
		g = self.image[:,:,1]
		r = self.image[:,:,2]
		gray = 0.114*b + 0.587*g + 0.299*r
		self.image[:,:,0] = self.image[:,:,1] = self.image[:,:,2] = gray
		self.updateLabel(self.image)

	def quantization(self):
		pass

if __name__ == '__main__':
	gui = GUI()
	gui.mainloop()
