from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np
import PIL.Image
import PIL.ImageTk

class Editor(Tk):

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
		self.buttonQuit		= Button(butFrame, text='Quit',		 		command=self.quit						).pack(fill=BOTH, expand=1)
		self.buttonOpen		= Button(butFrame, text='Open image', 		command=self.openImage					).pack(fill=BOTH, expand=1)
		self.buttonSave		= Button(butFrame, text='Save image', 		command=self.saveImage					).pack(fill=BOTH, expand=1)
		self.buttonFlipHor 	= Button(butFrame, text='Flip Horizontally',command=lambda: self.flip('HORIZONTAL')	).pack(fill=BOTH, expand=1)
		self.buttonFlipVer 	= Button(butFrame, text='Flip Vertically', 	command=lambda: self.flip('VERTICAL')	).pack(fill=BOTH, expand=1)
		self.buttonGray 	= Button(butFrame, text='Grayscale', 		command=self.grayscale					).pack(fill=BOTH, expand=1)
		self.buttonQuant 	= Button(butFrame, text='Quantization', 	command=self.quantization				).pack(fill=BOTH, expand=1) 
		self.buttonBright	= Button(butFrame, text='Brightness',		command=self.brightness					).pack(fill=BOTH, expand=1)
		self.buttonContrast	= Button(butFrame, text='Contrast',			command=self.contrast					).pack(fill=BOTH, expand=1)
		self.buttonNeg		= Button(butFrame, text='Negative',			command=self.negative					).pack(fill=BOTH, expand=1)
		self.buttonHist		= Button(butFrame, text='Histogram',		command=self.histogram					).pack(fill=BOTH, expand=1)
		self.buttonEqualize	= Button(butFrame, text='Equalize Histo',	command=self.equalizeHistograms			).pack(fill=BOTH, expand=1)
		self.buttonMatch	= Button(butFrame, text='Match Histos',		command=self.matchHistograms			).pack(fill=BOTH, expand=1)
		self.buttonZoomIn	= Button(butFrame, text='Zoom In',			command=lambda: self.zoom('IN')			).pack(fill=BOTH, expand=1) # just 1 method?
		self.buttonZoomOut	= Button(butFrame, text='Zoom Out',			command=lambda: self.zoom('OUT')		).pack(fill=BOTH, expand=1)
		self.buttonRotate	= Button(butFrame, text='Rotate',			command=self.rotate						).pack(fill=BOTH, expand=1) # just 1 button?
		

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
		h, w, _ = self.image.shape
		temp = np.zeros((h,w,3), np.uint8)
		if direction == 'HORIZONTAL':
			for i in range(0,w):
				temp[:,i,:] = self.image[:,w-i-1,:]
		elif direction == 'VERTICAL':
			for j in range(0,h):
				temp[j,:,:] = self.image[h-j-1,:,:]
		self.image = temp
		self.updateLabel(self.image)

	def grayscale(self):
		b = self.image[:,:,0]
		g = self.image[:,:,1]
		r = self.image[:,:,2]
		gray = 0.114*b + 0.587*g + 0.299*r
		self.image[:,:,0] = self.image[:,:,1] = self.image[:,:,2] = gray
		self.updateLabel(self.image)

	def quantization(self):
		pass

	def brightness(self):
		pass

	def contrast(self):
		pass

	def negative(self):
		pass

	def histogram(self):
		pass

	def equalizeHistograms(self):
		pass

	def matchHistograms(self):
		pass

	def zoom(self, direction):
		pass

	def rotate(self):
		pass

if __name__ == '__main__':
	app = Editor()
	app.mainloop()
