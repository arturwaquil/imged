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

		self.buttonQuit			= Button(self.butFrame, 	text='Quit',		 	command=self.quit						).pack(fill=BOTH)
		self.buttonOpen			= Button(self.butFrame, 	text='Open image', 		command=self.openImage					).pack(fill=BOTH)
		self.buttonRevert		= Button(self.butFrame, 	text='Revert to original',command=self.revertImage				).pack(fill=BOTH)
		self.buttonSave			= Button(self.butFrame, 	text='Save image', 		command=self.saveImage					).pack(fill=BOTH)
		self.flipLabel 			= Label(self.butFrame)
		self.flipLabel.pack()
		self.flipText			= Label(self.flipLabel, 	text='Flip:'													).pack(fill=BOTH, side='left')
		self.buttonFlipHor 		= Button(self.flipLabel,	text='Horiz',			command=lambda: self.flip('HORIZONTAL')	).pack(fill=BOTH, side='left')
		self.buttonFlipVer 		= Button(self.flipLabel,	text='Vert',			command=lambda: self.flip('VERTICAL')	).pack(fill=BOTH, side='right')
		self.brightLabel		= Label(self.butFrame)
		self.brightLabel.pack()
		self.brightText			= Label(self.brightLabel,	text='Brightness:'												).pack(fill=BOTH, side='left')
		self.buttonBrightUp		= Button(self.brightLabel,	text='Up',				command=lambda: self.brightness('UP')	).pack(fill=BOTH, side='left')
		self.buttonBrightDown	= Button(self.brightLabel,	text='Down',			command=lambda: self.brightness('DOWN')	).pack(fill=BOTH, side='right')
		self.contrastLabel		= Label(self.butFrame)
		self.contrastLabel.pack()
		self.contrastText		= Label(self.contrastLabel, text='Contrast:'												).pack(fill=BOTH, side='left')
		self.buttonContrastUp	= Button(self.contrastLabel,text='Up',				command=lambda: self.contrast('UP')		).pack(fill=BOTH, side='left')
		self.buttonContrastDown	= Button(self.contrastLabel,text='Down',			command=lambda: self.contrast('DOWN')	).pack(fill=BOTH, side='right')
		self.buttonGray 		= Button(self.butFrame, 	text='Grayscale', 		command=self.grayscale 					).pack(fill=BOTH)
		self.buttonQuant 		= Button(self.butFrame, 	text='Quantization', 	command=self.quantization 				).pack(fill=BOTH)
		self.buttonNeg			= Button(self.butFrame, 	text='Negative',		command=self.negative 					).pack(fill=BOTH)
		self.buttonHist			= Button(self.butFrame, 	text='Histogram',		command=self.histogram 					).pack(fill=BOTH)
		self.buttonEqualize		= Button(self.butFrame, 	text='Equalize Histo',	command=self.equalizeHistograms			).pack(fill=BOTH)
		self.buttonMatch		= Button(self.butFrame, 	text='Match Histos',	command=self.matchHistograms			).pack(fill=BOTH)
		self.zoomLabel 			= Label(self.butFrame)
		self.zoomLabel.pack()
		self.zoomText			= Label(self.zoomLabel, 	text='Zoom:'													).pack(fill=BOTH, side='left')
		self.buttonZoomIn		= Button(self.zoomLabel,	text='In ',				command=lambda: self.zoom('IN')			).pack(fill=BOTH, side='left')
		self.buttonZoomOut		= Button(self.zoomLabel,	text='Out',				command=lambda: self.zoom('OUT')		).pack(fill=BOTH, side='right')
		self.rotateLabel		= Label(self.butFrame)
		self.rotateLabel.pack()
		self.rotateText			= Label(self.rotateLabel, 	text='Rotate:'													).pack(fill=BOTH, side='left')
		self.buttonRotLeft		= Button(self.rotateLabel,	text='Left',			command=lambda: self.rotate('LEFT')		).pack(fill=BOTH, side='left')
		self.buttonRotRight		= Button(self.rotateLabel, 	text='Right',			command=lambda: self.rotate('RIGHT')	).pack(fill=BOTH, side='right')

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
			self.origImage = self.image.copy()
			self.updateLabel(self.image)

	def revertImage(self):
		self.image = self.origImage.copy()
		self.updateLabel(self.image)

	def saveImage(self):
		try:
			filename = filedialog.asksaveasfilename(initialdir='~/Pictures',title='Save image')
		except Exception as error:
			messagebox.showerror('Error','An error occurred: <error>')

		if filename:
			cv2.imwrite(filename, self.image)

	def flip(self, option):
		h, w, _ = self.image.shape
		temp = np.zeros((h,w,3), np.uint8)
		if option == 'HORIZONTAL':
			for i in range(0,w):
				temp[:,i,:] = self.image[:,w-i-1,:]
		elif option == 'VERTICAL':
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

	def brightness(self, option):
		if option == 'UP':
			bias = 20
		elif option == 'DOWN':
			bias = -20
		self.image = cv2.addWeighted(self.image, 1, np.zeros(self.image.shape, self.image.dtype), 0, bias)
		self.updateLabel(self.image)

	def contrast(self, option):
		if option == 'UP':
			gain = 1.25
		elif option == 'DOWN':
			gain = 0.8
		self.image = cv2.addWeighted(self.image, gain, np.zeros(self.image.shape, self.image.dtype), 0, 0)
		self.updateLabel(self.image)

	def negative(self):
		self.image[:,:,:] = 255 - self.image[:,:,:]
		self.updateLabel(self.image)

	def histogram(self):
		pass

	def equalizeHistograms(self):
		pass

	def matchHistograms(self):
		pass

	def zoom(self, option):
		h, w, _ = self.image.shape
		if option == 'IN':# and h < 2000 and w < 2000:
			temp1 = np.zeros((h,2*w,3), np.uint8)
			for i in range(0,w):
				temp1[:,2*i,:] = self.image[:,i,:]
				temp1[:,2*i+1,:] = self.image[:,i,:]
			temp = np.zeros((2*h,2*w,3), np.uint8)
			for j in range(0,h):
				temp[2*j,:,:] = temp1[j,:,:]
				temp[2*j+1,:,:] = temp1[j,:,:]
		elif option == 'OUT' and h > 10 and w > 10:
			temp1 = np.zeros((h,int(w/2),3), np.uint8)
			for i in range(0,int(w/2)):
				temp1[:,i,:] = (self.image[:,2*i,:] + self.image[:,2*i+1,:])/2
			temp = np.zeros((int(h/2),int(w/2),3), np.uint8)
			for j in range(0,int(h/2)):
				temp[j,:,:] = (temp1[2*j,:,:] + temp1[2*j+1,:,:])/2

		self.image = temp
		self.updateLabel(self.image)

	def rotate(self, option):
		h, w, _ = self.image.shape
		temp = np.zeros((w,h,3), np.uint8) # null image with inverted dimensions
		if option == 'LEFT':
			for i in range(0,w):
				temp[w-i-1,:,:] = self.image[:,i,:]
		elif option == 'RIGHT':
			for j in range(0,h):
				temp[:,h-j-1,:] = self.image[j,:,:]
		self.image = temp
		self.updateLabel(self.image)

	def convolutiom(self, kernel):
		pass

if __name__ == '__main__':
	app = Editor()
	app.mainloop()
