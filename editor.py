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

		self.butFrame = Frame(self)
		self.butFrame.grid(row=0,column=1)

		# buttons here
		self.buttonQuit		= Button(self.butFrame, text='Quit',		 	command=self.quit)
		self.buttonOpen		= Button(self.butFrame, text='Open image', 		command=self.openImage)
		self.buttonSave		= Button(self.butFrame, text='Save image', 		command=self.saveImage)
		self.flipLabel 		= Label(self.butFrame)
		self.buttonFlipHor 	= Button(self.flipLabel, text='Flip Horiz',		command=lambda: self.flip('HORIZONTAL'))
		self.buttonFlipVer 	= Button(self.flipLabel, text='Flip Vert',		command=lambda: self.flip('VERTICAL'))
		self.buttonGray 	= Button(self.butFrame, text='Grayscale', 		command=self.grayscale)
		self.buttonQuant 	= Button(self.butFrame, text='Quantization', 	command=self.quantization)
		self.buttonBright	= Button(self.butFrame, text='Brightness',		command=self.brightness)
		self.buttonContrast	= Button(self.butFrame, text='Contrast',		command=self.contrast)
		self.buttonNeg		= Button(self.butFrame, text='Negative',		command=self.negative)
		self.buttonHist		= Button(self.butFrame, text='Histogram',		command=self.histogram)
		self.buttonEqualize	= Button(self.butFrame, text='Equalize Histo',	command=self.equalizeHistograms)
		self.buttonMatch	= Button(self.butFrame, text='Match Histos',	command=self.matchHistograms)
		self.zoomLabel 		= Label(self.butFrame)
		self.buttonZoomIn	= Button(self.zoomLabel, text='Zoom In ',		command=lambda: self.zoom('IN'))
		self.buttonZoomOut	= Button(self.zoomLabel, text='Zoom Out',		command=lambda: self.zoom('OUT'))
		self.buttonRotate	= Button(self.butFrame, text='Rotate',			command=self.rotate) # just 1 button?

		self.buttonQuit.pack(fill=BOTH)
		self.buttonOpen.pack(fill=BOTH)
		self.buttonSave.pack(fill=BOTH)
		self.flipLabel.pack()
		self.buttonFlipHor.pack(fill=BOTH, side='left')
		self.buttonFlipVer.pack(fill=BOTH, side='right')
		self.buttonGray.pack(fill=BOTH)
		self.buttonQuant.pack(fill=BOTH)
		self.buttonBright.pack(fill=BOTH)
		self.buttonContrast.pack(fill=BOTH)
		self.buttonNeg.pack(fill=BOTH)
		self.buttonHist.pack(fill=BOTH)
		self.buttonEqualize.pack(fill=BOTH)
		self.buttonMatch.pack(fill=BOTH)
		self.zoomLabel.pack()
		self.buttonZoomIn.pack(fill=BOTH, side='left')
		self.buttonZoomOut.pack(fill=BOTH, side='right')
		self.buttonRotate.pack(fill=BOTH)

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
		self.image[:,:,:] = 255 - self.image[:,:,:]
		self.updateLabel(self.image)

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
